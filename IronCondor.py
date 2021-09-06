from NSEUtils import NSEUtils
import json
class IronCondor(NSEUtils):
	def __init__(self):
		self.description ="This is IronCondor"


	def backTest(self,stock,startdate,expiraydate):
		result={}
		sdsp=self.getStockPrice(stock,startdate)
		edsp=self.getStockPrice(stock,expiraydate)
		strikeprice=self.roundup(stock,sdsp)
		calloptionprice=self.getOptionPrice(stock,startdate,"CE",strikeprice,expiraydate)
		putoptionprice=self.getOptionPrice(stock,startdate,"PE",strikeprice,expiraydate)
		totalpreimium=self.roundup(stock,calloptionprice+putoptionprice)
		defcalloptionprice=self.getOptionPrice(stock,startdate,"CE",strikeprice+totalpreimium,expiraydate)
		defputoptionprice=self.getOptionPrice(stock,startdate,"PE",strikeprice-totalpreimium,expiraydate)
		exitcalloptionprice=self.getOptionPrice(stock,expiraydate,"CE",strikeprice,expiraydate)
		exitputoptionprice=self.getOptionPrice(stock,expiraydate,"PE",strikeprice,expiraydate)
		exitdefcalloptionprice=self.getOptionPrice(stock,expiraydate,"CE",strikeprice+totalpreimium,expiraydate)
		exitdefputoptionprice=self.getOptionPrice(stock,expiraydate,"PE",strikeprice-totalpreimium,expiraydate)
		ExpectedTotalPremium=calloptionprice+putoptionprice-defcalloptionprice-defputoptionprice
		ActualTotalPremium=exitcalloptionprice+exitputoptionprice-exitdefcalloptionprice-exitdefputoptionprice
		result["stock"]=stock
		result["expiry"]=expiraydate
		result["startdate"]=startdate
		result["sdsp"]=sdsp
		result["edsp"]=edsp
		result["strikeprice"]=strikeprice
		result["calloption"]=strikeprice
		result["putoption"]=strikeprice
		result["defcalloption"]=strikeprice+totalpreimium
		result["defputoption"]=strikeprice-totalpreimium
		result["calloptionprice"]=calloptionprice
		result["putoptionprice"]=putoptionprice
		result["defcalloptionprice"]=defcalloptionprice
		result["defputoptionprice"]=defputoptionprice
		result["PAndL"]=ExpectedTotalPremium-ActualTotalPremium
		result = json.dumps(result, indent = 4)
		return result
	def dailyTest(self,currentdate,result):
		data={}
		exitcalloptionprice=self.getOptionPrice(result["stock"],currentdate,"CE",result["calloption"],result["expiry"])
		exitputoptionprice=self.getOptionPrice(result["stock"],currentdate,"PE",result["putoption"],result["expiry"])
		exitdefcalloptionprice=self.getOptionPrice(result["stock"],currentdate,"CE",result["defcalloption"],result["expiry"])
		exitdefputoptionprice=self.getOptionPrice(result["stock"],currentdate,"PE",result["defputoption"],result["expiry"])
		ExpectedTotalPremium=result["calloptionprice"]+result["putoptionprice"]-result["defcalloptionprice"]-result["defputoptionprice"]
		if exitcalloptionprice == 'null':
			return False
		ActualTotalPremium=exitcalloptionprice+exitputoptionprice-exitdefcalloptionprice-exitdefputoptionprice
		data["currentdate"]=currentdate
		data["PAndL"]=ExpectedTotalPremium-ActualTotalPremium
		data = json.dumps(data, indent = 4)
		return data


if __name__== "__main__" :
	I=IronCondor()
	with open('expiry.json') as f:
		data = json.load(f)
	Monthdates=data['Monthly']
	for i in range(0,len(Monthdates)-1):
		result=I.backTest("MARUTI",Monthdates[i],Monthdates[i+1])
		result = json.loads(result)
		currentdate=I.convertDate(Monthdates[i])
		expirayday=I.convertDate(Monthdates[i+1])
		nextday=I.getNextDay(currentdate)
		data = json.dumps(result, indent = 4)
		print(data)
		while nextday != expirayday:
			x=I.dailyTest(str(nextday),result)
			nextday=I.getNextDay(nextday)
			if x != False:
				print(x)
		# result = json.dumps(result, indent = 4)
		# print(result,x)
		# break;
	# x=I.backTest("MARUTI","2021-06-","2021-07-29")
	# print(x)
	# f.close()



from NSEUtils import NSEUtils
import json
class AdjustedIronCondor(NSEUtils):
	def __init__(self):
		self.description ="This is IronCondor"


	def backTestATM(self,stock,startdate,expiraydate):
		#w1,w2,w3,w4,w5,w6
		result={}
		sdsp=self.getStockPrice(stock,startdate)
		edsp=self.getStockPrice(stock,expiraydate)
		strikeprice=self.roundup(stock,sdsp)
		w4=self.getOptionPrice(stock,startdate,"CE",strikeprice,expiraydate)
		w3=self.getOptionPrice(stock,startdate,"PE",strikeprice,expiraydate)
		w1=self.getOptionPrice(stock,startdate,"CE",strikeprice-self.roundup(stock,w4),expiraydate)
		w2=self.getOptionPrice(stock,startdate,"PE",strikeprice-self.roundup(stock,w3),expiraydate)
		w5=self.getOptionPrice(stock,startdate,"CE",strikeprice+self.roundup(stock,w4),expiraydate)
		w6=self.getOptionPrice(stock,startdate,"PE",strikeprice+self.roundup(stock,w3),expiraydate)
		ew4=self.getOptionPrice(stock,expiraydate,"CE",strikeprice,expiraydate)
		ew3=self.getOptionPrice(stock,expiraydate,"PE",strikeprice,expiraydate)
		ew1=self.getOptionPrice(stock,expiraydate,"CE",strikeprice-self.roundup(stock,w4),expiraydate)
		ew2=self.getOptionPrice(stock,expiraydate,"PE",strikeprice-self.roundup(stock,w3),expiraydate)
		ew5=self.getOptionPrice(stock,expiraydate,"CE",strikeprice+self.roundup(stock,w4),expiraydate)
		ew6=self.getOptionPrice(stock,expiraydate,"PE",strikeprice+self.roundup(stock,w3),expiraydate)
		print(sdsp,edsp,strikeprice)
		print(w1,w2,w3,w4,w5,w6)
		print(ew1,ew2,ew3,ew4,ew5,ew6)
		print(w1,ew1)
		print(w2,ew2)
		print(w3,ew3)
		print(w4,ew4)
		print(w5,ew5)
		print(w6,ew6)
		# result["stock"]=stock
		# result["expiry"]=expiraydate
		# result["startdate"]=startdate
		# result["sdsp"]=sdsp
		# result["edsp"]=edsp
		# result["strikeprice"]=strikeprice
		# result["calloption"]=strikeprice
		# result["putoption"]=strikeprice
		# result["defcalloption"]=strikeprice+totalpreimium
		# result["defputoption"]=strikeprice-totalpreimium
		# result["calloptionprice"]=calloptionprice
		# result["putoptionprice"]=putoptionprice
		# result["defcalloptionprice"]=defcalloptionprice
		# result["defputoptionprice"]=defputoptionprice
		# result["PAndL"]=ExpectedTotalPremium-ActualTotalPremium
		# result = json.dumps(result, indent = 4)
		# return result
	
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
	A=AdjustedIronCondor()
	with open('expiry.json') as f:
		data = json.load(f)
	Monthdates=data['Monthly']
	A.backTestATM("BANKNIFTY",Monthdates[0],Monthdates[1])
	# for i in range(0,len(Monthdates)-1):
	# 	result=A.backTestATM("BANKNIFTY",Monthdates[i],Monthdates[i+1])
	# 	result = json.loads(result)
	# 	result = json.dumps(result, indent = 4)
	# 	print(result)
	# weekdates=data['Weekly']
	# for i in range(0,len(weekdates)-1):
	# 	result=A.backTestATM("BANKNIFTY",weekdates[i],weekdates[i+1])
	# 	result = json.loads(result)
	# 	result = json.dumps(result, indent = 4)
	# 	print(result)
		# currentdate=I.convertDate(Monthdates[i])
		# expirayday=I.convertDate(Monthdates[i+1])
		# nextday=I.getNextDay(currentdate)
		# while nextday != expirayday:
		# 	x=I.dailyTest(str(nextday),result)
		# 	nextday=I.getNextDay(nextday)
		# 	if x != False:
		# 		print(x)
		# break;

		# result = json.dumps(result, indent = 4)
		# print(result,x)
		# break;
	# x=I.backTest("MARUTI","2021-06-","2021-07-29")
	# print(x)
	# f.close()



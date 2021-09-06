from NSEUtils import NSEUtils
import json
class Stradle(NSEUtils):
	def __init__(self):
		self.description ="This is Stradle"


	def backTest(self,stock,startdate,expiraydate):
		sdsp=self.getStockPrice(stock,startdate)
		edsp=self.getStockPrice(stock,expiraydate)
		strikeprice=self.roundup(stock,sdsp)
		calloptionprice=self.getOptionPrice(stock,startdate,"CE",strikeprice,expiraydate)
		putoptionprice=self.getOptionPrice(stock,startdate,"PE",strikeprice,expiraydate)
		totalpreimium=self.roundup(stock,calloptionprice+putoptionprice)
		exitcalloptionprice=self.getOptionPrice(stock,expiraydate,"CE",strikeprice,expiraydate)
		exitputoptionprice=self.getOptionPrice(stock,expiraydate,"PE",strikeprice,expiraydate)
		print("**********************")
		print("StartDate:",startdate,expiraydate)
		print("StartDateStockPrice:",sdsp)
		print("EndDateStockPrice:",edsp)
		# print("StrikePrice:",strikeprice)
		# print("calloptionprice:",calloptionprice)
		# print("putoptionprice:",putoptionprice)
		ExpectedTotalPremium=calloptionprice+putoptionprice
		ActualTotalPremium=exitcalloptionprice+exitputoptionprice
		# print("ExpectedTotalPremium:",ExpectedTotalPremium)
		# print("ActualTotalPremium:",ActualTotalPremium)
		print("TotalPAndL:",ExpectedTotalPremium-ActualTotalPremium)
		return ExpectedTotalPremium-ActualTotalPremium


if __name__== "__main__" :
	S=Stradle()
	with open('expiry.json') as f:
		data = json.load(f)
	Monthdates=data['Monthly']
	pAndl=0
	for i in range(0,len(Monthdates)-1):
		x=S.backTest("MARUTI",Monthdates[i],Monthdates[i+1])
		pAndl=pAndl+x
	print(pAndl)
	# I.backTest("MARUTI","2021-06-24","2021-07-29")
	# f.close()



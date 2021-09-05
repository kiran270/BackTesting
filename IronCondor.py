from NSEUtils import NSEUtils
class IronCondor(NSEUtils):
	def __init__(self):
		self.description ="This is IronCondor"

	def backTest(self,stock,startdate,expiraydate):
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
		print("**********************")
		print("StartDateStockPrice:",sdsp)
		print("EndDateStockPrice:",edsp)
		print("StrikePrice:",strikeprice)
		print("calloptionprice:",calloptionprice)
		print("putoptionprice:",putoptionprice)
		print("defcalloptionprice:",defcalloptionprice)
		print("defputoptionprice:",defputoptionprice)
		print("Exitcalloptionprice:",exitcalloptionprice)
		print("Exitputoptionprice:",exitputoptionprice)
		print("Exitdefcalloptionprice:",exitdefcalloptionprice)
		print("Exitdefputoptionprice:",exitdefputoptionprice)
		ExpectedTotalPremium=calloptionprice+putoptionprice-defcalloptionprice-defputoptionprice
		ActualTotalPremium=exitcalloptionprice+exitputoptionprice-exitdefcalloptionprice-exitdefputoptionprice
		print("ExpectedTotalPremium:",ExpectedTotalPremium)
		print("ActualTotalPremium:",ActualTotalPremium)
		print("TotalPAndL:",ExpectedTotalPremium-ActualTotalPremium)
	
I=IronCondor()
I.backTest("NIFTY","2021-02-25","2021-03-25")

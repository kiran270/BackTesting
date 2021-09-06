from nsepy import get_history
from datetime import date
import math
from nsepy.derivatives import get_expiry_date
import re
roundUpValues = {'NIFTY':50,'BANKNIFTY':100,'MARUTI':100,'SBIN':5}
class NSEUtils:
	
	def __init__(self):
		self.description ="This is NSEUtils"

	def getStockPrice(self,stock,sdate):
		index=False
		if stock == 'NIFTY' or stock == 'BANKNIFTY':
			index =True
		data = get_history(symbol=stock, start=self.convertDate(sdate), end=self.convertDate(sdate),index=index)
		return data.iloc[0]['Close']
	def getOptionPrice(self,stock,sdate,optiontype,strikeprice,expireydate):
		index=False
		if stock == 'NIFTY' or stock == 'BANKNIFTY':
			index =True
		data = get_history(symbol=stock,
                    	start=self.convertDate(sdate),
                        end=self.convertDate(sdate),
                        index=index,
                        option_type=optiontype,
                        strike_price=strikeprice,
                        expiry_date=self.convertDate(expireydate))
		return data.iloc[0]['Close']

	def convertDate(self,sdate):
		s=re.split("-",sdate)
		return date(int(s[0]),int(s[1]),int(s[2]))

	def roundup(self,stock,stockprice):
		return int(math.ceil(stockprice / roundUpValues[stock])) * roundUpValues[stock]

from decimal import Decimal

class BTM:

	def __init__(self, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
		self.priceModel = PriceModel(totalAmountBills,
                					 currentAmountBills,
                					 currentAmountBitcoin)

	def  buy_bills(amountBills):
		nAmountBills = amountBills.copy_negate()
		return self.priceModel.calculate(nAmountBills)

	def sell_bills(amountBills):
		amountBitcoin = self.priceModel.calculate(amountBills)
		return amountBitcoin.copy_negate()
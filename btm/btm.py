
import models

class BTM(object):

    def __init__(self, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
        self.priceModel = models.PriceModel(totalAmountBills,
                                            currentAmountBills,
                                            currentAmountBitcoin)

    def  buy_bills(self, amountBills):
        nAmountBills = amountBills.copy_negate()
        return self.priceModel.calculate(nAmountBills)

    def sell_bills(self, amountBills):
        amountBitcoin = self.priceModel.calculate(amountBills)
        return amountBitcoin.copy_negate()

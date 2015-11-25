
import models

class BTM(object):

    def __init__(self, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
        self.priceModel = models.PriceModel(totalAmountBills,
                                            currentAmountBills,
                                            currentAmountBitcoin)

    def  buy_bills(self, amountBills):
        nAmountBills = amountBills.copy_negate()
        amountBitcoin = self.priceModel.calculate(nAmountBills)
        self.priceModel.change_amount_bills(nAmountBills)
        self.priceModel.change_amount_bitcoin(amountBitcoin)

    def sell_bills(self, amountBills):
        amountBitcoin = self.priceModel.calculate(amountBills)
        self.priceModel.change_amount_bills(amountBills)
        self.priceModel.change_amount_bitcoin(amountBitcoin)

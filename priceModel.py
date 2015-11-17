
import decimal

class PriceModel:

	def __init__(self, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
        self.totalAmountBills = totalAmountBills
        self.currentAmountBills = currentAmountBills
        self.currentAmountBitcoin = currentAmountBitcoin
        self.eccentricity = decimal.Decimal("1")

    def calculate(amountBills):
        amountBitcoin = self.eccentricity * ((((self.totalAmountBills -
                        amountBills - self.currentAmountBills) *
                        (self.currentAmountBills)) / ((amountBills +
                        self.currentAmountBills) *
                        (self.totalAmountBills -
                        self.currentAmountBills))).ln() +
                        self.currentAmountBitcoin * ((1 -
                        amountBills.exp()) / (amountBills.exp())))
        return amountBitcoin
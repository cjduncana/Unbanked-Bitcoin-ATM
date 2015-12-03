
import decimal

class PriceModel(object):

    def __init__(self, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
        self.totalAmountBills = totalAmountBills
        self.currentAmountBills = currentAmountBills
        self.currentAmountBitcoin = currentAmountBitcoin
        self.eccentricity = decimal.Decimal("1")

    def calculate(self, amountBills):
        amountBitcoin = self.eccentricity * ((((self.totalAmountBills \
        - amountBills - self.currentAmountBills) \
        * (self.currentAmountBills)) / ((amountBills \
        + self.currentAmountBills) * (self.totalAmountBills \
        - self.currentAmountBills))).ln() + self.currentAmountBitcoin \
        * ((1 - amountBills.exp()) / (amountBills.exp())))

        return amountBitcoin

    def set_total_amount_bills(self, amount):
        self.totalAmountBills = amount

    def change_amount_bills(self, amount):
        self.currentAmountBills += amount

    def change_amount_bitcoin(self, amount):
        self.currentAmountBitcoin += amount

    def change_eccentricity(self, eccentricity):
        self.eccentricity *= eccentricity

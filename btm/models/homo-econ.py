
import csv
import decimal

import btm
import pid

dates = []
prices = []
quantity = 0

with open("../static/bitprices.csv") as csvFile:
    readCSV = csv.reader(csvFile, delimiter = ",")
    for row in readCSV:
        date = row[0]
        price = row[1]
        dates.append(date)
        prices.append(1 / decimal.Decimal(price))
        quantity += 1

currentAmountBills = decimal.Decimal(1000)
totalAmountBills = 2 * currentAmountBills
currentAmountBitcoin = prices[0] * currentAmountBills

xbtm = btm.BTM(totalAmountBills,
               currentAmountBills,
               currentAmountBitcoin)
  
class HomoEconPID(pid.PID):

    def __init__(self):
        pid.PID.__init__(self, currentAmountBills, currentAmountBills)

    def update(self):
        changeInTime = 1

        processVariable = self.model[-1]

        error = self.setPoint - processVariable
        self.integral += self.ki * error * changeInTime
        changeInInput = (processVariable - self.previousInput) \
        / changeInTime

        controlVariable = self.kp * error + self.integral - self.kd \
        * changeInInput

        self.previousInput = processVariable.normalize()

        return controlVariable.normalize()

xpid = HomoEconPID()

for x in range(quantity):
    successfulTransaction = False
    while True:
        xprice = xbtm.priceModel.calculate(decimal.Decimal(-1))
        if prices[x] > xprice and xprice > 0:
            print "A dollar was bought for " + xprice.to_eng_string() \
            + " Bitcoins on " + dates[x]
            xbtm.buy_bills(decimal.Decimal(1))
            successfulTransaction = True
            continue

        xprice = xbtm.priceModel.calculate(decimal.Decimal(1))
        if prices[x].copy_negate() > xprice and xprice < 0:
            print "A dollar was sold for " \
            + xprice.copy_negate().to_eng_string() \
            + " Bitcoins on " + dates[x]
            xbtm.sell_bills(decimal.Decimal(1))
            successfulTransaction = True
            continue

        xpid.add_point(xbtm.priceModel.currentAmountBills)
        controlVariable = xpid.update()
        eccentricityChange = (controlVariable \
        / xbtm.priceModel.currentAmountBills).exp()
        xbtm.priceModel.change_eccentricity(eccentricityChange)

        if successfulTransaction:
            successfulTransaction = False
            break
        else:
            print "No transactions were made on " + dates[x]
            successfulTransaction = False
            break

print("No more transactions will be made.\n")

if currentAmountBills > xbtm.priceModel.currentAmountBills:
    diff = currentAmountBills - xbtm.priceModel.currentAmountBills
    print "There is now " + diff.to_eng_string() + " fewer dollars."
elif currentAmountBills < xbtm.priceModel.currentAmountBills:
    diff =  xbtm.priceModel.currentAmountBills - currentAmountBills
    print "There is now " + diff.to_eng_string() + " more dollars."

if currentAmountBitcoin > xbtm.priceModel.currentAmountBitcoin:
    diff = currentAmountBitcoin - xbtm.priceModel.currentAmountBitcoin
    print "There is now " + diff.to_eng_string() + " fewer Bitcoins."
elif currentAmountBitcoin < xbtm.priceModel.currentAmountBitcoin:
    diff =  xbtm.priceModel.currentAmountBitcoin - currentAmountBitcoin
    print "There is now " + diff.to_eng_string() + " more Bitcoins."

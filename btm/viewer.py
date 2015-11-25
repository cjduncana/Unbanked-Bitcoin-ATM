
import decimal
from gi.repository import Gtk
import sys

import btm

class BTMWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application = app)
        self.set_title("Bitcoin ATM")
        self.set_border_width(10)

        info = InfoWindow(app, self)
        info.show_all()      

    def initiate_BTM(self, totalAmountBills,
                     currentAmountBills, currentAmountBitcoin):
        self.xbtm = btm.BTM(decimal.Decimal(totalAmountBills),
                       decimal.Decimal(currentAmountBills),
                       decimal.Decimal(currentAmountBitcoin))
        self.update_BTM_screen()
        self.show_all()

    def update_BTM_screen(self):

        for child in self.get_children():
            self.remove(child) 

        grid = Gtk.Grid()

        labels = ["Buy 3", "Buy 2", "Buy 1",
                  "Sell 1", "Sell 2", "Sell 3"]

        TWOPLACES = decimal.Decimal("0.01")

        for x in range(6):
            label = Gtk.Label(labels[x])
            label.set_margin_end(2)
            grid.attach(label, x, 0, 1, 1)

        for x in range(-3, 0):
            button = Gtk.Button(label = self.xbtm.priceModel.calculate(
                            decimal.Decimal(x)).quantize(TWOPLACES))
            button.set_can_focus(False)
            button.set_margin_end(2)
            button.connect("clicked", self.buy, -x)
            grid.attach(button, x + 3, 1, 1, 1)
        for x in range(1, 4):
            button = Gtk.Button(label = self.xbtm.priceModel.calculate(
                    decimal.Decimal(x))\
                    .quantize(TWOPLACES).copy_negate())
            button.set_can_focus(False)
            button.set_margin_end(2)
            button.connect("clicked", self.sell, x)
            grid.attach(button, x + 2, 1, 1, 1)

        self.add(grid)
        self.show_all()

    def buy(self, button, amount):
        self.xbtm.buy_bills(decimal.Decimal(amount))
        self.update_BTM_screen()
    
    def sell(self, button, amount):
        self.xbtm.sell_bills(decimal.Decimal(amount))
        self.update_BTM_screen()

class InfoWindow(Gtk.ApplicationWindow):

    def __init__(self, app, window):
        Gtk.Window.__init__(self, application = app)
        self.window = window

        grid = Gtk.Grid()

        tBillsLabel = Gtk.Label("Total Amount of Bills")
        cBillsLabel = Gtk.Label("Current Amount of Bills")
        cBitcoinLabel = Gtk.Label("Current Amount of Bitcoin")

        self.tBillsEntry = Gtk.Entry()
        self.cBillsEntry = Gtk.Entry()
        self.cBitcoinEntry = Gtk.Entry()

        submitButton = Gtk.Button(label = "Submit")
        submitButton.connect("clicked", self.on_submit_clicked)

        grid.attach(tBillsLabel, 0, 0, 1, 1)
        grid.attach(self.tBillsEntry, 1, 0, 1, 1)
        grid.attach(cBillsLabel, 0, 1, 1, 1)
        grid.attach(self.cBillsEntry, 1, 1, 1, 1)
        grid.attach(cBitcoinLabel, 0, 2, 1, 1)
        grid.attach(self.cBitcoinEntry, 1, 2, 1, 1)
        grid.attach(submitButton, 0, 3, 2, 1)

        self.add(grid)

    def on_submit_clicked(self, button):
        self.window.initiate_BTM(self.tBillsEntry.get_text(),
                                 self.cBillsEntry.get_text(),
                                 self.cBitcoinEntry.get_text())
        self.destroy()

class BTMApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        BTMWindow(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = BTMApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)


import decimal
from gi.repository import Gtk
import sys

import btm

class BTMWindow(Gtk.ApplicationWindow):

    def __init__(self, app, totalAmountBills,
                 currentAmountBills, currentAmountBitcoin):
        Gtk.Window.__init__(self,
                            title = "Bitcoin ATM", application = app)
        self.set_border_width(10)

        TWOPLACES = decimal.Decimal("0.01")

        xbtm = btm.BTM(decimal.Decimal(totalAmountBills),
                       decimal.Decimal(currentAmountBills),
                       decimal.Decimal(currentAmountBitcoin))

        grid = Gtk.Grid()

        labels = ["Buy 3", "Buy 2", "Buy 1",
                  "Sell 1", "Sell 2", "Sell 3"]

        for x in range(6):
            label = Gtk.Label(labels[x])
            label.set_margin_end(2)
            grid.attach(label, x, 0, 1, 1)

        for x in range(-3, 0):
            button = Gtk.Button(label = xbtm.priceModel.calculate(
                            decimal.Decimal(x)).quantize(TWOPLACES))
            button.set_can_focus(False)
            button.set_margin_end(2)
            grid.attach(button, x + 3, 1, 1, 1)
        for x in range(1, 4):
            button = Gtk.Button(label = xbtm.priceModel.calculate(
                    decimal.Decimal(x))\
                    .quantize(TWOPLACES).copy_negate())
            button.set_can_focus(False)
            button.set_margin_end(2)
            grid.attach(button, x + 2, 1, 1, 1)

        self.add(grid)

class InfoWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title = "", application = app)

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
        win = BTMWindow(app,
            self.tBillsEntry.get_text(),
            self.cBillsEntry.get_text(),
            self.cBitcoinEntry.get_text())
        win.show_all()

class BTMApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = InfoWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = BTMApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

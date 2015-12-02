
from gi.repository import GObject, Gtk

import decimal
import sys

import btm
import pid

class BTMWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application = app)

        self.set_title("Bitcoin ATM")
        self.set_border_width(10)
        self.connect("update", self.update_BTM_screen)

        self.info = InfoWindow(app, self)
        self.info.connect("delete-event", self.exit)
        self.info.show_all()      

    def initiate_BTM(self, totalAmountBills,
                     currentAmountBills, currentAmountBitcoin):
        self.xbtm = btm.BTM(decimal.Decimal(totalAmountBills),
                       decimal.Decimal(currentAmountBills),
                       decimal.Decimal(currentAmountBitcoin))

        self.show_all()
        self.info.destroy()
        self.emit("update")

        self.xpid = pid.PID(
            decimal.getcontext().divide_int(decimal.Decimal(
                self.xbtm.priceModel.totalAmountBills), 2),
            decimal.Decimal(
                self.xbtm.priceModel.currentAmountBills))

        GObject.timeout_add(10 * 1000, self.update_PID)

    def update_BTM_screen(self, window):
        del window

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

        currentAmountBills = self.xbtm.priceModel.currentAmountBills
        currentAmountBitcoin = self.xbtm.priceModel.currentAmountBitcoin
        totalAmountBills = self.xbtm.priceModel.totalAmountBills

        for x in range(-3, 0):
            price = self.xbtm.priceModel.calculate(decimal.Decimal(x))
            if currentAmountBills > -x:
                button = Gtk.Button(label = price.quantize(TWOPLACES))
                button.set_can_focus(False)
                button.set_margin_end(2)
                button.connect("clicked", self.buy, -x)
            else:
                button = Gtk.Button("Too Few Bills")
                button.set_can_focus(False)
                button.set_margin_end(2)
                button.set_sensitive(False)
            grid.attach(button, x + 3, 1, 1, 1)

        for x in range(1, 4):
            try:
                price = self.xbtm.priceModel.calculate(decimal.Decimal(x))
                if totalAmountBills - currentAmountBills > x:
                    button = Gtk.Button(
                        label = price.quantize(TWOPLACES).copy_negate())
                    button.set_can_focus(False)
                    button.set_margin_end(2)
                    button.connect("clicked", self.sell, x)
                else:
                    button = Gtk.Button("Too Many Bills")
                    button.set_can_focus(False)
                    button.set_margin_end(2)
                    button.set_sensitive(False)
            except decimal.InvalidOperation:
                button = Gtk.Button("Too Few Bitcoins")
                button.set_can_focus(False)
                button.set_margin_end(2)
                button.set_sensitive(False)
            finally:
                grid.attach(button, x + 2, 1, 1, 1)

        self.add(grid)
        self.show_all()

    def buy(self, button, amount):
        del button
        self.xbtm.buy_bills(decimal.Decimal(amount))
        self.emit("update")
    
    def sell(self, button, amount):
        del button
        self.xbtm.sell_bills(decimal.Decimal(amount))
        self.emit("update")

    def update_PID(self):
        self.xpid.add_point(self.xbtm.priceModel.currentAmountBills)
        controlVariable = self.xpid.update()
        eccentricityChange = controlVariable \
        / self.xbtm.priceModel.currentAmountBills
        self.xbtm.priceModel.change_eccentricity(eccentricityChange)
        self.emit("update")
        return True

    def exit(self, widget, event):
        del widget, event
        sys.exit()

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
        del button
        self.window.initiate_BTM(self.tBillsEntry.get_text(),
                                 self.cBillsEntry.get_text(),
                                 self.cBitcoinEntry.get_text())

class BTMApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        GObject.type_register(BTMWindow)
        GObject.signal_new("update", BTMWindow,
            GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())

    def do_activate(self):
        BTMWindow(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = BTMApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)


import decimal
from gi.repository import Gtk
import sys

import btm

class BTMWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self,
                            title = "Bitcoin ATM", application = app)
        self.set_default_size(350, 200)
        self.set_border_width(10)

        TWOPLACES = decimal.Decimal("0.01")

        xbtm = btm.BTM(decimal.Decimal("100"),
                       decimal.Decimal("50"),
                       decimal.Decimal("50"))

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_border_width(10)

        labels = ["Buy 3", "Buy 2", "Buy 1",
                  "Sell 1", "Sell 2", "Sell 3"]

        for x in range(6):
            label = Gtk.Label(labels[x])
            grid.attach(label, x, 0, 1, 1)

        for x in range(-3, 0):
            button = Gtk.Button(
                label = xbtm.buy_bills(
                    decimal.Decimal(x)).quantize(TWOPLACES))
            button.set_can_focus(False)
            grid.attach(button, x + 3, 1, 1, 1)
        for x in range(1, 4):
            button = Gtk.Button(
                label = xbtm.sell_bills(
                    decimal.Decimal(x)).quantize(TWOPLACES))
            button.set_can_focus(False)
            grid.attach(button, x + 2, 1, 1, 1)

        self.add(grid)

class BTMApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = BTMWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = BTMApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

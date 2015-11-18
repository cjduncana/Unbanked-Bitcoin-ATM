
import decimal
import unittest

import btm

class TestBTM(unittest.TestCase):

    def test_create_btm(self):
        xbtm = btm.BTM(decimal.Decimal("100"),
                       decimal.Decimal("50"),
                       decimal.Decimal("50"))
        assert xbtm.priceModel.totalAmountBills \
            == decimal.Decimal("100") \
           and xbtm.priceModel.currentAmountBills \
            == decimal.Decimal("50") \
           and xbtm.priceModel.currentAmountBitcoin \
            == decimal.Decimal("50")

    def test_buy_bills(self):
        xbtm = btm.BTM(decimal.Decimal("100"),
                       decimal.Decimal("50"),
                       decimal.Decimal("50"))
        assert xbtm.buy_bills(decimal.Decimal("1")) \
            == decimal.Decimal("85.95409675756596092944844792")

    def test_sell_bills(self):
        xbtm = btm.BTM(decimal.Decimal("100"),
                       decimal.Decimal("50"),
                       decimal.Decimal("50"))
        assert xbtm.sell_bills(decimal.Decimal("1")) \
            == decimal.Decimal("31.64603327604158308165788586")

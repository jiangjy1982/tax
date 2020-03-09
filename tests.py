import importlib
import unittest

from federal_tax_computer import RegularTaxComputer, AMTTaxComputer
from state_tax_computer import StateTaxComputer


class TestRedshiftInterface(unittest.TestCase):

    def setUp(self):
        pass

    def _test(self, module_name):
        numbers = importlib.import_module(module_name)
        params = {k: numbers.__dict__[k]
                  for k in dir(numbers) if not k.startswith('__')}

        rtc = RegularTaxComputer(**params)
        self.assertTrue(abs(rtc.tax - params['rt']) < 1)
        self.assertTrue(abs(rtc.additional_medicare_tax - params['mt']) < 1)
        self.assertTrue(abs(rtc.net_investment_income_tax - params['it']) < 1)

        if params['at'] is not None:
            atc = AMTTaxComputer(**params)
            self.assertTrue(abs(atc.tax - params['at']) < 1)

        stc = StateTaxComputer(**params)
        self.assertTrue(abs(stc.tax - params['st']) < 1)

    def test_2012(self):
        self._test('data.jiayan_2012')

    def test_2013(self):
        self._test('data.jiayan_2013')

    def test_2014(self):
        self._test('data.jiayan_2014')

    def test_2015(self):
        self._test('data.jiayan_2015')

    def test_2016(self):
        self._test('data.jiayan_2016')

    def test_2017(self):
        self._test('data.jiayan_2017')

    def test_2018(self):
        self._test('data.jiayan_2018')


if __name__ == '__main__':
        unittest.main()

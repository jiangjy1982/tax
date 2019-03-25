import importlib
import unittest

from tax import RegularTaxComputer, AMTTaxComputer, StateTaxComputer


class TestRedshiftInterface(unittest.TestCase):

    def setUp(self):
        pass

    def _test(self, module_name):
        numbers = importlib.import_module(module_name)
        params = {k: numbers.__dict__[k]
                  for k in dir(numbers) if not k.startswith('__')}

        rtc = RegularTaxComputer(**params)
        rt = rtc.get_tax()
        self.assertTrue(rt >= params['rt'] - 1 and rt <= params['rt'] + 1)
        mt = rtc.get_additional_medicare_tax()
        self.assertTrue(mt >= params['mt'] - 1 and mt <= params['mt'] + 1)
        it = rtc.get_net_investment_income_tax()
        self.assertTrue(it >= params['it'] - 1 and it <= params['it'] + 1)

        if params['at'] is not None:
            atc = AMTTaxComputer(**params)
            at = atc.get_tax()
            self.assertTrue(at >= params['at'] - 1 and at <= params['at'] + 1)

        stc = StateTaxComputer(**params)
        st = stc.get_tax()
        self.assertTrue(st >= params['st'] - 1 and st <= params['st'] + 1)

    def test_2012(self):
        self._test('jiayan_2012')

    def test_2013(self):
        self._test('jiayan_2013')

    def test_2014(self):
        self._test('jiayan_2014')

    def test_2015(self):
        self._test('jiayan_2015')

    def test_2016(self):
        self._test('jiayan_2016')

    def test_2017(self):
        self._test('jiayan_2017')

    def test_2018(self):
        self._test('jiayan_2018')


if __name__ == '__main__':
        unittest.main()

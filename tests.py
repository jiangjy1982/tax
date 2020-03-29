import importlib
import unittest

from federal_tax_computer import RegularTaxComputer, AMTTaxComputer
from state_tax_computer import StateTaxComputer


class TestRedshiftInterface(unittest.TestCase):

    def setUp(self):
        pass

    def _test(self, module_name, th=1.0):
        numbers = importlib.import_module(module_name)
        params = {k: numbers.__dict__[k]
                  for k in dir(numbers) if not k.startswith('__')}

        rtc = RegularTaxComputer(**params)

        rt_diff = abs(rtc.tax - params['rt'])
        self.assertTrue(rt_diff < th, f"diff: {rt_diff}")

        mt_diff = abs(rtc.additional_medicare_tax - params['mt'])
        self.assertTrue(mt_diff < th, f"diff: {mt_diff}")

        it_diff = abs(rtc.net_investment_income_tax - params['it'])
        self.assertTrue(it_diff < th, f"diff: {it_diff}")

        atc = AMTTaxComputer(**params)
        at_diff = abs(max(0, atc.tax - rtc.tax) - params['at'])
        self.assertTrue(at_diff < th, f"diff: {at_diff}")

        stc = StateTaxComputer(**params)

        st_diff = abs(stc.tax - params['st'])
        self.assertTrue(st_diff < th, f"diff: {st_diff}")

        mht_diff = abs(stc.mental_health_services_tax - params['mht'])
        self.assertTrue(mht_diff < th, f"diff: {mht_diff}")

        ft_due_diff = abs(
            max(rtc.tax, atc.tax)
            + rtc.additional_medicare_tax
            + rtc.net_investment_income_tax
            - rtc.credits
            - rtc.tax_withheld
            + rtc.penalty
            - params['ft_due'])
        self.assertTrue(ft_due_diff < th, f"diff: {ft_due_diff}")

        st_due_diff = abs(
            stc.tax
            + stc.mental_health_services_tax
            - stc.tax_withheld
            - params['st_due'])
        self.assertTrue(st_due_diff < th, f"diff: {st_due_diff}")


    def test_2012(self):
        self._test('data.jiayan_2012')

    def test_2013(self):
        self._test('data.jiayan_2013', 1.5)

    def test_2014(self):
        self._test('data.jiayan_2014')

    def test_2015(self):
        self._test('data.jiayan_2015')

    def test_2016(self):
        self._test('data.jiayan_2016', 1.5)

    def test_2017(self):
        self._test('data.jiayan_2017')

    def test_2018(self):
        self._test('data.jiayan_2018')


if __name__ == '__main__':
        unittest.main()

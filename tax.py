import argparse
import importlib
import logging
import matplotlib.pyplot as plt

from federal_tax_computer import RegularTaxComputer, AMTTaxComputer
from state_tax_computer import StateTaxComputer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        help='python module with tax info')
    parser.add_argument('-e', '--extrapolate',
                        action='store_true',
                        help='extrapolation analysis')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if not args.extrapolate else logging.INFO,
        format='%(funcName)s [%(lineno)d]: %(message)s')

    numbers = importlib.import_module(args.file)

    params = {
        k: numbers.__dict__[k] for k in dir(numbers) if not k.startswith('__')}

    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    ENDC = '\033[0m'

    logging.info(GREEN + "========== Regular Tax ==========" + ENDC)
    rtc = RegularTaxComputer(**params)
    logging.info(f"W2: {rtc.w2:.0f}")
    logging.info(f"Interest: {rtc.interest:.0f}")
    logging.info(f"Dividends: {rtc.dividends:.0f}")
    logging.info(f"    Qualified dividends: {rtc.qualified_dividends:.0f}")
    logging.info(f"IRA distributions: {rtc.roth_conversion_gain:.0f}")
    logging.info(f"Capital gain: {rtc.capital_gain:.0f}")
    logging.info(f"Other income: {rtc.other_income:.0f}")
    logging.info(f"    State refund: {rtc.state_refund:.0f}")
    logging.info(f"    Rental income: {rtc.rental_income:.0f}")
    logging.info(f"    Misc income: {rtc.misc_income:.0f}")
    logging.info(f"AGI: {rtc.agi:.0f}")
    logging.info(f"Taxable income: {rtc.taxable_income:.0f}")
    logging.info(f"Exemption: {rtc.exemption:.0f}")
    logging.info(f"Regular tax: {rtc.tax:.0f}")
    logging.info(f"Other taxes: {(rtc.additional_medicare_tax + rtc.net_investment_income_tax):.0f}")
    logging.info(f"    Additional medicare tax: {rtc.additional_medicare_tax:.0f}")
    logging.info(f"    Net investment income tax: {rtc.net_investment_income_tax:.0f}")

    logging.info(RED + "========== AMT Tax ==========" + ENDC)
    atc = AMTTaxComputer(**params)
    logging.info(f"Taxable income: {atc.taxable_income:.0f}")
    logging.info(f"Exemption: {atc.exemption:.0f}")
    logging.info(f"AMT tax: {atc.tax:.0f}")

    logging.info(BLUE + "========== State Tax ==========" + ENDC)
    stc = StateTaxComputer(**params)
    logging.info(f"CA adjusted AGI: {stc.ca_adjusted_agi:.0f}")
    logging.info(f"Taxable income: {stc.taxable_income:.0f}")
    logging.info(f"Exemption: {stc.exemption:.0f}")
    logging.info(f"State tax: {stc.tax:.0f}")
    logging.info(f"Mental health services tax: {stc.mental_health_services_tax:.0f}")

    if args.extrapolate:
        deltas = range(0, 200001, 10000)
        item = 'capital_gain'
        regular_taxes = [RegularTaxComputer(
            **dict(params, **{
                item: params[item] + delta,
                'long_term_capital_gain':
                    params['long_term_capital_gain'] + delta,
            })).tax for delta in deltas]
        amt_taxes = [AMTTaxComputer(
            **dict(params, **{
                item: params[item] + delta,
                'long_term_capital_gain':
                    params['long_term_capital_gain'] + delta,
            })).tax for delta in deltas]

        fig, ax = plt.subplots()
        ax.plot(deltas, regular_taxes, 'bo-', label='Regular Tax')
        ax.plot(deltas, amt_taxes, 'rs--', label='AMT Tax')
        actual_tax = max(
            rtc.get_tax(), atc.get_tax())
        ax.plot(0, actual_tax,
                'y*', markersize=20, label='Actual Tax')
        legend = ax.legend(loc='upper center', shadow=True)
        plt.grid(True)
        plt.show()

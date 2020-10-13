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

    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    C = '\033[36m'
    E = '\033[0m'

    logging.info(G + "========== Regular Tax ==========" + E)
    rtc = RegularTaxComputer(**params)
    logging.info(f"W2: {rtc.w2:.0f}")
    logging.info(f"Interest: {rtc.interests:.0f}")
    logging.info(f"Dividends: {rtc.dividends:.0f}")
    logging.info(f"    Qualified dividends: {rtc.qualified_dividends:.0f}")
    logging.info(f"IRA distributions: {rtc.roth_conversion_gain:.0f}")
    logging.info(f"Capital gain: {rtc.capital_gain:.0f}")
    other_income = (rtc.taxable_state_refund + rtc.rental_income_offset + rtc.misc_income)
    logging.info(f"Other income: {other_income:.0f}")
    logging.info(f"    Taxable state refunds: {rtc.taxable_state_refund:.0f}")
    logging.info(f"    Rental income: {rtc.rental_income_offset:.0f} ({rtc.rental_income:.0f} - {rtc.rental_loss_carryover:.0f})")
    logging.info(f"    Misc income: {rtc.misc_income:.0f}")
    logging.info(f"AGI: {rtc.agi:.0f}")
    logging.info(f"Itemized deduction: {rtc.itemized_deduction:.0f}")
    logging.info(f"QBI: {rtc.qualified_business_income:.0f}")
    logging.info(f"Taxable income: {rtc.taxable_income:.0f}")
    logging.info(f"Exemption: {rtc.exemption:.0f}")
    logging.info(G + f"Regular tax: {rtc.tax:.0f}" + E)
    logging.info(f"Other taxes: {(rtc.additional_medicare_tax + rtc.net_investment_income_tax):.0f}")
    logging.info(G + f"    Additional medicare tax: {rtc.additional_medicare_tax:.0f}" + E)
    logging.info(G + f"    Net investment income tax: {rtc.net_investment_income_tax:.0f}" + E)

    logging.info(R + "========== AMT Tax ==========" + E)
    atc = AMTTaxComputer(**params)
    logging.info(f"Taxable income: {atc.taxable_income:.0f}")
    logging.info(f"Itemized deduction: {atc.itemized_deduction:.0f}")
    logging.info(f"Exemption: {atc.exemption:.0f}")
    logging.info(R + f"AMT tax: {max(0, atc.tax - rtc.tax):.0f} ({(atc.tax - atc.credits):.0f})" + E)

    logging.info(f"Federal tax withheld {rtc.tax_withheld:.0f}")
    logging.info(C + f"Fedaral tax due: {(max(rtc.tax, atc.tax) + rtc.additional_medicare_tax + rtc.net_investment_income_tax - rtc.credits - rtc.tax_withheld + rtc.penalty):.0f}" + E)

    logging.info(Y + "========== State Tax ==========" + E)
    stc = StateTaxComputer(**params)
    logging.info(f"CA adjusted AGI: {stc.ca_adjusted_agi:.0f}")
    logging.info(f"Itemized deduction: {stc.itemized_deduction:.0f}")
    logging.info(f"Taxable income: {stc.taxable_income:.0f}")
    logging.info(f"Exemption: {stc.exemption:.0f}")
    logging.info(Y + f"State tax: {stc.tax:.0f}" + E)
    logging.info(Y + f"Mental health services tax: {stc.mental_health_services_tax:.0f}" + E)
    logging.info(f"State tax withheld {stc.tax_withheld:.0f}")
    logging.info(C + f"State tax due: {(stc.tax + stc.mental_health_services_tax - stc.tax_withheld):.0f}" + E)

    if args.extrapolate:
        deltas = range(0, 200001, 10000)
        regular_taxes = []
        amt_taxes = []
        for delta in deltas:
            rtc2 = RegularTaxComputer(**params)
            rtc2.long_term_capital_gain = rtc.long_term_capital_gain + delta
            regular_taxes.append(rtc2.tax)
            atc2 = AMTTaxComputer(**params)
            atc2.long_term_capital_gain = rtc.long_term_capital_gain + delta
            amt_taxes.append(atc2.tax)

        fig, ax = plt.subplots()
        ax.plot(deltas, regular_taxes, 'bo-', label='Regular Tax')
        ax.plot(deltas, amt_taxes, 'rs--', label='AMT Tax')
        actual_tax = max(rtc.tax, atc.tax)
        ax.plot(0, actual_tax,
                'y*', markersize=20, label='Actual Tax')
        legend = ax.legend(loc='upper center', shadow=True)
        plt.grid(True)
        plt.show()

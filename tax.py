from __future__ import division
from __future__ import print_function
from abc import ABCMeta, abstractmethod

import argparse
import importlib
import logging
import math
import matplotlib.pyplot as plt
import sys


class TaxComputer:
    __metaclass__ = ABCMeta

    def __init__(self, year, w2, w2_for_medicare,
                 state_income_tax, casdi=0,
                 state_tax_previous_year=0, car_registration=0,
                 interest=0, other_interest=0,
                 dividends=0, qualified_dividends=0, unrecaptured_1250_gain=0,
                 roth_conversion_gain=0, state_refund=0,
                 capital_gain=0, long_term_capital_gain=0,
                 rental_income=0, qbi = 0, investment_income_modification=0,
				 other_income=0, hsa=0,
                 primary_home_property_tax=0, other_taxes=0,
                 primary_home_interest=0, gifts=0, credits = 0,
                 *args, **kwargs):

        self.year = year
        self.w2 = w2
        self.w2_for_medicare = w2_for_medicare
        self.state_income_tax = state_income_tax
        self.casdi = casdi
        self.state_tax_previous_year = state_tax_previous_year
        self.car_registration = car_registration
        self.interest = interest
        self.other_interest = other_interest
        self.dividends = dividends
        self.qualified_dividends = qualified_dividends
        self.unrecaptured_1250_gain = unrecaptured_1250_gain
        self.roth_conversion_gain = roth_conversion_gain
        self.state_refund = state_refund
        self.capital_gain = capital_gain
        self.long_term_capital_gain = long_term_capital_gain
        self.rental_income = rental_income
        self.qbi = qbi
        self.investment_income_modification = investment_income_modification
        self.other_income = other_income
        self.hsa = hsa
        self.primary_home_property_tax = primary_home_property_tax
        self.other_taxes = other_taxes
        self.primary_home_interest = primary_home_interest
        self.gifts = gifts
        self.credits = credits

        self.state_local_income_taxes = (
            self.state_income_tax +
            self.casdi +
            self.state_tax_previous_year)
        logging.debug("state_local_income_taxes = {}".format(self.state_local_income_taxes))

        self.investment_income = (
            self.interest +
            self.dividends +
            self.capital_gain +
            self.rental_income)
        logging.debug("investment_income = {:.0f}".format(self.investment_income))

        self.agi = (
            self.w2 +
            self.investment_income +
            self.roth_conversion_gain +
            self.state_refund +
            self.other_income)
        logging.debug("agi = {:.0f}".format(self.agi))

        self.exemption = None
        self.taxable_income = None
        self.tax = None

    @abstractmethod
    def get_exemption(self):
        pass

    @abstractmethod
    def get_taxable_income(self):
        pass

    @abstractmethod
    def get_tax(self):
        pass

    @staticmethod
    def _apply_tax_brackets(brackets, taxable_income):
        tax = 0
        for boundary, taxrate in reversed(brackets):
            if taxable_income > boundary:
                overamount = taxable_income - boundary
                tax += overamount * taxrate
                logging.debug(
                        "applying tax rate {} to {}-{}: {:.0f} cumulative".format(
                        taxrate, taxable_income, boundary, tax))
                taxable_income -= overamount
        return tax

    @staticmethod
    def _get_qdcg_tax(thresholds, taxable_income, qdcg):
        tax = 0
        remaining_qdcg = min(taxable_income, qdcg)
        for threshold in thresholds:
            limit = max(0, taxable_income - threshold[0])
            qualified_qdcg = max(0, remaining_qdcg - limit)
            tax += qualified_qdcg * threshold[1]
            logging.debug(
                    "applying tax rate {} to {}-{}: {:.0f} cumulative".format(
                    threshold[1], remaining_qdcg, limit, tax))
            remaining_qdcg -= qualified_qdcg
            if remaining_qdcg == 0:
                break
        return tax

    def _compute_tax_with_qdcg(self, taxable_income):
        brackets = self.TAX_BRACKETS[self.year]
        tax = self._apply_tax_brackets(brackets, taxable_income)
        logging.debug("tax: {:.0f}".format(tax))

        qdcg_thresholds = self.QDCG_THRESHOLDS[self.year]
        qdcg = self.qualified_dividends
        if self.capital_gain > 0 and self.long_term_capital_gain > 0:
            qdcg += min(self.capital_gain, self.long_term_capital_gain)
        qdcg -= self.unrecaptured_1250_gain
        taxable_income -= self.unrecaptured_1250_gain
        if qdcg > 0:
            tax_qdcg = (
                self._apply_tax_brackets(brackets,
                                         max(0, taxable_income - qdcg)) +
                self._get_qdcg_tax(qdcg_thresholds, taxable_income, qdcg))
            unrecaptured_1250_tax = self.unrecaptured_1250_gain * 0.25
            logging.debug("applying tax rate {} to {}: {:.0f}".format(
                self.UNRECAPTURED_1250_TAX_RATE,
                self.unrecaptured_1250_gain,
                unrecaptured_1250_tax))
            tax_qdcg += unrecaptured_1250_tax
            logging.debug("tax_qdcg: {:.0f}".format(tax_qdcg))
            tax = min(tax, tax_qdcg)

        return tax


class RegularTaxComputer(TaxComputer):

    TAX_BRACKETS = {
        2012: [
            (0, 0.1),
            (8700, 0.15),
            (35350, 0.25),
            (85650, 0.28),
            (178650, 0.33),
            (388350, 0.35)],
        2013: [
            (0, 0.1),
            (8925, 0.15),
            (36250, 0.25),
            (87850, 0.28),
            (183250, 0.33),
            (398350, 0.35),
            (400000, 0.396)],
        2014: [
            (0, 0.1),
            (9075, 0.15),
            (36900, 0.25),
            (89350, 0.28),
            (186350, 0.33),
            (405100, 0.35),
            (406750, 0.396)],
        2015: [
            (0, 0.1),
            (9225, 0.15),
            (37450, 0.25),
            (90750, 0.28),
            (189300, 0.33),
            (411500, 0.35),
            (413200, 0.396)],
        2016: [
            (0, 0.1),
            (9275, 0.15),
            (37650, 0.25),
            (91150, 0.28),
            (190150, 0.33),
            (413350, 0.35),
            (415050, 0.396)],
        2017: [
            (0, 0.1),
            (9325, 0.15),
            (37950, 0.25),
            (91900, 0.28),
            (191650, 0.33),
            (416700, 0.35),
            (418400, 0.396)],
        2018: [
            (0, 0.1),
            (9525, 0.12),
            (38700, 0.22),
            (82500, 0.24),
            (157500, 0.32),
            (200000, 0.35),
            (500000, 0.37)],
    }

    QDCG_THRESHOLDS = {
        2012: [
            (35350, 0),
            (sys.maxsize, 0.15)],
        2013: [
            (36250, 0),
            (400000, 0.15),
            (sys.maxsize, 0.2)],
        2014: [
            (36900, 0),
            (406750, 0.15),
            (sys.maxsize, 0.2)],
        2015: [
            (37450, 0),
            (413200, 0.15),
            (sys.maxsize, 0.2)],
        2016: [
            (37650, 0),
            (415050, 0.15),
            (sys.maxsize, 0.2)],
        2017: [
            (37950, 0),
            (418400, 0.15),
            (sys.maxsize, 0.2)],
        2018: [
            (38600, 0),
            (425800, 0.15),
            (sys.maxsize, 0.2)],
    }

    UNRECAPTURED_1250_TAX_RATE = 0.25

    def get_exemption(self):
        exemption_threshold = {
            2012: (sys.maxsize, 3800),
            2013: (250000, 3900),
            2014: (254200, 3950),
            2015: (258250, 4000),
            2016: (259400, 4050),
            2017: (261500, 4050),
            2018: (sys.maxsize, 0),
        }

        if self.exemption is not None:
            return self.exemption

        excess = max(0, self.agi - exemption_threshold[self.year][0])
        logging.debug("excess = {}".format(excess))
        self.exemption = (
            exemption_threshold[self.year][1] *
            (1 - min(1, math.ceil(excess / 2500) * 0.02)))
        return self.exemption

    def get_taxable_income(self):
        itemized_deduction_limit_threshold_on_agi = {
            2012: sys.maxsize,
            2013: 250000,
            2014: 254200,
            2015: 258250,
            2016: 259400,
            2017: 261500,
            2018: sys.maxsize,
        }
        standard_deduction = {
            2012: 5950,
            2013: 6100,
            2014: 6200,
            2015: 6300,
            2016: 6300,
            2017: 6350,
            2018: 12000,
        }

        if self.taxable_income is not None:
            return self.taxable_income

        state_local_taxes = (
            self.state_local_income_taxes +
            self.primary_home_property_tax +
            self.car_registration)
        if self.year >= 2018 and state_local_taxes > 10000:
            logging.debug("state_local_taxes = {}, but limited to 10000".format(
                state_local_taxes))
            state_local_taxes = 10000
        tentative_deduction = (
            state_local_taxes +
            self.other_taxes +
            self.primary_home_interest +
            self.gifts)
        logging.debug("tentative_deduction = {}".format(tentative_deduction))
        limit = min(
            0.03 * max(
                0,
                self.agi - itemized_deduction_limit_threshold_on_agi[self.year]
            ),
            tentative_deduction * 0.8,
        )
        logging.debug("limit = {:.0f}".format(limit))
        itemized_deduction = tentative_deduction - limit
        logging.debug("itemized_deduction = {:.0f}".format(itemized_deduction))
        logging.debug("standard_deduction = {}".format(
            standard_deduction[self.year]))

        self.taxable_income = max(
            0,
            self.agi - max(standard_deduction[self.year], itemized_deduction)
        )
        if self.year >= 2018:
            self.taxable_income -= self.qbi
        return self.taxable_income

    def get_tax(self):
        taxable_income = self.get_taxable_income()
        exemption = self.get_exemption()
        tax = self._compute_tax_with_qdcg(max(0, taxable_income - exemption))
        return tax

    def get_additional_medicare_tax(self):
        threshold_on_w2 = 200000
        taxrate = 0.009
        overamount = max(0, self.w2_for_medicare - threshold_on_w2)
        tax = taxrate * overamount
        logging.debug("applying tax rate {} to {}-{}: {:.0f}".format(
            taxrate, self.w2_for_medicare, threshold_on_w2, tax))
        return tax

    def get_net_investment_income_tax(self):
        threshold_on_agi = 200000
        taxrate = 0.038
        investment_income = (
            self.investment_income +
            self.investment_income_modification)
        taxable_investment = (
            investment_income * (1 - self.state_local_income_taxes / self.agi))
        logging.debug("taxable investment: {:.0f}".format(taxable_investment))
        overamount = max(0, self.agi - threshold_on_agi)
        tax = taxrate * min(taxable_investment, overamount)
        logging.debug("applying tax rate {} to min({:.0f}, {}-{}): {:.0f}".format(
            taxrate, taxable_investment, self.agi, threshold_on_agi, tax))
        return tax


class AMTTaxComputer(TaxComputer):

    TAX_BRACKETS = {
        2012: [
            (0, 0.26),
            (175000, 0.28)],
        2013: [
            (0, 0.26),
            (179500, 0.28)],
        2014: [
            (0, 0.26),
            (182500, 0.28)],
        2015: [
            (0, 0.26),
            (185400, 0.28)],
        2016: [
            (0, 0.26),
            (186300, 0.28)],
        2017: [
            (0, 0.26),
            (187800, 0.28)],
        2018: [
            (0, 0.26),
            (191500, 0.28)],
    }

    QDCG_THRESHOLDS = RegularTaxComputer.QDCG_THRESHOLDS

    UNRECAPTURED_1250_TAX_RATE = RegularTaxComputer.UNRECAPTURED_1250_TAX_RATE

    def get_exemption(self):
        exemption_threshold = {
            2012: (112500, 50600),
            2013: (115400, 51900),
            2014: (117300, 52800),
            2015: (119200, 53600),
            2016: (119700, 53900),
            2017: (120700, 54300),
            2018: (500000, 70300),
        }

        if self.exemption is not None:
            return self.exemption

        taxable_income = self.get_taxable_income()
        excess = max(0, taxable_income - exemption_threshold[self.year][0])
        logging.debug("excess = {}".format(excess))
        self.exemption = max(
            0, exemption_threshold[self.year][1] - excess * 0.25)
        return self.exemption

    def get_taxable_income(self):
        if self.taxable_income is not None:
            return self.taxable_income

        tentative_deduction = (
            self.primary_home_interest +
            self.gifts)
        logging.debug("tentative_deduction = {}".format(tentative_deduction))
        self.taxable_income = max(
            0,
            self.agi -
            self.state_refund -
            tentative_deduction +
            self.other_interest
        )
        return self.taxable_income

    def get_tax(self):
        taxable_income = self.get_taxable_income()
        exemption = self.get_exemption()
        tax = self._compute_tax_with_qdcg(max(0, taxable_income - exemption))
        tax -= self.credits
        return tax


class StateTaxComputer(TaxComputer):

    TAX_BRACKETS = {
        2012: [
            (0, 0.01),
            (7455, 0.02),
            (17676, 0.04),
            (27897, 0.06),
            (38726, 0.08),
            (48942, 0.093),
            (250000, 0.103),
            (300000, 0.113),
            (500000, 0.123)],
        2013: [
            (0, 0.01),
            (7582, 0.02),
            (17976, 0.04),
            (28371, 0.06),
            (39384, 0.08),
            (49774, 0.093),
            (254250, 0.103),
            (305100, 0.113),
            (508500, 0.123)],
        2014: [
            (0, 0.01),
            (7749, 0.02),
            (18371, 0.04),
            (28995, 0.06),
            (40250, 0.08),
            (50869, 0.093),
            (259844, 0.103),
            (311812, 0.113),
            (519687, 0.123)],
        2015: [
            (0, 0.01),
            (7850, 0.02),
            (18610, 0.04),
            (29372, 0.06),
            (40773, 0.08),
            (51530, 0.093),
            (263222, 0.103),
            (315866, 0.113),
            (526443, 0.123)],
        2016: [
            (0, 0.01),
            (8015, 0.02),
            (19001, 0.04),
            (29989, 0.06),
            (41629, 0.08),
            (52612, 0.093),
            (268750, 0.103),
            (322499, 0.113),
            (537498, 0.123)],
        2017: [
            (0, 0.01),
            (8223, 0.02),
            (19495, 0.04),
            (30769, 0.06),
            (42711, 0.08),
            (53980, 0.093),
            (275738, 0.103),
            (330884, 0.113),
            (551473, 0.123)],
        2018: [
            (0, 0.01),
            (8544, 0.02),
            (20255, 0.04),
            (31969, 0.06),
            (44377, 0.08),
            (56085, 0.093),
            (286492, 0.103),
            (343788, 0.113),
            (572980, 0.123)],
    }

    def get_exemption(self):
        exemption_threshold = {
            2012: (169730, 104),
            2013: (172615, 106),
            2014: (176413, 108),
            2015: (178706, 109),
            2016: (182459, 111),
            2017: (187203, 114),
            2018: (194504, 118),
        }

        if self.exemption is not None:
            return self.exemption

        excess = max(0, self.agi - exemption_threshold[self.year][0])
        self.exemption = max(
            0,
            exemption_threshold[self.year][1] - math.ceil(excess / 2500) * 6)
        return self.exemption

    def get_taxable_income(self):
        itemized_deduction_limit_threshold_on_agi = {
            2012: 169730,
            2013: 172615,
            2014: 176413,
            2015: 178706,
            2016: 182459,
            2017: 187203,
            2018: 194504,
        }
        standard_deduction = {
            2012: 3841,
            2013: 3906,
            2014: 3992,
            2015: 4044,
            2016: 4129,
            2017: 4236,
            2018: 4401,
        }

        if self.taxable_income is not None:
            return self.taxable_income

        state_agi = self.agi - self.state_refund + self.hsa
        tentative_deduction = (
            self.primary_home_property_tax +
            self.car_registration +
            self.other_taxes +
            self.primary_home_interest +
            self.gifts
        )
        logging.debug("tentative_deduction = {}".format(tentative_deduction))
        limit = min(
            0.06 * max(
                0,
                self.agi - itemized_deduction_limit_threshold_on_agi[self.year]
            ),
            tentative_deduction * 0.8,
        )
        logging.debug("limit = {:.0f}".format(limit))
        itemized_deduction = tentative_deduction - limit
        logging.debug("itemized_deduction = {:.0f}".format(itemized_deduction))
        logging.debug("standard_deduction = {}".format(
            standard_deduction[self.year]))
        self.taxable_income = max(
            0,
            state_agi - max(standard_deduction[self.year], itemized_deduction)
        )
        return self.taxable_income

    def get_tax(self):
        taxable_income = self.get_taxable_income()
        brackets = self.TAX_BRACKETS[self.year]
        tax = self._apply_tax_brackets(brackets, taxable_income)
        exemption = self.get_exemption()
        return max(0, tax - exemption)

    def get_mental_health_services_tax(self):
        threshold = 1000000
        taxrate = 0.01
        overamount = max(0, self.get_taxable_income() - threshold)
        tax = taxrate * overamount
        logging.debug("applying tax rate {} to {}-{}: {:.0f}".format(
            taxrate, self.get_taxable_income(), threshold, tax))
        return tax


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

    logging.info("========== Regular Tax ==========")
    regular_tax_computer = RegularTaxComputer(**params)
    logging.info("Taxable Income: {:.0f}".format(
        regular_tax_computer.get_taxable_income()))
    logging.info("Exemption: {:.0f}".format(
        regular_tax_computer.get_exemption()))
    logging.info(GREEN + "Regular Tax: {:.0f}".format(
        regular_tax_computer.get_tax()) + ENDC)
    additional_medicare_tax = \
        regular_tax_computer.get_additional_medicare_tax()
    logging.info(BLUE + "Additional Medicare Tax: {:.0f}".format(
        additional_medicare_tax) + ENDC)
    net_investment_income_tax = \
        regular_tax_computer.get_net_investment_income_tax()
    logging.info(BLUE + "Net Investment Income Tax: {:.0f}".format(
        net_investment_income_tax) + ENDC)

    logging.info("========== AMT Tax ==========")
    amt_tax_computer = AMTTaxComputer(**params)
    logging.info("Taxable Income: {:.0f}".format(
        amt_tax_computer.get_taxable_income()))
    logging.info("Exemption: {:.0f}".format(
        amt_tax_computer.get_exemption()))
    logging.info(RED + "AMT Tax: {:.0f}".format(
        amt_tax_computer.get_tax()) + ENDC)

    logging.info("========== State Tax ==========")
    state_tax_computer = StateTaxComputer(**params)
    logging.info("Taxable Income: {:.0f}".format(
        state_tax_computer.get_taxable_income()))
    logging.info("Exemption: {:.0f}".format(
        state_tax_computer.get_exemption()))
    logging.info(CYAN + "State Tax: {:.0f}\n".format(
        state_tax_computer.get_tax()) + ENDC)
    mental_health_services_tax = \
        state_tax_computer.get_mental_health_services_tax()
    logging.info(CYAN + "Mental Health Services Tax: {:.0f}".format(
        mental_health_services_tax) + ENDC)

    if args.extrapolate:
        deltas = range(0, 200001, 10000)
        item = 'capital_gain'
        regular_taxes = [RegularTaxComputer(
            **dict(params, **{
                item: params[item] + delta,
                'long_term_capital_gain':
                    params['long_term_capital_gain'] + delta,
            })).get_tax() for delta in deltas]
        amt_taxes = [AMTTaxComputer(
            **dict(params, **{
                item: params[item] + delta,
                'long_term_capital_gain':
                    params['long_term_capital_gain'] + delta,
            })).get_tax() for delta in deltas]

        fig, ax = plt.subplots()
        ax.plot(deltas, regular_taxes, 'bo-', label='Regular Tax')
        ax.plot(deltas, amt_taxes, 'rs--', label='AMT Tax')
        actual_tax = max(
            regular_tax_computer.get_tax(), amt_tax_computer.get_tax())
        ax.plot(0, actual_tax,
                'y*', markersize=20, label='Actual Tax')
        legend = ax.legend(loc='upper center', shadow=True)
        plt.grid(True)
        plt.show()

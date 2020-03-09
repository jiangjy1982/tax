from functools import cached_property

import logging
import math

from tax_computer import TaxComputer
from federal_tax_table import regular_tax_table, amt_tax_table


class FederalTaxComputer(TaxComputer):

    UNRECAPTURED_1250_TAX_RATE = 0.25

    @cached_property
    def state_local_income_taxes(self):
        return (
            self.state_income_tax
            + self.casdi
            + self.state_tax_previous_year)


    def compute_tax_with_qdcg(self, taxable_income):

        def _get_qdcg_tax(thresholds, taxable_income, qdcg):
            tax = 0
            remaining_qdcg = min(taxable_income, qdcg)
            for threshold in thresholds:
                limit = max(0, taxable_income - threshold[0])
                qualified_qdcg = max(0, remaining_qdcg - limit)
                tax += qualified_qdcg * threshold[1]
                logging.debug(
                    f"applying {threshold[1]} to {remaining_qdcg}-{limit}: {tax:.0f} cumulative")
                remaining_qdcg -= qualified_qdcg
                if remaining_qdcg == 0:
                    break
            return tax

        tax = self.apply_tax_brackets(self.params.brackets, taxable_income)
        logging.debug(f"tax: {tax:.0f}")

        qdcg = self.qualified_dividends
        if self.capital_gain > 0 and self.long_term_capital_gain > 0:
            qdcg += min(self.capital_gain, self.long_term_capital_gain)
        qdcg -= self.unrecaptured_1250_gain
        taxable_income -= self.unrecaptured_1250_gain
        if qdcg > 0:
            tax_qdcg = (
                self.apply_tax_brackets(self.params.brackets, max(0, taxable_income - qdcg))
                + _get_qdcg_tax(self.params.qdcg_thresholds, taxable_income, qdcg))
            unrecaptured_1250_tax = self.unrecaptured_1250_gain * self.UNRECAPTURED_1250_TAX_RATE
            logging.debug(
                f"applying {self.UNRECAPTURED_1250_TAX_RATE} to {self.unrecaptured_1250_gain}: {unrecaptured_1250_tax:.0f}")
            tax_qdcg += unrecaptured_1250_tax
            logging.debug(f"tax_qdcg: {tax_qdcg:.0f}")
            tax = min(tax, tax_qdcg)

        return tax


class RegularTaxComputer(FederalTaxComputer):

    @cached_property
    def params(self):
        return regular_tax_table[self.year]


    @cached_property
    def exemption(self):
        excess = max(0, self.agi - self.params.limit_threshold)
        logging.debug(f"excess = {excess}")
        return self.params.exemption * (1 - min(1, math.ceil(excess / 2500) * 0.02))


    @cached_property
    def taxable_income(self):
        state_local_taxes = (
            self.state_local_income_taxes
            + self.primary_home_property_tax
            + self.car_registration)
        if self.year >= 2018 and state_local_taxes > 10000:
            state_local_taxes = 10000

        tentative_deduction = (
            state_local_taxes
            + self.other_taxes
            + self.primary_home_interest
            + self.gifts)

        logging.debug(f"tentative_deduction = {tentative_deduction}")
        logging.debug(f"    state_local_taxes = {state_local_taxes}")
        logging.debug(f"        state_local_income_taxes = {self.state_local_income_taxes}")
        logging.debug(f"        primary_home_property_tax = {self.primary_home_property_tax}")
        logging.debug(f"        car_registration = {self.car_registration}")
        logging.debug(f"    other_taxes = {self.other_taxes}")
        logging.debug(f"    primary_home_interest = {self.primary_home_interest}")
        logging.debug(f"    gifts = {self.gifts}")

        limit = min(
            0.03 * max(0, self.agi - self.params.limit_threshold),
            tentative_deduction * 0.8,
        )
        logging.debug(f"limit = {limit:.0f}")
        itemized_deduction = tentative_deduction - limit
        logging.debug(f"itemized_deduction = {itemized_deduction:.0f}")
        logging.debug(f"standard_deduction = {self.params.standard_deduction}")

        taxable_income = max(
            0, self.agi - max(self.params.standard_deduction, itemized_deduction)
        )
        if self.year >= 2018:
            taxable_income -= self.qbi

        return taxable_income


    @cached_property
    def tax(self):
        return self.compute_tax_with_qdcg(max(0, self.taxable_income - self.exemption))


    @cached_property
    def additional_medicare_tax(self):
        threshold_on_w2 = 200000
        taxrate = 0.009

        tax = taxrate * max(0, self.w2_for_medicare - threshold_on_w2)
        logging.debug(f"applying {taxrate} to {self.w2_for_medicare}-{threshold_on_w2}: {tax:.0f}")
        return tax


    @cached_property
    def net_investment_income_tax(self):
        threshold_on_agi = 200000
        taxrate = 0.038

        investment_income = (
            self.interest
            + self.dividends
            + self.rental_income
            + self.capital_gain
            + self.investment_income_modification)
        logging.debug(f"investment_income: {investment_income:.0f}")
        logging.debug(f"    interest: {self.interest:.0f}")
        logging.debug(f"    dividends: {self.dividends:.0f}")
        logging.debug(f"    rental_income: {self.rental_income:.0f}")
        logging.debug(f"    capital_gain: {self.capital_gain:.0f}")
        logging.debug(f"    investment_income_modification: {self.investment_income_modification:.0f}")

        ratio = round(investment_income / self.agi, 4)
        allocable_state_local_income_taxes = self.state_local_income_taxes * ratio
        logging.debug(f"allocable_state_local_income_taxes: {allocable_state_local_income_taxes:.0f}")
        if self.year >= 2018 and allocable_state_local_income_taxes > 10000:
            allocable_state_local_income_taxes = 10000
            logging.debug("    BUT LIMITED TO 10000!")

        taxable_investment = investment_income - allocable_state_local_income_taxes
        logging.debug(f"taxable_investment: {taxable_investment:.0f}")
        tax = taxrate * min(taxable_investment, max(0, self.agi - threshold_on_agi))
        logging.debug(f"applying {taxrate} to min({taxable_investment:.0f}, {self.agi}-{threshold_on_agi}): {tax:.0f}")
        return tax


class AMTTaxComputer(FederalTaxComputer):

    @cached_property
    def params(self):
        return amt_tax_table[self.year]


    @cached_property
    def exemption(self):
        excess = max(0, self.taxable_income - self.params.limit_threshold)
        logging.debug(f"excess = {excess}")
        return max(0, self.params.exemption - excess * 0.25)


    @cached_property
    def taxable_income(self):
        tentative_deduction = (
            self.primary_home_interest
            + self.gifts)

        logging.debug(f"tentative_deduction = {tentative_deduction}")
        logging.debug(f"    primary_home_interest = {self.primary_home_interest}")
        logging.debug(f"    gifts = {self.gifts}")

        return max(
            0,
            self.agi
            - self.state_refund
            - tentative_deduction
            + self.other_interest
        )


    @cached_property
    def tax(self):
        tax = self.compute_tax_with_qdcg(max(0, self.taxable_income - self.exemption))
        tax -= self.credits
        return tax

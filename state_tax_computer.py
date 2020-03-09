from functools import cached_property

import logging
import math

from tax_computer import TaxComputer
from state_tax_table import state_tax_table


class StateTaxComputer(TaxComputer):

    @cached_property
    def ca_adjusted_agi(self):
        return (
            self.agi
            - self.state_refund
            + self.hsa
            - self.rental_loss_carryover)


    @cached_property
    def params(self):
        return state_tax_table[self.year]


    @cached_property
    def exemption(self):
        excess = max(0, self.agi - self.params.limit_threshold)
        logging.debug(f"excess = {excess}")
        return max(0, self.params.exemption - math.ceil(excess / 2500) * 6)


    @cached_property
    def taxable_income(self):
        tentative_deduction = (
            self.primary_home_property_tax +
            self.car_registration +
            self.other_taxes +
            self.primary_home_interest +
            self.gifts)
        logging.debug(f"tentative_deduction = {tentative_deduction}")
        limit = min(
            0.06 * max(0, self.agi - self.params.limit_threshold),
            tentative_deduction * 0.8,
        )
        logging.debug(f"limit = {limit:.0f}")
        itemized_deduction = tentative_deduction - limit
        logging.debug(f"itemized_deduction = {itemized_deduction:.0f}")
        logging.debug(f"standard_deduction = {self.params.standard_deduction}")
        taxable_income = max(
            0, self.ca_adjusted_agi - max(self.params.standard_deduction, itemized_deduction)
        )
        return taxable_income


    @cached_property
    def tax(self):
        tax = self.apply_tax_brackets(self.params.brackets, self.taxable_income)
        return max(0, tax - self.exemption)


    @cached_property
    def mental_health_services_tax(self):
        threshold = 1000000
        taxrate = 0.01

        tax = taxrate * max(0, self.taxable_income - threshold)
        logging.debug(f"applying {taxrate} to {self.taxable_income}-{threshold}: {tax:.0f}")
        return tax

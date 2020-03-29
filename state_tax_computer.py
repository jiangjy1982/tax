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
            - self.taxable_state_refund
            + self.hsa)


    @cached_property
    def params(self):
        return state_tax_table[self.year]


    @cached_property
    def exemption(self):
        excess = max(0, self.agi - self.params.limit_threshold)
        logging.debug(f"excess = {excess:.0f}")
        return max(0, self.params.exemption - math.ceil(excess / 2500) * 6)


    @cached_property
    def itemized_deduction(self):
        tentative_deduction = (
            self.primary_home_taxes +
            self.car_registration +
            self.other_taxes +
            self.primary_home_interests +
            self.gifts)
        logging.debug(f"tentative_deduction = {tentative_deduction:.0f}")
        logging.debug(f"    primary_home_taxes = {self.primary_home_taxes:.0f}")
        logging.debug(f"    car_registration = {self.car_registration:.0f}")
        logging.debug(f"    other_taxes = {self.other_taxes:.0f}")
        logging.debug(f"    primary_home_interests = {self.primary_home_interests:.0f}")
        logging.debug(f"    gifts = {self.gifts:.0f}")

        limit = min(
            0.06 * max(0, self.agi - self.params.limit_threshold),
            tentative_deduction * 0.8,
        )
        logging.debug(f"limit = {limit:.0f}")
        return tentative_deduction - limit


    @cached_property
    def taxable_income(self):
        return max(
            0,
            self.ca_adjusted_agi
            - max(self.params.standard_deduction, self.itemized_deduction)
        )


    @cached_property
    def tax(self):
        tax = self.apply_tax_brackets(self.params.brackets, self.taxable_income)
        return max(0, tax - self.exemption)


    @cached_property
    def mental_health_services_tax(self):
        threshold = 1000000
        taxrate = 0.01

        tax = taxrate * max(0, self.taxable_income - threshold)
        logging.debug(f"applying {taxrate} to {self.taxable_income:.0f}-{threshold}: {tax:.0f}")
        return tax


    @cached_property
    def excess_sdi_vpdi(self):
        return max(0,
            self.ca_sdi + self.ca_vpdi
            - self.params.ca_sdi_vpdi_taxrate * min(
                self.params.ca_sdi_vpdi_max_wage,
                self.state_wages))


    @cached_property
    def tax_withheld(self):
        return (
            self.state_income_tax_withheld
            + self.excess_sdi_vpdi
            + self.state_estimated_tax_paid_last_year
            + self.state_estimated_tax_paid_this_year)

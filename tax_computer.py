from abc import ABC, abstractmethod

import logging


class TaxComputer(ABC):

    CAPITAL_LOSS_LIMIT = -3000

    def __init__(self, year,
            w2, w2_for_medicare,
            state_income_tax, casdi=0,
            state_tax_previous_year=0, car_registration=0,
            interest=0, other_interest=0,
            dividends=0, qualified_dividends=0, unrecaptured_1250_gain=0,
            roth_conversion_gain=0, state_refund=0,
            capital_gain=0, long_term_capital_gain=0,
            rental_income_current=0, rental_loss_carryover=0, qbi=0,
            investment_income_modification=0,
            misc_income=0, hsa=0,
            primary_home_property_tax=0, other_taxes=0,
            primary_home_interest=0, gifts=0, credits=0,
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
        self.rental_income_current = rental_income_current
        self.rental_loss_carryover = rental_loss_carryover
        self.misc_income = misc_income
        self.qbi = qbi
        self.investment_income_modification = investment_income_modification
        self.hsa = hsa
        self.primary_home_property_tax = primary_home_property_tax
        self.other_taxes = other_taxes
        self.primary_home_interest = primary_home_interest
        self.gifts = gifts
        self.credits = credits

        self.capital_gain = max(self.capital_gain, self.CAPITAL_LOSS_LIMIT)
        self.rental_income = max(0, self.rental_income_current + self.rental_loss_carryover)
        self.other_income = self.state_refund + self.rental_income + self.misc_income
        self.agi = (
            self.w2
            + self.interest
            + self.dividends
            + self.roth_conversion_gain
            + self.capital_gain
            + self.other_income)


    @staticmethod
    def apply_tax_brackets(brackets, amount):
        tax = 0
        for boundary, taxrate in reversed(brackets):
            if amount > boundary:
                excess = amount - boundary
                tax += excess * taxrate
                logging.debug(
                        f"applying {taxrate} to {amount:.0f}-{boundary}: {tax:.0f} cumulative")
                amount -= excess
        return tax


    @abstractmethod
    def params(self):
        pass


    @abstractmethod
    def exemption(self):
        pass


    @abstractmethod
    def taxable_income(self):
        pass


    @abstractmethod
    def tax(self):
        pass

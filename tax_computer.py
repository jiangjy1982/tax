from abc import ABC, abstractmethod

import inspect
import logging


class TaxComputer(ABC):

    CAPITAL_LOSS_LIMIT = -3000

    def __init__(self,
            year,
            form_w2s,
            form_1099s,
            real_estates,
            capital_loss_carryover=0,
            rental_loss_carryover=0,
            investment_income_modification=0,
            state_tax_adjustments_last_year=0,
            car_registration=0,
            other_taxes=0,
            gifts=0,
            federal_estimated_tax_paid=0,
            state_estimated_tax_paid_last_year=0,
            state_estimated_tax_paid_this_year=0,
            penalty=0,
            *args, **kwargs):

        self.year = year

        self.w2 = sum([w2.wages for w2 in form_w2s])
        self.federal_income_tax_withheld = sum(
            [w2.federal_income_tax_withheld for w2 in form_w2s]
            + [f1099.federal_income_tax_withheld for f1099 in form_1099s])
        self.social_security_wages = sum([w2.social_security_wages for w2 in form_w2s])
        self.social_security_tax_withheld = sum([w2.social_security_tax_withheld for w2 in form_w2s])
        self.medicare_wages = sum([w2.medicare_wages for w2 in form_w2s])
        self.medicare_tax_withheld = sum([w2.medicare_tax_withheld for w2 in form_w2s])
        self.hsa = sum([w2.hsa for w2 in form_w2s])
        self.ca_sdi = sum([w2.ca_sdi for w2 in form_w2s])
        self.ca_vpdi = sum([w2.ca_vpdi for w2 in form_w2s])
        self.state_wages = sum([w2.state_wages for w2 in form_w2s])
        self.state_income_tax_withheld = sum([w2.state_income_tax_withheld for w2 in form_w2s])

        self.interests = sum([f1099.interests for f1099 in form_1099s])
        self.dividends = sum([f1099.dividends for f1099 in form_1099s])
        self.qualified_dividends = sum([f1099.qualified_dividends for f1099 in form_1099s])
        self.unrecaptured_1250_gain = sum([f1099.unrecaptured_1250_gain for f1099 in form_1099s])
        self.section_199A_dividends = sum([f1099.section_199A_dividends for f1099 in form_1099s])
        self.foreign_tax_paid = sum([f1099.foreign_tax_paid for f1099 in form_1099s])
        self.private_activity_bond_interest_dividends = sum([f1099.private_activity_bond_interest_dividends for f1099 in form_1099s])
        self.short_term_capital_gain = sum([f1099.short_term_capital_gain for f1099 in form_1099s])
        self.long_term_capital_gain = sum([f1099.long_term_capital_gain + f1099.capital_gain_distributions
            for f1099 in form_1099s])
        self.misc_income = sum([f1099.misc for f1099 in form_1099s])
        self.roth_conversion_gain = sum([f1099.roth_conversion_gain for f1099 in form_1099s])

        primary_homes = [r for r in real_estates if r.is_primary]
        self.primary_home_taxes = sum([rs.taxes for rs in primary_homes])
        self.primary_home_interests = sum([rs.interests for rs in primary_homes])

        rentals = [r for r in real_estates if not r.is_primary]
        self.rental_incomes = [(
            r.id,
            r.rents - sum(getattr(r, a) for a in r._fields if a not in ('id', 'is_primary', 'rents')))
            for r in rentals]
        self.rental_income = sum([ri[1] for ri in self.rental_incomes])

        self.capital_loss_carryover = capital_loss_carryover
        self.rental_loss_carryover = rental_loss_carryover
        self.investment_income_modification = investment_income_modification
        self.taxable_state_refund = max(0, -state_tax_adjustments_last_year)
        self.state_tax_due_last_year = max(0, state_tax_adjustments_last_year)
        self.car_registration = car_registration
        self.other_taxes = other_taxes
        self.gifts = gifts
        self.federal_estimated_tax_paid = federal_estimated_tax_paid
        self.state_estimated_tax_paid_last_year = state_estimated_tax_paid_last_year
        self.state_estimated_tax_paid_this_year = state_estimated_tax_paid_this_year
        self.penalty = penalty

        self.capital_gain = max(
            self.CAPITAL_LOSS_LIMIT,
            self.short_term_capital_gain
            + self.long_term_capital_gain
            - self.capital_loss_carryover)
        self.rental_income_offset = max(
            0,
            self.rental_income
            - self.rental_loss_carryover)
        self.agi = (
            self.w2
            + self.interests
            + self.dividends
            + self.capital_gain
            + self.misc_income
            + self.rental_income_offset
            + self.taxable_state_refund
            + self.roth_conversion_gain)


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

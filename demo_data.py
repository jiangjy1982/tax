from defs import FormW2, Form1099, RealEstate


year = 2019

form_w2s = [
    FormW2(
        id='Company',
        wages=1000,
        federal_income_tax_withheld=0,
        social_security_wages=0,
        social_security_tax_withheld=0,
        medicare_wages=0,
        medicare_tax_withheld=0,
        ca_sdi=0,
        state_wages=0,
        state_income_tax_withheld=0,
    ),
]

form_1099s = [
    Form1099(
        id='Bank',
        dividends=100,
        qualified_dividends=0,
        section_199A_dividends=0,
        short_term_capital_gain=500,
        long_term_capital_gain=5000,
        misc=0,
    ),
]

real_estates = [
    RealEstate(
        id='Primary',
        is_primary=True,
        taxes=10000,
        interests=5000,
    ),
    RealEstate(
        id='Rental',
        rents=20000,
        taxes=10000,
        interests=10000,
        insurance=1000,
        management=0,
        repairs=0,
        utilities=0,
        depreciation=3000,
        other=0,
    ),
]

capital_loss_carryover = 0
rental_loss_carryover = 0
state_tax_adjustments_last_year = 0
car_registration = 0
gifts = 0

federal_estimated_tax_paid = 0
state_estimated_tax_paid_last_year = 0
state_estimated_tax_paid_this_year = 0

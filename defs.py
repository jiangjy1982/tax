from collections import namedtuple


fields_w2 = (
    'id',
    'wages',
    'federal_income_tax_withheld',
    'social_security_wages',
    'social_security_tax_withheld',
    'medicare_wages',
    'medicare_tax_withheld',
    'hsa',
    'ca_sdi',
    'ca_vpdi',
    'state_wages',
    'state_income_tax_withheld',
)
FormW2 = namedtuple(
    'FormW2',
    fields_w2,
    defaults=('',) + (0,) * len(fields_w2[1:]))


fields_1099 = (
    'id',
    'interests',
    'dividends',
    'qualified_dividends',
    'capital_gain_distributions',
    'unrecaptured_1250_gain',
    'federal_income_tax_withheld',
    'section_199A_dividends',
    'foreign_tax_paid',
    'private_activity_bond_interest_dividends',
    'short_term_capital_gain',
    'long_term_capital_gain',
    'misc',
    'roth_conversion_gain',
)
Form1099 = namedtuple(
    'Form1099',
    fields_1099,
    defaults=('',) + (0,) * len(fields_1099[1:]))


fields_real_estate = (
    'id',
    'is_primary',
    'rents',
    'taxes',
    'interests',
    'hoa',
    'insurance',
    'advertising',
    'legal',
    'commissions',
    'management',
    'repairs',
    'utilities',
    'depreciation',
    'other',
)
RealEstate = namedtuple(
    'RealEstate',
    fields_real_estate,
    defaults=('', False) + (0,) * len(fields_real_estate[2:]))

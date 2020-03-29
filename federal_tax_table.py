from collections import namedtuple

import sys


RegularTaxParameters = namedtuple('RegularTaxParameters', [
    'social_security_max_wage',
    'social_security_taxrate',
    'brackets',
    'qdcg_thresholds',
    'limit_threshold',
    'exemption',
    'standard_deduction',
])


regular_tax_table = {

    2012: RegularTaxParameters(
        social_security_max_wage=110100,
        social_security_taxrate=0.052,
        brackets=[
            (0, 0.1),
            (8700, 0.15),
            (35350, 0.25),
            (85650, 0.28),
            (178650, 0.33),
            (388350, 0.35)],
        qdcg_thresholds=[
            (35350, 0),
            (sys.maxsize, 0.15)],
        limit_threshold=sys.maxsize,
        exemption=3800,
        standard_deduction=5950,
    ),

    2013: RegularTaxParameters(
        social_security_max_wage=113700,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (8925, 0.15),
            (36250, 0.25),
            (87850, 0.28),
            (183250, 0.33),
            (398350, 0.35),
            (400000, 0.396)],
        qdcg_thresholds=[
            (36250, 0),
            (400000, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=250000,
        exemption=3900,
        standard_deduction=6100,
    ),

    2014: RegularTaxParameters(
        social_security_max_wage=117000,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9075, 0.15),
            (36900, 0.25),
            (89350, 0.28),
            (186350, 0.33),
            (405100, 0.35),
            (406750, 0.396)],
        qdcg_thresholds=[
            (36900, 0),
            (406750, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=254200,
        exemption=3950,
        standard_deduction=6200,
    ),

    2015: RegularTaxParameters(
        social_security_max_wage=118500,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9225, 0.15),
            (37450, 0.25),
            (90750, 0.28),
            (189300, 0.33),
            (411500, 0.35),
            (413200, 0.396)],
        qdcg_thresholds=[
            (37450, 0),
            (413200, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=258250,
        exemption=4000,
        standard_deduction=6300,
    ),

    2016: RegularTaxParameters(
        social_security_max_wage=118500,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9275, 0.15),
            (37650, 0.25),
            (91150, 0.28),
            (190150, 0.33),
            (413350, 0.35),
            (415050, 0.396)],
        qdcg_thresholds=[
            (37650, 0),
            (415050, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=259400,
        exemption=4050,
        standard_deduction=6300,
    ),

    2017: RegularTaxParameters(
        social_security_max_wage=127200,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9325, 0.15),
            (37950, 0.25),
            (91900, 0.28),
            (191650, 0.33),
            (416700, 0.35),
            (418400, 0.396)],
        qdcg_thresholds=[
            (37950, 0),
            (418400, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=261500,
        exemption=4050,
        standard_deduction=6350,
    ),

    2018: RegularTaxParameters(
        social_security_max_wage=128400,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9525, 0.12),
            (38700, 0.22),
            (82500, 0.24),
            (157500, 0.32),
            (200000, 0.35),
            (500000, 0.37)],
        qdcg_thresholds=[
            (38600, 0),
            (425800, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=sys.maxsize,
        exemption=0,
        standard_deduction=12000,
    ),

    2019: RegularTaxParameters(
        social_security_max_wage=132900,
        social_security_taxrate=0.062,
        brackets=[
            (0, 0.1),
            (9700, 0.12),
            (39475, 0.22),
            (84200, 0.24),
            (160725, 0.32),
            (204100, 0.35),
            (510300, 0.37)],
        qdcg_thresholds=[
            (39375, 0),
            (434550, 0.15),
            (sys.maxsize, 0.2)],
        limit_threshold=sys.maxsize,
        exemption=0,
        standard_deduction=12200,
    ),
}


AMTTaxParameters = namedtuple('AMTTaxParameters', [
    'brackets',
    'qdcg_thresholds',
    'limit_threshold',
    'exemption',
])


amt_tax_table = {

    2012: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (175000, 0.28)],
        qdcg_thresholds=regular_tax_table[2012].qdcg_thresholds,
        limit_threshold=112500,
        exemption=50600,
    ),

    2013: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (179500, 0.28)],
        qdcg_thresholds=regular_tax_table[2013].qdcg_thresholds,
        limit_threshold=115400,
        exemption=51900,
    ),

    2014: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (182500, 0.28)],
        qdcg_thresholds=regular_tax_table[2014].qdcg_thresholds,
        limit_threshold=117300,
        exemption=52800,
    ),

    2015: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (185400, 0.28)],
        qdcg_thresholds=regular_tax_table[2015].qdcg_thresholds,
        limit_threshold=119200,
        exemption=53600,
    ),

    2016: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (186300, 0.28)],
        qdcg_thresholds=regular_tax_table[2016].qdcg_thresholds,
        limit_threshold=119700,
        exemption=53900,
    ),

    2017: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (187800, 0.28)],
        qdcg_thresholds=regular_tax_table[2017].qdcg_thresholds,
        limit_threshold=120700,
        exemption=54300,
    ),

    2018: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (191500, 0.28)],
        qdcg_thresholds=regular_tax_table[2018].qdcg_thresholds,
        limit_threshold=500000,
        exemption=70300,
    ),

    2019: AMTTaxParameters(
        brackets=[
            (0, 0.26),
            (194800, 0.28)],
        qdcg_thresholds=regular_tax_table[2019].qdcg_thresholds,
        limit_threshold=510300,
        exemption=71700,
    ),
}

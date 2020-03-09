from collections import namedtuple


StateTaxParameters = namedtuple('StateTaxParameters', [
    'brackets',
    'limit_threshold',
    'exemption',
    'standard_deduction',
    ])


state_tax_table = {

    2012: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (7455, 0.02),
            (17676, 0.04),
            (27897, 0.06),
            (38726, 0.08),
            (48942, 0.093),
            (250000, 0.103),
            (300000, 0.113),
            (500000, 0.123)],
        limit_threshold=169730,
        exemption=104,
        standard_deduction=3841,
    ),

    2013: StateTaxParameters(
        brackets= [
            (0, 0.01),
            (7582, 0.02),
            (17976, 0.04),
            (28371, 0.06),
            (39384, 0.08),
            (49774, 0.093),
            (254250, 0.103),
            (305100, 0.113),
            (508500, 0.123)],
        limit_threshold=172615,
        exemption=106,
        standard_deduction=3906,
    ),

    2014: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (7749, 0.02),
            (18371, 0.04),
            (28995, 0.06),
            (40250, 0.08),
            (50869, 0.093),
            (259844, 0.103),
            (311812, 0.113),
            (519687, 0.123)],
        limit_threshold=176413,
        exemption=108,
        standard_deduction=3992,
    ),

    2015: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (7850, 0.02),
            (18610, 0.04),
            (29372, 0.06),
            (40773, 0.08),
            (51530, 0.093),
            (263222, 0.103),
            (315866, 0.113),
            (526443, 0.123)],
        limit_threshold=178706,
        exemption=109,
        standard_deduction=4044,
    ),

    2016: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (8015, 0.02),
            (19001, 0.04),
            (29989, 0.06),
            (41629, 0.08),
            (52612, 0.093),
            (268750, 0.103),
            (322499, 0.113),
            (537498, 0.123)],
        limit_threshold=182459,
        exemption=111,
        standard_deduction=4129,
    ),

    2017: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (8223, 0.02),
            (19495, 0.04),
            (30769, 0.06),
            (42711, 0.08),
            (53980, 0.093),
            (275738, 0.103),
            (330884, 0.113),
            (551473, 0.123)],
        limit_threshold=187203,
        exemption=114,
        standard_deduction=4236,
    ),

    2018: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (8544, 0.02),
            (20255, 0.04),
            (31969, 0.06),
            (44377, 0.08),
            (56085, 0.093),
            (286492, 0.103),
            (343788, 0.113),
            (572980, 0.123)],
        limit_threshold=194504,
        exemption=118,
        standard_deduction=4401,
    ),

    2019: StateTaxParameters(
        brackets=[
            (0, 0.01),
            (8809, 0.02),
            (20883, 0.04),
            (32960, 0.06),
            (45753, 0.08),
            (57824, 0.093),
            (295373, 0.103),
            (354445, 0.113),
            (590742, 0.123)],
        limit_threshold=200534,
        exemption=122,
        standard_deduction=4537,
    ),
}

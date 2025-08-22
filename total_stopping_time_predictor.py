#!/usr/bin/env python3
#########################################################################################################
# total_stopping_time_predictor.py
#
# Collatz total stopping time predictor
#########################################################################################################

# Standard library imports
import sys
from typing import Dict, Union

# Configuration constants
MAX_COMPUTATION_STEPS = 10000      # Safety limit to prevent infinite loops in sequence generation
MAX_INPUT_VALUE = 2**50            # Maximum allowed input to prevent integer overflow


DICTIONARY = {
    1: {
        "wormhole": [1],
        "mr": 0,
        "pseudocycle": [1,1]
    },
    3: {
        "wormhole": [3,10,5,16,8,4,2,1],
        "mr": 1,
        "pseudocycle": [3,4]
    },
    6: {
        "wormhole": [6,3,10,5,16,8,4,2,1],
        "mr": 2,
        "pseudocycle": [6,5]
    },
    7: {
        "wormhole": [7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 3,
        "pseudocycle": [7,8]
    },
    14: {
        "wormhole": [14,7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 6,
        "pseudocycle": [14,13]
    },
    15: {
        "wormhole": [15,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 7,
        "pseudocycle": [15,16]
    },
    18: {
        "wormhole": [18,9,28,14,7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 8,
        "pseudocycle": [18,17]
    },
    19: {
        "wormhole": [19,58,29,88,44,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 9,
        "pseudocycle": [19,20]
    },
    25: {
        "wormhole": [25,76,38,19,58,29,88,44,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 12,
        "pseudocycle": [25,26]
    },
    33: {
        "wormhole": [33,100,50,25,76,38,19,58,29,88,44,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 16,
        "pseudocycle": [33,34]
    },
    39: {
        "wormhole": [39,118,59,178,89,268,134,67,202,101,304,152,76,38,19,58,29,88,44,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 19,
        "pseudocycle": [39,40]
    },
    51: {
        "wormhole": [51,154,77,232,116,58,29,88,44,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1],
        "mr": 25,
        "pseudocycle": [51,52]
    },
    91: {
        "wormhole": [91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 45,
        "pseudocycle": [91,92]
    },
    108: {
        "wormhole": [108,54,27,82,41,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 53,
        "pseudocycle": [108,107]
    },
    121: {
        "wormhole": [121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 60,
        "pseudocycle": [121,122]
    },
    159: {
        "wormhole": [159,478,239,718,359,1078,539,1618,809,2428,1214,607,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 79,
        "pseudocycle": [159,160]
    },
    183: {
        "wormhole": [183,550,275,826,413,1240,620,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 91,
        "pseudocycle": [183,184]
    },
    243: {
        "wormhole": [243,730,365,1096,548,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 121,
        "pseudocycle": [243,244]
    },
    252: {
        "wormhole": [252,126,63,190,95,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 125,
        "pseudocycle": [252,251]
    },
    284: {
        "wormhole": [284,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 141,
        "pseudocycle": [284,283]
    },
    333: {
        "wormhole": [333,1000,500,250,125,376,188,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 166,
        "pseudocycle": [333,334]
    },
    378: {
        "wormhole": [378,189,568,284,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 188,
        "pseudocycle": [378,377]
    },
    411: {
        "wormhole": [411,1234,617,1852,926,463,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 205,
        "pseudocycle": [411,412]
    },
    487: {
        "wormhole": [487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 243,
        "pseudocycle": [487,488]
    },
    501: {
        "wormhole": [501,1504,752,376,188,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 250,
        "pseudocycle": [501,502]
    },
    649: {
        "wormhole": [649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 324,
        "pseudocycle": [649,650]
    },
    667: {
        "wormhole": [667,2002,1001,3004,1502,751,2254,1127,3382,1691,5074,2537,7612,3806,1903,5710,2855,8566,4283,12850,6425,19276,9638,4819,14458,7229,21688,10844,5422,2711,8134,4067,12202,6101,18304,9152,4576,2288,1144,572,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 333,
        "pseudocycle": [667,668]
    },
    865: {
        "wormhole": [865,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 432,
        "pseudocycle": [865,866]
    },
    889: {
        "wormhole": [889,2668,1334,667,2002,1001,3004,1502,751,2254,1127,3382,1691,5074,2537,7612,3806,1903,5710,2855,8566,4283,12850,6425,19276,9638,4819,14458,7229,21688,10844,5422,2711,8134,4067,12202,6101,18304,9152,4576,2288,1144,572,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 444,
        "pseudocycle": [889,890]
    },
    975: {
        "wormhole": [975,2926,1463,4390,2195,6586,3293,9880,4940,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 487,
        "pseudocycle": [975,976]
    },
    1153: {
        "wormhole": [1153,3460,1730,865,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 576,
        "pseudocycle": [1153,1154]
    },
    1185: {
        "wormhole": [1185,3556,1778,889,2668,1334,667,2002,1001,3004,1502,751,2254,1127,3382,1691,5074,2537,7612,3806,1903,5710,2855,8566,4283,12850,6425,19276,9638,4819,14458,7229,21688,10844,5422,2711,8134,4067,12202,6101,18304,9152,4576,2288,1144,572,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 592,
        "pseudocycle": [1185,1186]
    },
    1299: {
        "wormhole": [1299,3898,1949,5848,2924,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 649,
        "pseudocycle": [1299,1300]
    },
    1335: {
        "wormhole": [1335,4006,2003,6010,3005,9016,4508,2254,1127,3382,1691,5074,2537,7612,3806,1903,5710,2855,8566,4283,12850,6425,19276,9638,4819,14458,7229,21688,10844,5422,2711,8134,4067,12202,6101,18304,9152,4576,2288,1144,572,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 667,
        "pseudocycle": [1335,1336]
    },
    1368: {
        "wormhole": [1368,684,342,171,514,257,772,386,193,580,290,145,436,218,109,328,164,82,41,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 683,
        "pseudocycle": [1368,1367]
    },
    1731: {
        "wormhole": [1731,5194,2597,7792,3896,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 865,
        "pseudocycle": [1735,1736]
    },
    1779: {
        "wormhole": [1779,5338,2669,8008,4004,2002,1001,3004,1502,751,2254,1127,3382,1691,5074,2537,7612,3806,1903,5710,2855,8566,4283,12850,6425,19276,9638,4819,14458,7229,21688,10844,5422,2711,8134,4067,12202,6101,18304,9152,4576,2288,1144,572,286,143,430,215,646,323,970,485,1456,728,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 889,
        "pseudocycle": [1779,1780]
    },
    2307: {
        "wormhole": [2307,6922,3461,10384,5192,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 1153,
        "pseudocycle": [2307,2308]
    },
    2430: {
        "wormhole": [2430,1215,3646,1823,5470,2735,8206,4103,12310,6155,18466,9233,27700,13850,6925,20776,10388,5194,2597,7792,3896,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 1214,
        "pseudocycle": [2430,2429]
    },
    3643: {
        "wormhole": [3643,10930,5465,16396,8198,4099,12298,6149,18448,9224,4612,2306,1153,3460,1730,865,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 1821,
        "pseudocycle": [3643,3644]
    },
    4857: {
        "wormhole": [4857,14572,7286,3643,10930,5465,16396,8198,4099,12298,6149,18448,9224,4612,2306,1153,3460,1730,865,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 2428,
        "pseudocycle": [4857,4858]
    },
    7287: {
        "wormhole": [7287,21862,10931,32794,16397,49192,24596,12298,6149,18448,9224,4612,2306,1153,3460,1730,865,2596,1298,649,1948,974,487,1462,731,2194,1097,3292,1646,823,2470,1235,3706,1853,5560,2780,1390,695,2086,1043,3130,1565,4696,2348,1174,587,1762,881,2644,1322,661,1984,992,496,248,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1],
        "mr": 3643,
        "pseudocycle": [7287,7288]
    },
}

# Custom exceptions for specific error handli   ng
class ValidationError(Exception):
    pass

class ComputationError(Exception):
    pass

def validate_input(n: Union[int, str, float]) -> int:
    """
    Validate and convert input to a positive integer for Collatz sequence computation.
    
    This function performs comprehensive input validation and type conversion to ensure
    the input is suitable for Collatz sequence analysis. It handles various input types
    (string, float, int) and applies mathematical and practical constraints.
    
    Args:
        n (Union[int, str, float]): The input value to validate and convert.
                                   Can be a string representation of a number,
                                   a float (must be a whole number), or an integer.
    
    Returns:
        int: A validated positive integer ready for Collatz computation.
    
    Raises:
        ValidationError: If input is None, empty, not a whole number, non-positive,
                        too large, or has invalid format.
    
    Examples:
        >>> validate_input("27")
        27
        >>> validate_input(42.0)
        42
        >>> validate_input(15)
        15
        >>> validate_input("0")  # Raises ValidationError
        >>> validate_input("3.14")  # Raises ValidationError
        >>> validate_input("")  # Raises ValidationError
    
    Notes:
        - Maximum allowed value is 2^50 to prevent computational overflow
        - Floating point inputs must represent exact integers (e.g., 27.0 is valid, 27.1 is not)
        - String inputs are stripped of whitespace before processing
        - Input must be positive (> 0) as Collatz conjecture is defined for positive integers
    """

    # Check for None input - cannot proceed with null values
    if n is None:
        raise ValidationError("Input cannot be None")
    
    try:
        # Handle string input type
        if isinstance(n, str):
            # Remove leading/trailing whitespace
            n = n.strip()

            # Check for empty string after stripping
            if not n:
                raise ValidationError("Input cannot be empty")
            # Check if string contains decimal point (potential float)
            if '.' in n:
                # Convert to float first to validate decimal representation
                float_n = float(n)
                # Ensure the float represents a whole number
                if float_n.is_integer():
                    n_int = int(float_n)
                else:
                    raise ValidationError(f"Input '{n}' is not a whole number")
            else:
                # Direct integer conversion for strings without decimal points
                n_int = int(n)
        # Handle float input type
        elif isinstance(n, float):
            # Verify that float represents a whole number
            if not n.is_integer():
                raise ValidationError(f"Input {n} is not a whole number")
            n_int = int(n)
        # Handle integer input type (direct assignment)
        elif isinstance(n, int):
            n_int = n
        # Handle unsupported input types
        else:
            raise ValidationError(f"Cannot convert {type(n).__name__} to integer")
    # Catch conversion errors and provide meaningful feedback
    except (ValueError, OverflowError) as e:
        raise ValidationError(f"Invalid number format: {n}") from e
    # Validate that the number is positive (Collatz conjecture requirement)
    if n_int <= 0:
        raise ValidationError(f"n must be positive, got {n_int}")
    # Check against maximum allowed value to prevent computational issues
    if n_int > MAX_INPUT_VALUE:
        raise ValidationError(f"n={n_int} too large (limit: {MAX_INPUT_VALUE})")
    
    return n_int

def next_collatz_value(n: int) -> int:
    """
    Apply one step of the Collatz function to compute the next value in the sequence.
    
    This function implements the core Collatz conjecture transformation:
    - If n is even: return n/2
    - If n is odd: return 3n+1
    
    The function includes overflow protection to prevent integer overflow during
    the 3n+1 operation for very large odd numbers.
    
    Args:
        n (int): A positive integer for which to compute the next Collatz value.
                Must be greater than 0.
    
    Returns:
        int: The next value in the Collatz sequence according to the transformation rules.
    
    Raises:
        ComputationError: If n is non-positive or if overflow risk is detected
                         during the 3n+1 operation for large odd numbers.
    
    Examples:
        >>> next_collatz_value(6)    # Even: 6/2
        3
        >>> next_collatz_value(3)    # Odd: 3*3+1
        10
        >>> next_collatz_value(1)    # Odd: 3*1+1
        4
        >>> next_collatz_value(0)    # Raises ComputationError
        
    Notes:
        - This is the fundamental operation of the Collatz conjecture
        - Even numbers are always divided by 2 (right bit shift equivalent)
        - Odd numbers follow the 3n+1 rule with overflow protection
        - Overflow threshold is set at (2^62 - 1) // 3 to prevent integer overflow
        - The sequence eventually reaches 1 for all tested positive integers
    """
    # Validate input is positive (Collatz function domain requirement)
    if n <= 0:
        raise ComputationError(f"Invalid value: {n}")
    # Apply Collatz transformation based on parity
    if n % 2 == 0:
        # Even case: divide by 2 (equivalent to right bit shift)
        return n // 2
    else:
        # Odd case: apply 3n+1 with overflow protection
        # Check if 3n+1 would cause integer overflow
        if n > (2**62 - 1) // 3:
            raise ComputationError(f"Overflow risk for n={n}")
        return 3 * n + 1

def generate_standard_sequence(n: int) -> list:
    """
    Generate the complete Collatz sequence from n to 1 using the standard algorithm.
    
    This function implements the traditional Collatz sequence generation by repeatedly
    applying the Collatz function until reaching 1. It serves as the baseline reference
    for comparison with optimized algorithms (like the wormhole approach).
    
    The sequence generation follows these steps:
    1. Start with the input number n
    2. Apply next_collatz_value() repeatedly
    3. Continue until reaching 1
    4. Include 1 as the final element
    
    Args:
        n (int): A positive integer starting point for the Collatz sequence.
                Must be already validated (typically by validate_input).
    
    Returns:
        list: Complete Collatz sequence from n to 1 (inclusive).
              Example: for n=3, returns [3, 10, 5, 16, 8, 4, 2, 1]
    
    Raises:
        ComputationError: If the sequence exceeds MAX_COMPUTATION_STEPS without
                         reaching 1, indicating potential infinite loop or
                         computational limits.
    
    Examples:
        >>> generate_standard_sequence(3)
        [3, 10, 5, 16, 8, 4, 2, 1]
        >>> generate_standard_sequence(1)
        [1]
        >>> generate_standard_sequence(4)
        [4, 2, 1]
        
    Notes:
        - This is the reference implementation for Collatz sequence generation
        - Includes safety mechanism to prevent infinite loops via MAX_COMPUTATION_STEPS
        - The Collatz conjecture states that this sequence reaches 1 for all positive integers
        - Sequence length equals the total stopping time + 1 (including the starting number)
        - Used for validation and comparison with optimized algorithms
    """
    sequence = []  # Initialize empty sequence to store the path
    current = n    # Start with the input number
    steps = 0      # Counter to prevent infinite loops
    
    # Generate sequence until reaching 1
    while current != 1 and steps < MAX_COMPUTATION_STEPS:
        sequence.append(current)                    # Add current number to sequence
        current = next_collatz_value(current)       # Apply Collatz transformation
        steps += 1                                  # Increment step counter
    
    # Check if we exceeded the maximum allowed steps (safety mechanism)
    if steps >= MAX_COMPUTATION_STEPS:
        raise ComputationError(f"Sequence too long for n={n}")

    # Add the final 1 to complete the sequence
    sequence.append(1)
    return sequence

def generate_wormhole_sequence(n: int) -> tuple:
    """
    Generate Collatz sequence using the wormhole optimization algorithm.
    
    This function implements an optimized approach to Collatz sequence generation
    by utilizing pre-computed "wormhole" sequences. Instead of calculating every
    step, it searches for known entry points in the DICTIONARY and uses the
    corresponding pre-computed sequence to "jump" directly to the end.
    
    Algorithm workflow:
    1. Start with input number n
    2. For each step, check if current number is a wormhole entry point
    3. If found: append the pre-computed wormhole sequence and terminate
    4. If not found: continue with standard Collatz calculation
    5. Repeat until reaching 1 or finding a wormhole
    
    Args:
        n (int): A positive integer starting point for the Collatz sequence.
                Must be already validated (typically by validate_input).
    
    Returns:
        tuple: A 2-tuple containing:
            - sequence (list): Complete Collatz sequence from n to 1
            - entry_point_info (dict): Information about wormhole usage containing:
                * wormhole_used (bool): Whether a wormhole was utilized
                * entry_point_found (int): The number that served as wormhole entry
                * entry_point_position (int): Step position where wormhole was found
                * wormhole_length (int): Length of the utilized wormhole sequence
    
    Raises:
        ComputationError: If computation exceeds MAX_COMPUTATION_STEPS without
                         finding a wormhole or reaching 1.
    
    Examples:
        >>> seq, info = generate_wormhole_sequence(6)
        >>> seq
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> info
        {'entry_point_found': 3, 'entry_point_position': 1, 'wormhole_used': True, 'wormhole_length': 8}
        
        >>> seq, info = generate_wormhole_sequence(2)
        >>> info['wormhole_used']
        False
        
    Notes:
        - This is the core optimization that provides computational efficiency
        - Wormholes are pre-computed sequences stored in the global DICTIONARY
        - Entry point detection happens at each step before applying Collatz function
        - The algorithm gracefully falls back to standard computation if no wormhole is found
        - Sequence generated is mathematically identical to standard algorithm
        - Computational savings can be significant for numbers that quickly reach known entry points
    """
    sequence = []          # Initialize sequence to store the computational path
    current = n            # Start with the input number
    steps = 0              # Counter for computed steps (before wormhole usage)
    
    # Generate sequence until reaching 1
    sequence = []
    current = n
    steps = 0
    
    while current != 1:
        sequence.append(current) # Add current number to sequence
        
        # Check if current number is a wormhole entry point in our dictionary
        if current in DICTIONARY:
            # Wormhole found! Extract the pre-computed sequence
            wormhole_seq = DICTIONARY[current]["wormhole"]
            # Append wormhole sequence (skip first element to avoid duplication)
            # The first element is already computed and in our sequence as 'current'
            sequence.extend(wormhole_seq[1:]) 
            
            # Return sequence with detailed wormhole usage information
            return sequence, {
                "entry_point_found": current,            # Which number triggered the wormhole
                "entry_point_position": steps,           # At what step the wormhole was found
                "wormhole_used": True,                   # Confirmation that optimization was applied
                "wormhole_length": len(wormhole_seq)     # Size of the utilized wormhole
            }
        
        # No wormhole found at this step, so let's continue with standard Collatz calculation
        current = next_collatz_value(current)
        steps += 1
        
        # Safety mechanism to prevent infinite loops
        if steps > MAX_COMPUTATION_STEPS:
            raise ComputationError(f"Exceeded {MAX_COMPUTATION_STEPS} steps")
    
    # Reached 1 without finding any wormhole - standard computation completed
    sequence.append(1)  # Add final 1 to complete the sequence
    
    # Return sequence with information indicating no wormhole was used
    return sequence, {"wormhole_used": False}

def compare_sequences(n: int) -> dict:
    """
    Compare Collatz sequences generated by standard Colatz algorithm and wormhole algorithm.
    
    This function performs a comprehensive comparison between the traditional Collatz
    sequence generation and the optimized wormhole approach to ensure mathematical
    equivalence. It serves as a validation mechanism to verify that the wormhole
    optimization produces identical results to the standard computation.
    
    The comparison includes:
    - Sequence content verification (element-by-element comparison)
    - Length validation
    - First difference detection (if sequences differ)
    - Wormhole usage statistics
    
    Args:
        n (int): A positive integer for which to generate and compare sequences.
                Must be already validated.
    
    Returns:
        dict: Comprehensive comparison results containing:
            - n (int): The input number that was analyzed
            - sequences_identical (bool): Whether both sequences are exactly the same
            - standard_length (int): Length of the standard algorithm sequence
            - wormhole_length (int): Length of the wormhole algorithm sequence
            - entry_point_info (dict): Information about wormhole usage from wormhole algorithm
            
            If sequences differ, additional fields are included:
            - first_difference_position (int): Index where sequences first differ
            - standard_value_at_diff: Value in standard sequence at difference position
            - wormhole_value_at_diff: Value in wormhole sequence at difference position
            - standard_sequence (list): Complete standard sequence for debugging
            - wormhole_sequence (list): Complete wormhole sequence for debugging
            
            If error occurs:
            - error (str): Description of the error that occurred
    
    Examples:
        >>> result = compare_sequences(27)
        >>> result['sequences_identical']
        True
        >>> result['entry_point_info']['wormhole_used']
        True
        
        >>> result = compare_sequences(1)
        >>> result['sequences_identical']
        True
        >>> result['entry_point_info']['wormhole_used']
        False
        
    Notes:
        - This function is critical for validating the correctness of wormhole optimization
        - Sequences should always be identical if wormhole dictionary is correct
        - Any difference indicates an error in the wormhole pre-computed sequences
        - Used extensively in testing and validation workflows
        - Provides detailed debugging information when discrepancies are found
    """
    try:
        # Generate sequences using both algorithms for comparison
        standard_sequence = generate_standard_sequence(n)
        wormhole_sequence, entry_point_info = generate_wormhole_sequence(n)
        
        # Perform element-by-element comparison of the sequences
        sequences_match = standard_sequence == wormhole_sequence
        
        # Build basic comparison result structure
        result = {
            "n": n,
            "sequences_identical": sequences_match,
            "standard_length": len(standard_sequence),
            "wormhole_length": len(wormhole_sequence),
            "entry_point_info": entry_point_info
        }
        
        # If sequences differ, provide detailed diagnostic information
        if not sequences_match:
            # Find the first position where sequences diverge
            min_len = min(len(standard_sequence), len(wormhole_sequence))
            first_diff_pos = None
            
            # Scan through sequences to locate first difference
            for i in range(min_len):
                if standard_sequence[i] != wormhole_sequence[i]:
                    first_diff_pos = i
                    break
            
            # Add detailed debugging information for sequence differences
            result.update({
                "first_difference_position": first_diff_pos,
                "standard_value_at_diff": standard_sequence[first_diff_pos] if first_diff_pos is not None else None,
                "wormhole_value_at_diff": wormhole_sequence[first_diff_pos] if first_diff_pos is not None else None,
                "standard_sequence": standard_sequence,    # Full sequence for analysis
                "wormhole_sequence": wormhole_sequence     # Full sequence for analysis
            })
        
        return result
        
    except Exception as e:
        # Handle any errors during sequence generation or comparison
        return {
            "n": n,
            "sequences_identical": False,  # Mark as non-identical due to error
            "error": str(e)                # Capture error details for debugging
        }

def validate_wormhole_sequence(n: int, entry_point_num: int, entry_point_position: int) -> Dict[str, any]:
    """
    Validate that a wormhole sequence matches the actual Collatz computation.
    
    This function performs mathematical verification of wormhole sequences stored
    in the DICTIONARY by computing the actual Collatz sequence from the entry point
    and comparing it element-by-element with the pre-stored wormhole sequence.
    This ensures the integrity and correctness of the wormholes.
    
    The validation process:
    1. Retrieve the expected wormhole sequence from DICTIONARY
    2. Compute the actual Collatz sequence from the entry point
    3. Compare sequences for length and content
    4. Report any discrepancies with detailed diagnostic information
    
    Args:
        n (int): The original input number (used for context/reporting)
        entry_point_num (int): The number that serves as the wormhole entry point
        entry_point_position (int): The step position where the entry point was reached
    
    Returns:
        Dict[str, any]: Validation results containing:
            - valid (bool): Whether the wormhole sequence is mathematically correct
            - sequence_length (int): Length of validated sequence (if valid)
            
            If validation fails, additional diagnostic fields:
            - error (str): Description of the validation failure
            - actual_length (int): Length of computed sequence
            - expected_length (int): Length of stored wormhole sequence
            - position (int): First position where sequences differ (if applicable)
            - actual_value: Value in computed sequence at difference position
            - expected_value: Value in wormhole sequence at difference position
            - actual_sequence (list): Complete computed sequence for debugging
            - expected_sequence (list): Complete wormhole sequence for debugging
    
    Examples:
        >>> validate_wormhole_sequence(27, 3, 1)
        {'valid': True, 'sequence_length': 8}
        
        >>> # If wormhole had an error:
        >>> validate_wormhole_sequence(100, 999, 5)
        {'valid': False, 'error': 'Entry point 999 does not lead a valid wormhole'}
        
    Notes:
        - This is a critical quality assurance function for wormhole integrity
        - Should be called whenever a wormhole is used to ensure mathematical correctness
        - Includes safety mechanisms to prevent infinite loops during validation
        - Provides detailed debugging information when validation fails
        - Essential for maintaining trust in the wormhole optimization results
    """
    # Check if the entry point exists in our wormhole dictionary
    if entry_point_num not in DICTIONARY:
        return {"valid": False, "error": f"Entry point {entry_point_num} does not lead a valid wormhole"}
    
    try:
        # Retrieve the expected wormhole sequence from the dictionary
        expected_sequence = DICTIONARY[entry_point_num]["wormhole"]
        
        # Compute the actual Collatz sequence starting from the entry point
        actual_sequence = []
        current = entry_point_num
        
        # Generate actual sequence until reaching 1
        while current != 1:
            actual_sequence.append(current)
            current = next_collatz_value(current)
            
            # Safety check to prevent infinite loops during validation
            # Allow some tolerance beyond expected length for safety
            if len(actual_sequence) > len(expected_sequence) + 100:
                return {
                    "valid": False, 
                    "error": f"Actual sequence too long (>{len(expected_sequence) + 100})",
                    "actual_length": len(actual_sequence),
                    "expected_length": len(expected_sequence)
                }
        
        # Add the final 1 to complete the actual sequence
        actual_sequence.append(1)
        
        # Validate sequence lengths match
        if len(actual_sequence) != len(expected_sequence):
            return {
                "valid": False,
                "error": "Sequence lengths differ",
                "actual_length": len(actual_sequence),
                "expected_length": len(expected_sequence),
                "actual_sequence": actual_sequence,
                "expected_sequence": expected_sequence
            }
        
        # Perform element-by-element validation
        for i, (actual, expected) in enumerate(zip(actual_sequence, expected_sequence)):
            if actual != expected:
                return {
                    "valid": False,
                    "error": f"Sequences differ at position {i}",
                    "position": i,
                    "actual_value": actual,
                    "expected_value": expected,
                    "actual_sequence": actual_sequence,
                    "expected_sequence": expected_sequence
                }
        
        # Validation successful - sequences are identical
        return {
            "valid": True,
            "sequence_length": len(actual_sequence)
        }
        
    except Exception as e:
        # Handle any computational errors during validation
        return {
            "valid": False,
            "error": f"Validation failed: {str(e)}"
        }

def calculate_wormhole_total_stopping_time(n: Union[int, str, float]) -> Dict[str, any]:
    """
    Calculate the total stopping time for Collatz sequence using wormhole optimization.
    
    This is the main computational function that implements the wormhole algorithm
    to efficiently calculate the total stopping time (number of steps to reach 1)
    for a given input. The function combines input validation, wormhole detection,
    and mathematical verification to provide both speed and accuracy.
    
    Algorithm workflow:
    1. Validate and convert input to proper integer format
    2. Handle trivial case (n=1) immediately
    3. Iterate through Collatz steps, checking for wormhole entry points
    4. When wormhole found: calculate total time using pre-computed data
    5. Validate wormhole accuracy to ensure mathematical correctness
    6. Fall back to standard computation if no wormhole available
    
    Args:
        n (Union[int, str, float]): The input number for which to calculate
                                   total stopping time. Can be string, float, or int.
    
    Returns:
        Dict[str, any]: Comprehensive results containing:
            - total_stopping_time (int): Number of steps to reach 1 (-1 if error)
            - algorithm (str): Always "wormhole" to identify the method used
            - prediction_type (str): Type of result achieved:
                * "trivial": Input was 1 (0 steps)
                * "entry_point_found": Wormhole was successfully used
                * "no_entry_point": No wormhole available, computed to completion
                * "validation_failed": Wormhole found but failed validation
                * "error": Input validation or computation error occurred
            - computed_steps (int): Steps calculated before using wormhole
            - saved_steps (int): Steps saved by using wormhole optimization
            
            Additional fields when wormhole is used:
            - entry_point_found (int): The number that triggered wormhole usage
            - entry_point_position (int): Step where wormhole entry was reached
            - wormhole_length (int): Total length of the wormhole sequence
            - validation (dict): Results from wormhole mathematical verification
            
            Additional fields when errors occur:
            - error_message (str): Detailed description of the error
            - validation_error (str): Specific validation error (if applicable)
    
    Examples:
        >>> calculate_wormhole_total_stopping_time(27)
        {
            'total_stopping_time': 111,
            'algorithm': 'wormhole',
            'prediction_type': 'entry_point_found',
            'entry_point_found': 91,
            'entry_point_position': 27,
            'computed_steps': 27,
            'saved_steps': 84,
            'wormhole_length': 85,
            'validation': {'valid': True, 'sequence_length': 85}
        }
        
        >>> calculate_wormhole_total_stopping_time(1)
        {
            'total_stopping_time': 0,
            'algorithm': 'wormhole',
            'prediction_type': 'trivial',
            'computed_steps': 0,
            'saved_steps': 0
        }
        
        >>> calculate_wormhole_total_stopping_time("invalid")
        {
            'total_stopping_time': -1,
            'algorithm': 'wormhole',
            'prediction_type': 'error',
            'error_message': 'Invalid number format: invalid',
            'computed_steps': 0,
            'saved_steps': 0
        }
    
    Notes:
        - This function provides the main interface for wormhole-optimized computation
        - Includes comprehensive error handling and input validation
        - Always validates wormhole results to ensure mathematical accuracy
        - Gracefully falls back to standard computation when no optimization available
        - Tracks computational efficiency metrics (computed vs saved steps)
        - Essential for demonstrating the performance benefits of wormhole optimization
    """
    # Validate and convert input to proper integer format
    try:
        n_val = validate_input(n)
    except ValidationError as e:
        # Return error result with diagnostic information
        return {
            "total_stopping_time": -1,
            "algorithm": "wormhole",
            "prediction_type": "error",
            "error_message": str(e),
            "computed_steps": 0,
            "saved_steps": 0
        }
    
    # Handle trivial case where input is already 1
    if n_val == 1:
        return {
            "total_stopping_time": 0,
            "algorithm": "wormhole",
            "prediction_type": "trivial",
            "computed_steps": 0,
            "saved_steps": 0
        }
    
    try:
        current = n_val  # Start computation from validated input
        steps = 0        # Counter for steps computed before wormhole usage
        
        # Main computation loop: search for wormhole entry points
        while current != 1:
            # Check if current number is a wormhole entry point in our dictionary
            if current in DICTIONARY:
                # Wormhole entry point found! Calculate total stopping time
                wormhole_sequence = DICTIONARY[current]["wormhole"]
                wormhole_steps = len(wormhole_sequence) - 1  # Exclude starting number
                total_steps = steps + wormhole_steps
                
                # Build comprehensive result with wormhole usage information
                result = {
                    "total_stopping_time": total_steps,
                    "algorithm": "wormhole",
                    "prediction_type": "entry_point_found",
                    "entry_point_found": current,              # Which number triggered wormhole
                    "entry_point_position": steps,             # When wormhole was found
                    "computed_steps": steps,                   # Steps calculated manually
                    "saved_steps": wormhole_steps,             # Steps saved by optimization
                    "wormhole_length": len(wormhole_sequence)  # Size of wormhole used
                }
                
                # Validate wormhole mathematical correctness
                validation_result = validate_wormhole_sequence(n_val, current, steps)
                result["validation"] = validation_result
                
                # Check if validation failed and update prediction type accordingly
                if not validation_result["valid"]:
                    result["prediction_type"] = "validation_failed"
                    result["validation_error"] = validation_result.get("error", "Unknown validation error")
                
                return result
            
            # No wormhole found at current step - continue with standard Collatz calculation
            current = next_collatz_value(current)
            steps += 1
            
            # Safety mechanism to prevent infinite computation
            if steps > MAX_COMPUTATION_STEPS:
                raise ComputationError(f"Exceeded {MAX_COMPUTATION_STEPS} steps")
        
        # Reached 1 without finding any wormhole entry point
        return {
            "total_stopping_time": steps,
            "algorithm": "wormhole",
            "prediction_type": "no_entry_point",
            "computed_steps": steps,
            "saved_steps": 0
        }
        
    except (ComputationError, ValidationError) as e:
        # Handle computation errors with diagnostic information
        return {
            "total_stopping_time": -1,
            "algorithm": "wormhole",
            "prediction_type": "error",
            "error_message": str(e),
            "computed_steps": steps if 'steps' in locals() else 0,
            "saved_steps": 0
        }

def calculate_standard_total_stopping_time(n: Union[int, str, float]) -> Dict[str, any]:
    """
    Calculate the total stopping time for Collatz sequence using standard algorithm.
    
    This function implements the traditional, unoptimized approach to calculating
    the total stopping time by applying the Collatz function repeatedly until
    reaching 1. It serves as a baseline reference for comparison with optimized
    algorithms and provides validation that wormhole results are mathematically correct.
    
    Algorithm workflow:
    1. Validate and convert input to proper integer format
    2. Handle trivial case (n=1) immediately
    3. Apply Collatz transformations step by step until reaching 1
    4. Count and return total number of steps taken
    
    Args:
        n (Union[int, str, float]): The input number for which to calculate
                                   total stopping time. Can be string, float, or int.
    
    Returns:
        Dict[str, any]: Standard algorithm results containing:
            - total_stopping_time (int): Number of steps to reach 1 (-1 if error)
            - algorithm (str): Always "standard" to identify the method used
            - prediction_type (str): Type of result achieved:
                * "trivial": Input was 1 (0 steps)
                * "complete": Successfully computed full sequence to completion
                * "error": Input validation or computation error occurred
            - computed_steps (int): Total steps calculated (same as total_stopping_time)
            - saved_steps (int): Always 0 (no optimization applied)
            
            Additional fields when errors occur:
            - error_message (str): Detailed description of the error
    
    Examples:
        >>> calculate_standard_total_stopping_time(27)
        {
            'total_stopping_time': 111,
            'algorithm': 'standard',
            'prediction_type': 'complete',
            'computed_steps': 111,
            'saved_steps': 0
        }
        
        >>> calculate_standard_total_stopping_time(1)
        {
            'total_stopping_time': 0,
            'algorithm': 'standard',
            'prediction_type': 'trivial',
            'computed_steps': 0,
            'saved_steps': 0
        }
        
        >>> calculate_standard_total_stopping_time("invalid")
        {
            'total_stopping_time': -1,
            'algorithm': 'standard',
            'prediction_type': 'error',
            'error_message': 'Invalid number format: invalid',
            'computed_steps': 0,
            'saved_steps': 0
        }
    
    Notes:
        - This function provides the reference implementation for comparison purposes
        - No optimizations applied - every step is computed individually
        - Essential for validating that wormhole algorithm produces identical results
        - Computational complexity is O(stopping_time) with no shortcuts
        - Used extensively in testing and validation workflows
        - Provides baseline performance metrics for efficiency comparisons
    """
    # Validate and convert input to proper integer format
    try:
        n_val = validate_input(n)
    except ValidationError as e:
        # Return error result with diagnostic information
        return {
            "total_stopping_time": -1,
            "algorithm": "standard",
            "prediction_type": "error",
            "error_message": str(e),
            "computed_steps": 0,
            "saved_steps": 0
        }
    
    # Handle trivial case where input is already 1
    if n_val == 1:
        return {
            "total_stopping_time": 0,
            "algorithm": "standard",
            "prediction_type": "trivial",
            "computed_steps": 0,
            "saved_steps": 0
        }
    
    try:
        steps = 0        # Counter for total steps to reach 1
        current = n_val  # Start computation from validated input
        
        # Main computation loop: apply Collatz function until reaching 1
        while current != 1:
            current = next_collatz_value(current)  # Apply Collatz transformation
            steps += 1                             # Increment step counter
            
            # Safety mechanism to prevent infinite computation
            if steps > MAX_COMPUTATION_STEPS:
                raise ComputationError(f"Exceeded {MAX_COMPUTATION_STEPS} steps")
        
        # Successfully computed stopping time
        return {
            "total_stopping_time": steps,
            "algorithm": "standard",
            "prediction_type": "complete",
            "computed_steps": steps,  # Same as total (no optimization)
            "saved_steps": 0          # No steps saved (no optimization)
        }
        
    except (ComputationError, ValidationError) as e:
        # Handle computation errors with diagnostic information
        return {
            "total_stopping_time": -1,
            "algorithm": "standard",
            "prediction_type": "error",
            "error_message": str(e),
            "computed_steps": steps if 'steps' in locals() else 0,
            "saved_steps": 0
        }
    
    # Handle trivial case where input is already 1
    if n_val == 1:
        return {
            "total_stopping_time": 0,
            "algorithm": "wormhole",
            "prediction_type": "trivial",
            "computed_steps": 0,
            "saved_steps": 0
        }
    
    try:
        current = n_val  # Start computation from validated input
        steps = 0        # Counter for steps computed before wormhole usage
        
        # Main computation loop: search for wormhole entry points
        while current != 1:
            # Check if current number is a wormhole entry point in our dictionary
            if current in DICTIONARY:
                # Wormhole entry point found! Calculate total stopping time
                wormhole_sequence = DICTIONARY[current]["wormhole"]
                wormhole_steps = len(wormhole_sequence) - 1  # Exclude starting number
                total_steps = steps + wormhole_steps
                
                # Build comprehensive result with wormhole usage information
                result = {
                    "total_stopping_time": total_steps,
                    "algorithm": "wormhole",
                    "prediction_type": "entry_point_found",
                    "entry_point_found": current,              # Which number triggered wormhole
                    "entry_point_position": steps,             # When wormhole was found
                    "computed_steps": steps,                   # Steps calculated manually
                    "saved_steps": wormhole_steps,             # Steps saved by optimization
                    "wormhole_length": len(wormhole_sequence)  # Size of wormhole used
                }
                
                # Validate wormhole mathematical correctness
                validation_result = validate_wormhole_sequence(n_val, current, steps)
                result["validation"] = validation_result
                
                # Check if validation failed and update prediction type accordingly
                if not validation_result["valid"]:
                    result["prediction_type"] = "validation_failed"
                    result["validation_error"] = validation_result.get("error", "Unknown validation error")
                
                return result
            
            # No wormhole found at current step - continue with standard Collatz calculation
            current = next_collatz_value(current)
            steps += 1
            
            # Safety mechanism to prevent infinite computation
            if steps > MAX_COMPUTATION_STEPS:
                raise ComputationError(f"Exceeded {MAX_COMPUTATION_STEPS} steps")
        
        # Reached 1 without finding any wormhole entry point
        return {
            "total_stopping_time": steps,
            "algorithm": "wormhole",
            "prediction_type": "no_entry_point",
            "computed_steps": steps,
            "saved_steps": 0
        }
        
    except (ComputationError, ValidationError) as e:
        # Handle computation errors with diagnostic information
        return {
            "total_stopping_time": -1,
            "algorithm": "wormhole",
            "prediction_type": "error",
            "error_message": str(e),
            "computed_steps": steps if 'steps' in locals() else 0,
            "saved_steps": 0
        }

def test_sequence_equivalence(max_n: int) -> None:
    """
    Test mathematical equivalence between standard and wormhole algorithms for a range of inputs.
    
    This function performs comprehensive validation testing by comparing the sequences
    generated by both algorithms across a range of input values from 1 to max_n.
    It serves as the primary quality assurance mechanism to ensure that wormhole
    optimization produces mathematically identical results to the standard algorithm.
    
    The testing process:
    1. Iterate through all integers from 1 to max_n
    2. Generate sequences using both standard and wormhole algorithms
    3. Compare sequences element-by-element for exact matches
    4. Track statistics about wormhole usage and computational savings
    5. Report any discrepancies with detailed diagnostic information
    6. Display comprehensive summary of testing results
    
    Args:
        max_n (int): The maximum number to test (inclusive). Testing range is [1, max_n].
                    Should be reasonable size to avoid excessive computation time.
    
    Returns:
        None: This function prints results directly to console and doesn't return values.
              All output is displayed in real-time during execution.
    
    Console Output:
        - Header with testing information
        - Real-time progress for each number tested:
          * Success cases showing wormhole usage and savings
          * Error cases highlighting sequence differences
        - Comprehensive summary with statistics:
          * Total numbers tested
          * Percentage of identical sequences
          * Wormhole usage statistics
          * Computational savings metrics
          * Detailed error reports (if any)
    
    Examples:
        >>> test_sequence_equivalence(100)
        # Outputs detailed testing results for n=1 to n=100
        
        >>> test_sequence_equivalence(1000)
        # Comprehensive testing across larger range
    
    Notes:
        - This is the primary function for validating wormhole algorithm correctness
        - Any sequence differences indicate errors in wormhole dictionary entries
        - Essential for quality assurance before deploying wormhole optimization
        - Provides valuable statistics about optimization effectiveness
        - Should be run regularly when updating wormhole dictionary
        - Execution time scales linearly with max_n and complexity of sequences
        - Critical for maintaining mathematical integrity of the optimization
    """
    # Display testing header with configuration information
    print("=" * 100)
    print("  COLLATZ TOTAL STOPPING TIME PREDICTOR")
    print("=" * 100)
    
    # Initialize statistics counters for tracking results
    identical_count = 0      # Number of cases where sequences matched exactly
    different_count = 0      # Number of cases where sequences differed
    error_count = 0          # Number of cases where computation errors occurred
    entry_points_used = 0    # Number of cases where wormholes were utilized
    total_savings = 0        # Total computational steps saved across all tests
    
    differences = []         # Detailed list of cases where sequences differed
    
    # Display testing configuration and start message
    print(f"\n[*] Testing sequences equivalence for n <= {max_n}")
    print("")

    # Main testing loop: iterate through all numbers in range
    for n in range(1, max_n + 1):
        
        # Compare sequences generated by both algorithms for current n
        comparison = compare_sequences(n)
        
        # Handle cases where comparison failed due to computational errors
        if "error" in comparison:
            error_count += 1
            print(f"    ERROR n={n}: {comparison['error']}")
            continue
        
        # Process cases where sequences are mathematically identical
        if comparison["sequences_identical"]:
            identical_count += 1
            
            # Track and report wormhole usage statistics
            if comparison["entry_point_info"]["wormhole_used"]:
                entry_points_used += 1
                entry_point_pos = comparison["entry_point_info"]["entry_point_position"]
                wormhole_len = comparison["entry_point_info"]["wormhole_length"]
                total_savings += wormhole_len - 1  # Steps saved by using wormhole
                
                entry_point = comparison["entry_point_info"]["entry_point_found"]
                print(f"\tn={n} uses the wormhole {entry_point} from position {entry_point_pos}, saving {wormhole_len-1} steps")
            else:
                # Case where no wormhole was available or needed
                print(f"\tn={n} uses the trivial cycle, so no saves")

        else:
            # Critical case: sequences differ, indicating potential wormhole error
            different_count += 1
            differences.append(comparison)
            
            # Extract diagnostic information for error reporting
            diff_pos = comparison.get("first_difference_position", "unknown")
            standard_val = comparison.get("standard_value_at_diff", "?")
            wormhole_val = comparison.get("wormhole_value_at_diff", "?")
            print(f"\tn={n} \033[31mSEQUENCES DIFFER\033[0m at position {diff_pos} (standard value is {standard_val} and wormhole is {wormhole_val})")
    
    # Display comprehensive summary of all testing results
    display_equivalence_summary(max_n, identical_count, different_count, error_count, entry_points_used, total_savings, differences)

def display_equivalence_summary(max_n: int, identical_count: int, different_count: int, 
                               error_count: int, entry_points_used: int, total_savings: int,
                               differences: list) -> None:
    """
    Display comprehensive summary of sequence equivalence testing results.
    
    This function generates a detailed report summarizing the results of sequence
    equivalence testing between standard and wormhole algorithms. It provides
    statistical analysis, efficiency metrics, and detailed error reporting to
    help assess the quality and performance of the wormhole optimization.
    
    The summary includes:
    1. Overall testing statistics (counts and percentages)
    2. Wormhole usage and efficiency metrics
    3. Detailed error analysis (if any differences found)
    4. Success/failure determination with clear conclusions
    
    Args:
        max_n (int): The maximum number that was tested (defines the testing range)
        identical_count (int): Number of cases where sequences were exactly identical
        different_count (int): Number of cases where sequences differed
        error_count (int): Number of cases where computation errors occurred
        entry_points_used (int): Number of cases where wormholes were successfully utilized
        total_savings (int): Total computational steps saved across all wormhole usage
        differences (list): Detailed list of comparison results for cases where sequences differed
    
    Returns:
        None: This function prints the summary directly to console.
    
    Console Output Structure:
        - Header section with title
        - Basic statistics (tested, identical, different counts with percentages)
        - Error analysis section:
          * If differences found: detailed breakdown of each discrepancy
          * If no differences: success message with efficiency metrics
        - Wormhole performance metrics:
          * Usage frequency and percentage
          * Total and average computational savings
        - Final conclusion (SUCCESS or ERROR status)
    
    Examples:
        # For successful testing (no differences):
        >>> display_equivalence_summary(100, 98, 0, 2, 45, 2340, [])
        # Outputs success summary with efficiency metrics
        
        # For testing with sequence differences:
        >>> display_equivalence_summary(50, 48, 2, 0, 20, 1200, [diff1, diff2])
        # Outputs detailed error analysis and diagnostic information
    
    Notes:
        - This function is called by test_sequence_equivalence() to present results
        - Provides clear SUCCESS/ERROR determination for quality assurance
        - Essential for identifying wormhole dictionary errors
        - Calculates and displays optimization effectiveness metrics
        - Uses color coding (red) for critical error highlighting
        - Serves as the final report for validation testing
    """
    total_tested = max_n  # Total number of values tested in the range [1, max_n]
    
    # Display formatted summary header
    print("\n" + "=" * 100)
    print("SEQUENCE EQUIVALENCE SUMMARY")
    print("=" * 100)
    
    # Display basic testing statistics with percentages
    print(f"Numbers tested: {total_tested}")
    print(f"Sequences identical: {identical_count} ({100*identical_count/total_tested:.3f}%)")
    print(f"Sequences different: {different_count} ({100*different_count/total_tested:.3f}%)")
      
    # Analyze and report sequence differences (critical errors)
    if different_count > 0:
        # Error case: sequences differ, indicating wormhole dictionary problems
        print(f"Errors: {different_count} sequences are DIFFERENT. This indicates errors in a wormhole sequence.")
        
        # Provide detailed breakdown of each difference found
        if differences:
            print("\nRegistered differences:")
            for i, diff in enumerate(differences):
                n = diff["n"]
                pos = diff.get("first_difference_position", "?")
                standard_val = diff.get("standard_value_at_diff", "?")
                wormhole_val = diff.get("wormhole_value_at_diff", "?")
                print(f"  n={n} differs at position {pos} (expected {standard_val}, got {wormhole_val})")
    else:
        # Success case: all sequences are mathematically identical
        print(f"Errors: {different_count}")
        
        # Display wormhole optimization efficiency metrics (only when successful)
        if entry_points_used > 0:
            print("\nWormholes usage:")
            print(f"  Cases of n using wormholes: {entry_points_used} out of {total_tested} ({100*entry_points_used/total_tested:.3f}%)")
            print(f"  Total steps saved: {total_savings}")
            print(f"  Average steps saved per wormholes: {total_savings/entry_points_used:.3f}")
        
        # Display final success message
        print("\nSUCCESS: All sequences are identical!")
        print("The wormhole algorithm produced exactly the same results as standard algorithm.")
    
    # Display footer
    print("=" * 100)

def display_complete_analysis(n: Union[int, str, float]) -> None:
    """
    Display comprehensive analysis comparing standard and wormhole algorithms for a single input.
    
    This function provides a complete analytical report for a single input number,
    showcasing the differences between standard and wormhole algorithms. It serves
    as the main user interface for demonstrating the capabilities, accuracy, and
    efficiency benefits of the wormhole optimization approach.
    
    The analysis includes:
    1. Input validation and preprocessing
    2. Sequence generation using both algorithms
    3. Visual sequence comparison and representation
    4. Wormhole detection and usage analysis
    5. Mathematical validation of wormhole correctness
    6. Computational efficiency metrics and comparison
    
    Args:
        n (Union[int, str, float]): The input number to analyze. Can be string,
                                   float, or integer format. Will be validated
                                   and converted internally.
    
    Returns:
        None: This function prints comprehensive analysis directly to console.
    
    Console Output Structure:
        - Header with program title and input information
        - Sequence Analysis Section:
          * Standard algorithm sequence (complete path)
          * Wormhole algorithm sequence with visual optimization highlighting
        - Wormhole Detection Section:
          * Entry point information and position
          * Optimization strategy explanation
        - Wormhole Validation Section:
          * Mathematical correctness verification
          * Error reporting if validation fails
        - Computational Efficiency Table:
          * Side-by-side comparison of both algorithms
          * Steps computed, saved, and efficiency percentages
          * Visual highlighting of optimized portions
    
    Examples:
        >>> display_complete_analysis(27)
        # Displays full analysis for n=27 showing wormhole optimization
        
        >>> display_complete_analysis("100")
        # Analyzes n=100 with string input (automatically converted)
        
        >>> display_complete_analysis(1)
        # Shows trivial case analysis
        
        >>> display_complete_analysis("invalid")
        # Displays input validation error
    
    Notes:
        - This is the primary user-facing function for single number analysis
        - Combines all analysis components into a unified, comprehensive report
        - Uses color coding to highlight optimized vs computed portions
        - Provides educational value by showing algorithm differences
        - Essential for demonstrating wormhole optimization benefits
        - Includes robust error handling for all input types
        - Serves as the main interface for the CLI application
    """
    # Display program header with title and formatting
    print("=" * 100)
    print("  COLLATZ TOTAL STOPPING TIME PREDICTOR ")
    print("=" * 100)
    
    try:
        # Validate and convert input to proper integer format
        n_val = validate_input(n)
        print(f"\n[*] ANALYZING n = {n_val}")
        
        # Calculate results using both algorithms for comparison
        standard_result = calculate_standard_total_stopping_time(n_val)
        wormhole_result = calculate_wormhole_total_stopping_time(n_val)
        
        # Check for computational errors in standard algorithm
        if standard_result["total_stopping_time"] < 0:
            print(f"\n[!] ERROR: {standard_result.get('error_message', 'Computation failed')}")
            return
        
        # Check for computational errors in wormhole algorithm
        if wormhole_result["total_stopping_time"] < 0:
            print(f"\n[!] ERROR: {wormhole_result.get('error_message', 'Computation failed')}")
            return
        
        # Display visual sequences comparison and analysis
        display_standard_and_predicted_sequences(n_val, wormhole_result)
        
        # Display detailed wormhole detection and usage information
        display_wormhole_info(wormhole_result)
        
        # Display mathematical validation results for wormhole accuracy
        if "validation" in wormhole_result:
            display_validation_results(wormhole_result["validation"])

        # Display efficiency comparison table (only if validation passed)
        if "validation_failed" not in wormhole_result["prediction_type"]:
            display_efficiency_table(standard_result, wormhole_result)
        
    except ValidationError as e:
        # Handle input validation errors with clear messaging
        print(f"\n[!] INPUT ERROR: {e}")
    except Exception as e:
        # Handle unexpected errors with diagnostic information
        print(f"\n[!] UNEXPECTED ERROR: {e}")

def display_standard_and_predicted_sequences(n: int, wormhole_result: Dict) -> None:
    """
    Display visual comparison between standard and predicted Collatz sequences.
    
    This function creates a side-by-side visual representation of Collatz sequences
    generated by both algorithms, highlighting the computational optimization achieved
    through wormhole usage. It uses color coding to distinguish between computed
    steps and optimized (wormhole) portions of the sequence.
    
    Visual Elements:
    - Standard sequence: Complete step-by-step path with arrow separators
    - Wormhole sequence: Color-coded path showing computed vs optimized portions
    - Orange arrows (computed): Steps calculated manually before wormhole usage
    - Green arrows (wormhole): Steps retrieved from pre-computed wormhole sequence
    
    Args:
        n (int): The input number for which sequences were generated
        wormhole_result (Dict): Results from wormhole algorithm containing:
                               - prediction_type: Type of optimization applied
                               - entry_point_found: Wormhole entry point (if applicable)
                               - entry_point_position: Position where wormhole was triggered
    
    Returns:
        None: This function prints formatted sequences directly to console.
    
    Console Output:
        - Section header for sequence analysis
        - Standard sequence: Complete numerical path with arrow separators
        - Wormhole sequence: Color-coded path showing optimization breakdown
        - Information about sequence lengths and step counts
    
    Examples:
        For n=6 with wormhole at position 1:
        Standard sequence (9 elements and 8 steps):
        6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
        
        Predicted sequence (9 elements and 8 steps):
        6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
        (orange portion: computed, green portion: from wormhole)
    
    Notes:
        - This function provides crucial visual feedback for understanding optimization
        - Color coding helps users distinguish between computed and optimized portions
        - Essential for educational demonstration of wormhole algorithm benefits
        - Handles various scenarios: entry point found, no entry point, trivial cases
        - Uses ANSI escape codes for terminal color formatting
        - Complements the numerical analysis with intuitive visual representation
    """
    print("\n\t= SEQUENCES ANALYSIS:")
    
    # Generate and display the standard (reference) sequence
    try:
        standard_sequence = generate_standard_sequence(n)
        print(f"\n\t   - Standard sequence ({len(standard_sequence)} elements and {len(standard_sequence)-1} steps):")
        
        # Display standard sequence with arrow separators
        print(f"\t   {' → '.join(map(str, standard_sequence))}")
    except Exception as e:
        print(f"\t   Error generating standard sequence: {e}")
        return
    
    # Display wormhole sequence based on optimization result type
    if wormhole_result.get("prediction_type") == "entry_point_found":
        # Case: Wormhole optimization was successfully applied
        entry_point_pos = wormhole_result.get("entry_point_position", 0)
        entry_point_num = wormhole_result.get("entry_point_found")

        # Generate the computed portion (steps before wormhole usage)
        computed_part = []
        current = n
        for i in range(entry_point_pos + 1):
            computed_part.append(current)
            if current != 1:
                current = next_collatz_value(current)
        
        # Extract the wormhole portion from dictionary
        # Skip first element to avoid duplication (already in computed_part)
        if entry_point_num in DICTIONARY:
            wormhole_part = DICTIONARY[entry_point_num]["wormhole"][1:]  
        else:
            wormhole_part = []
        
        # Calculate total predicted sequence length
        predicted_sequence = len(computed_part) + len(wormhole_part)

        print(f"\n\t   - Predicted sequence ({predicted_sequence} elements and {predicted_sequence - 1} steps):")
        
        # Display color-coded sequence:
        # Orange for computed steps, green for wormhole steps
        computed_str = ' \033[38;5;214m→\033[0m '.join(map(str, computed_part))
        wormhole_str = ' \033[32m→\033[0m '.join(map(str, wormhole_part))

        print(f"\t   {computed_str} \033[32m→\033[0m {wormhole_str}")
      
    else:
        # Cases where no wormhole optimization was applied
        if "no_entry_point" in wormhole_result["prediction_type"]:
            print("\n\t   - Predicted sequence: No wormhole available before trivial cycle")
        elif "trivial" in wormhole_result["prediction_type"]:
            print("\n\t   - Predicted sequence: No wormhole needed for trivial cycle")
        else:
            print(f"\n\t   - Predicted sequence: Available wormhole {wormhole_result.get('entry_point_found', 'unknown')} is unusable")

def display_wormhole_info(wormhole_result: Dict) -> None:
    """
    Display detailed information about wormhole detection and optimization strategy.
    
    This function provides comprehensive analysis of wormhole usage, explaining
    the optimization strategy applied and the computational benefits achieved.
    It serves as an educational component to help users understand how the
    wormhole algorithm detects and utilizes pre-computed sequences.
    
    Information displayed includes:
    - Wormhole entry point detection results
    - Position in sequence where optimization was triggered
    - Size and characteristics of the utilized wormhole
    - Optimization strategy explanation based on scenario
    - Efficiency assessment (best case vs worst case scenarios)
    
    Args:
        wormhole_result (Dict): Results from wormhole algorithm containing:
                               - prediction_type: Type of optimization result
                               - entry_point_found: Number that triggered wormhole (if applicable)
                               - entry_point_position: Step where wormhole was detected
                               - wormhole_length: Size of the wormhole sequence used
    
    Returns:
        None: This function prints wormhole analysis directly to console.
    
    Console Output Scenarios:
        1. Entry Point Found:
           - Entry point value and discovery position
           - Wormhole characteristics (length, steps saved)
           - Efficiency assessment (immediate vs delayed discovery)
           - Strategic explanation of the optimization approach
        
        2. No Entry Point:
           - Explanation of worst-case computational scenario
           - Strategy description for trivial cycle completion
    
    Examples:
        For successful wormhole detection:
        = WORMHOLE DETECTION:
        - The wormhole entry point takes the value 91 and it is reached at step 27
        - This is the most efficient situation, when n equals an entry point of wormholes
        - The wormhole has 85 elements (84 steps)
        - Strategy: Compute until it finds an entry point for wormhole, then use it
        
        For no wormhole available:
        = WORMHOLE DETECTION:
        - The wormhole entry point requires full steps, being the worst computational situation
        - Strategy: Compute until repetition happens on the trivial cycle (1, 4, 2, 1)
    
    Notes:
        - This function provides educational value about optimization strategies
        - Helps users understand the computational benefits of wormhole approach
        - Explains the difference between best-case and worst-case scenarios
        - Essential for demonstrating algorithm intelligence and efficiency
        - Complements numerical results with strategic insights
    """
    # Skip wormhole analysis for trivial cases (n=1)
    if "trivial" not in wormhole_result["prediction_type"]:
        
        # Case 1: Wormhole entry point was successfully detected and used
        if wormhole_result.get("prediction_type") == "entry_point_found":
            entry_point = wormhole_result.get("entry_point_found")
            position = wormhole_result.get("entry_point_position")
            wormhole_len = wormhole_result.get("wormhole_length", 0)
            
            print("\n\t= WORMHOLE DETECTION:\n")
            print(f"\t   - The wormhole entry point takes the value {entry_point} and it is reached at step {position}")
            
            # Assess optimization efficiency based on entry point position
            if position == 0:
                # Best case scenario: input number itself is a wormhole entry point
                print("\t   - This is the most efficient situation, when n equals an entry point of wormholes")
            
            # Display wormhole characteristics and size information
            print(f"\t   - The wormhole has {wormhole_len} elements ({wormhole_len-1} steps)")
            print("\t   - Strategy: Compute until it finds an entry point for wormhole, then use it")
        
        else:
            # Case 2: No wormhole entry point was found (worst case scenario)
            print("\n\t= WORMHOLE DETECTION:\n")
            print("\t   - The wormhole entry point requires full steps, being the worst computational situation")
            print("\t   - Strategy: Compute until repetition happens on the trivial cycle (1, 4, 2, 1)")
    
    # Note: Trivial case (n=1 or mr=0) don't require wormhole analysis as they complete immediately

def display_validation_results(validation: Dict) -> None:
    """
    Display mathematical validation results for wormhole sequence accuracy.
    
    This function presents the results of wormhole sequence validation, which
    verifies that pre-computed wormhole sequences are mathematically correct
    by comparing them against actual Collatz computations. It serves as a
    quality assurance component that builds trust in optimization results.
    
    The validation display includes:
    - Pass/fail status of mathematical verification
    - Detailed error analysis if validation fails
    - Diagnostic information for troubleshooting sequence discrepancies
    - Length and content comparison results
    
    Args:
        validation (Dict): Validation results from validate_wormhole_sequence() containing:
                          - valid (bool): Whether wormhole sequence is mathematically correct
                          - error (str): Error description if validation failed
                          - actual_length (int): Length of computed sequence (if length mismatch)
                          - expected_length (int): Length of wormhole sequence (if length mismatch)
                          - position (int): Position of first difference (if content mismatch)
                          - actual_value: Computed value at difference position
                          - expected_value: Wormhole value at difference position
    
    Returns:
        None: This function prints validation results directly to console.
    
    Console Output Scenarios:
        1. Validation Passed:
           = WORMHOLE VALIDATION:
           PASSED: Wormhole sequence matches standard sequence
        
        2. Validation Failed - Length Mismatch:
           = WORMHOLE VALIDATION:
           FAILED: Sequence lengths differ
           - Wormhole length is 85 but standard length is 87
        
        3. Validation Failed - Content Mismatch:
           = WORMHOLE VALIDATION:
           FAILED: Sequences differ at position 15
           - Wormhole value is 52 but standard value is 26
    
    Examples:
        >>> validation = {'valid': True}
        >>> display_validation_results(validation)
        # Outputs success message
        
        >>> validation = {
        ...     'valid': False,
        ...     'error': 'Sequences differ at position 10',
        ...     'position': 10,
        ...     'expected_value': 52,
        ...     'actual_value': 26
        ... }
        >>> display_validation_results(validation)
        # Outputs detailed failure analysis
    
    Notes:
        - This function is critical for maintaining trust in wormhole optimization
        - Provides essential quality assurance feedback for algorithm reliability
        - Helps identify and diagnose errors in wormhole dictionary entries
        - Essential component of the verification workflow
        - Builds confidence in optimization results through mathematical proof
        - Supports debugging and troubleshooting of sequence discrepancies
    """
    print("\n\t= WORMHOLE VALIDATION:\n")
    
    # Check validation status and display appropriate results
    if validation["valid"]:
        # Validation successful: wormhole sequence is mathematically correct
        print("\t   PASSED: Wormhole sequence matches standard sequence")
    else:
        # Validation failed: display detailed error analysis
        print(f"\t   FAILED: {validation['error']}")
        
        # Provide specific diagnostic information based on error type
        
        # Case 1: Sequence length mismatch
        if "actual_length" in validation and "expected_length" in validation:
            print(f"\t   - Wormhole length is {validation['expected_length']} but standard length is {validation['actual_length']}")
        
        # Case 2: Sequence content mismatch at specific position
        if "position" in validation:
            print(f"\t   - Wormhole value is {validation['expected_value']} but standard value is {validation['actual_value']}")

def display_efficiency_table(standard_result: Dict, wormhole_result: Dict) -> None:
    """
    Display comprehensive efficiency comparison table between standard and wormhole algorithms.
    
    This function creates a formatted table that provides side-by-side comparison
    of computational efficiency between the traditional and optimized approaches.
    It serves as the primary performance metrics display, highlighting the
    computational benefits achieved through wormhole optimization.
    
    The efficiency table includes:
    - Total stopping time comparison for both algorithms
    - Breakdown of computed vs saved steps for wormhole algorithm
    - Percentage efficiency gains from optimization
    - Color-coded visualization of optimization components
    - Assessment of wormhole detection effectiveness
    
    Args:
        standard_result (Dict): Results from standard algorithm containing:
                               - total_stopping_time (int): Steps calculated by standard method
        wormhole_result (Dict): Results from wormhole algorithm containing:
                               - total_stopping_time (int): Total steps (computed + saved)
                               - computed_steps (int): Steps calculated manually
                               - saved_steps (int): Steps saved through wormhole usage
    
    Returns:
        None: This function prints formatted efficiency table directly to console.
    
    Table Structure:
        Header: "COMPUTATIONAL EFFICIENCY TABLE"
        Columns: Method | Total Steps | Computed | Saved | % Saved
        Rows:
        - Standard: Shows traditional algorithm metrics (no optimization)
        - Wormhole: Shows optimized algorithm with color-coded breakdown
        
        Color Coding:
        - Orange text: Computed steps (standard calculation)
        - Green text: Saved steps (wormhole optimization)
        - Regular text: Standard algorithm and totals
    
    Examples:
        For n=51 with wormhole optimization (best case):
        ================================================================================
        COMPUTATIONAL EFFICIENCY TABLE
        ================================================================================
        Method               Total Steps  Computed   Saved      % Saved
        --------------------------------------------------------------------------------
        Standard                      24        24       0       0.000%
        Wormhole                      24         0      24     100.000%
        ================================================================================


        For n=27 with wormhole optimization:
        ================================================================================
        COMPUTATIONAL EFFICIENCY TABLE
        ================================================================================
        Method               Total Steps  Computed   Saved      % Saved
        --------------------------------------------------------------------------------
        Standard                     111       111       0       0.000%
        Wormhole                     111        16      95      85.586%
        ================================================================================
        
        For n=84 without wormhole optimization (worst case):
        ================================================================================
        COMPUTATIONAL EFFICIENCY TABLE
        ================================================================================
        Method               Total Steps  Computed   Saved      % Saved
        --------------------------------------------------------------------------------
        Standard                       9         9       0       0.000%
        Wormhole                       9         9       0       0.000%
        ================================================================================
    
    Notes:
        - This function provides the primary performance comparison interface
        - Essential for demonstrating computational benefits of wormhole optimization
        - Uses color coding to visually distinguish optimization components
        - Calculates and displays percentage efficiency gains
        - Provides clear evidence of algorithm effectiveness
        - Critical for performance analysis and algorithm validation
        - Helps users understand the practical benefits of optimization
    """
    # Extract computational metrics from both algorithm results
    standard_time = standard_result.get("total_stopping_time", 0)
    wormhole_time = wormhole_result.get("total_stopping_time", 0)
    computed_steps = wormhole_result.get("computed_steps", 0)
    saved_steps = wormhole_result.get("saved_steps", 0)
    
    # Display formatted table header
    print("\n" + "=" * 100)
    print("COMPUTATIONAL EFFICIENCY TABLE")
    print("=" * 100)
    print(f"{'Method':<20} {'Total Steps':<12} {'Computed':<10} {'Saved':<10} {'% Saved':<12}")
    print("-" * 100)
    
    # Display standard algorithm row (baseline performance)
    print(f"{'Standard':<20} {standard_time:>11} {standard_time:>9} {0:7} {0.0:>11.3f}%")
    
    # Calculate optimization efficiency metrics for wormhole algorithm
    if saved_steps > 0 and standard_time > 0:
        # Case: Wormhole optimization was successfully applied
        saved_pct = (saved_steps / standard_time) * 100
    else:
        # Case: No wormhole optimization available or applied
        saved_pct = 0.0
    
    # Display wormhole algorithm row with color-coded optimization breakdown
    # Orange for computed steps, green for saved steps
    print(f"{'Wormhole':<20} {wormhole_time:>11} \033[38;5;214m{computed_steps:>9}\033[0m \033[32m{saved_steps:7}\033[0m {saved_pct:>11.3f}%")
      
    # Display table footer
    print("=" * 100)

def print_usage():
    """
    Display comprehensive usage information and help documentation for the CLI application.
    
    This function provides complete command-line interface documentation, explaining
    all available commands, their syntax, and practical examples. It serves as the
    primary help system for users to understand how to properly use the Collatz
    total stopping time predictor with wormhole optimization.
    
    The usage information includes:
    - Command syntax and parameter requirements for all operations
    - Available operation modes (single analysis, batch testing, help requests)
    - Practical examples with real inputs and expected behaviors
    - Clear explanations of each command's purpose and use cases
    - Multiple ways to access help information
    
    Args:
        None: This function requires no parameters.
    
    Returns:
        None: This function prints usage documentation directly to console.
    
    Console Output Structure:
        1. Usage Syntax Section:
           - Command format for single number analysis
           - Command format for sequence equivalence testing
           - Command format for help requests (multiple variants)
        
        2. Commands Description Section:
           - Detailed explanation of each available command
           - Parameter requirements and formats
           - Help system access methods
        
        3. Examples Section:
           - Practical examples showing real command usage
           - Different scenarios and use cases
           - Error handling demonstrations
    
    Available Commands Documented:
        1. Single Number Analysis:
           - Syntax: python total_stopping_time_predictor.py <n>
           - Purpose: Analyze one specific number with full comparison
        
        2. Sequence Equivalence Testing:
           - Syntax: python total_stopping_time_predictor.py --test-sequences <max_n>
           - Purpose: Validate algorithm correctness across a range
        
        3. Help Display:
           - Syntax: python total_stopping_time_predictor.py [--help|-h|help]
           - Purpose: Display this usage information
    
    Examples:
        >>> print_usage()
        # Outputs complete usage documentation
        
        Typical usage scenarios:
        - User needs help: python total_stopping_time_predictor.py --help
        - User wants analysis: python total_stopping_time_predictor.py 27
        - User wants validation: python total_stopping_time_predictor.py --test-sequences 1000
        - Invalid input: Shows specific error + suggests --help
    
    Notes:
        - This function is automatically called when insufficient arguments provided
        - Essential for user onboarding and command discovery
        - Provides clear guidance for both beginners and advanced users
        - Documents all available functionality in one place
        - Critical for CLI usability and user experience
        - Should be updated whenever new commands are added
        - Supports multiple help command variants for user convenience
        - Integrates with improved error handling system
    """
    print("Usage:")
    print("  python total_stopping_time_predictor.py <n>")
    print("  python total_stopping_time_predictor.py --test-sequences <max_n>")
    print("  python total_stopping_time_predictor.py [--help | -h | help]")
    print("")
    print("Commands:")
    print("  <n>                      Analyze single number (integer, float, or string)")
    print("  --test-sequences <max_n> Test sequences equivalence from 1 to max_n")
    print("  --help, -h, help         Display this help information")
    print("")
    print("Examples:")
    print("  python total_stopping_time_predictor.py 27")
    print("  python total_stopping_time_predictor.py \"100\"")
    print("  python total_stopping_time_predictor.py 42.0")
    print("  python total_stopping_time_predictor.py --test-sequences 1000")
    print("  python total_stopping_time_predictor.py --help")
    print("")
    print("Input Formats:")
    print("  - Integers: 27, 100, 1")
    print("  - Strings: \"27\", \"100\" (will be converted)")
    print("  - Floats: 27.0, 100.0 (must be whole numbers)")
    print("")
    print("Error Examples:")
    print("  python total_stopping_time_predictor.py abc     # Invalid format")
    print("  python total_stopping_time_predictor.py 3.14    # Not a whole number")
    print("  python total_stopping_time_predictor.py -5      # Must be positive")

def main():
   """
   Main entry point and command-line interface coordinator for the Collatz predictor application.
   
   This function serves as the central dispatcher that processes command-line arguments,
   validates user input, and routes execution to the appropriate analysis or testing
   functions. It provides comprehensive error handling and user feedback for all
   supported operations with improved help system and validation.
   
   Supported Operations:
   1. Single Number Analysis: Comprehensive analysis of one input number
   2. Sequence Equivalence Testing: Batch validation across a range of numbers
   3. Help Display: Usage information via multiple command formats
   
   Command Line Argument Processing:
   - Validates minimum argument requirements
   - Parses and routes commands to appropriate functions
   - Handles numeric inputs, command flags, and help requests
   - Provides specific error messages for different failure types
   - Distinguishes between help requests and invalid inputs
   
   Args:
       None: Uses sys.argv to access command-line arguments directly.
   
   Returns:
       None: This function coordinates execution and exits with appropriate status codes.
   
   Exit Codes:
       - 0: Successful execution or help display
       - 1: Invalid arguments, input errors, or execution failures
   
   Command Line Formats:
       1. python total_stopping_time_predictor.py <n>
          - Performs complete analysis of number n
          - Displays sequences, wormhole info, validation, and efficiency
       
       2. python total_stopping_time_predictor.py --test-sequences <max_n>
          - Tests algorithm equivalence for range [1, max_n]
          - Validates wormhole correctness across multiple inputs
       
       3. python total_stopping_time_predictor.py [--help|-h|help]
          - Displays usage information and exits successfully
       
       4. python total_stopping_time_predictor.py
          - Shows usage information when no arguments provided
   
   Error Handling:
       - Insufficient arguments: Shows usage and exits
       - Invalid numeric inputs: Displays specific validation errors with guidance
       - Help requests: Shows usage and exits successfully
       - Computation interruption: Handles Ctrl+C gracefully
       - Unexpected errors: Captures and reports with diagnostic info
   
   Examples:
       Command line usage:
       $ python total_stopping_time_predictor.py 27
       # Analyzes n=27 with full comparison
       
       $ python total_stopping_time_predictor.py --test-sequences 100
       # Tests equivalence for n=1 to n=100
       
       $ python total_stopping_time_predictor.py --help
       # Shows usage information
       
       $ python total_stopping_time_predictor.py abc
       # Shows "Error: Invalid number format: abc" with help guidance
   
   Notes:
       - This function is the primary entry point for CLI execution
       - Provides robust error handling for all execution paths with specific messaging
       - Essential for user experience and application reliability
       - Handles both interactive and automated execution scenarios
       - Critical for proper application lifecycle management
       - Ensures graceful handling of user interruptions and errors
       - Improved help system allows multiple ways to request usage information
       - Early input validation prevents confusion between help requests and invalid inputs
   """
   try:
       # Validate minimum command-line argument requirements
       if len(sys.argv) < 2:
           print_usage()
           sys.exit(1)
       
       # Extract the primary command from command-line arguments
       command = sys.argv[1]
       
       # Route 1: Sequence equivalence testing command
       if command == "--test-sequences":
           # Validate that maximum number parameter is provided
           if len(sys.argv) < 3:
               print("Error: --test-sequences requires a maximum number")
               sys.exit(1)
           try:
               # Parse and validate the maximum number for testing range
               max_n = int(sys.argv[2])
               test_sequence_equivalence(max_n)
           except ValueError:
               # Handle invalid integer conversion for test range parameter
               print("Error: Maximum number must be an integer")
               sys.exit(1)
               
       # Route 2: Help command variants (multiple formats supported)
       elif command in ["--help", "-h", "help"]:
           # Display usage information and exit successfully
           print_usage()
           sys.exit(0)
           
       else:
           # Route 3: Single number analysis command
           try:
               # Perform early input validation to distinguish between help requests and invalid numbers
               # This prevents confusion where invalid inputs might be interpreted as help requests
               validate_input(command)  # Raises ValidationError for invalid formats
               
               # Input validation passed - proceed with comprehensive analysis
               display_complete_analysis(command)
               
           except ValidationError as e:
               # Handle specific input validation errors with clear messaging
               # Provide specific error details and guidance for proper usage
               print(f"Error: {e}")
               print("\nUse --help for usage information")
               sys.exit(1)
       
   except KeyboardInterrupt:
       # Handle user interruption (Ctrl+C) gracefully
       print("\n\n[!] Computation interrupted by user")
       sys.exit(1)
   except Exception as e:
       # Handle unexpected errors with diagnostic information
       # This catches system-level errors that shouldn't normally occur
       print(f"\n[!] UNEXPECTED ERROR: {e}")
       sys.exit(1)

if __name__ == "__main__":
    main()


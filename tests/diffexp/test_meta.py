import unittest

import numpy as np
import pandas as pd
import patsy

from inmoose.deseq2 import DESeq, makeExampleDESeqDataSet
from inmoose.diffexp import meta_de
from inmoose.edgepy import (
    DGEList,
    exactTest,
    glmLRT,
    glmQLFTest,
)
from inmoose.utils import Factor


class Test(unittest.TestCase):
    def test_meta_de(self):
        # test contrasts
        dds = makeExampleDESeqDataSet(n=200, m=12, seed=42)
        dds.obs["condition"] = Factor(np.repeat([1, 2, 3], 4))
        dds.obs["group"] = Factor(np.repeat([[1, 2]], 6, axis=0).flatten())
        dds.counts()[:, 0] = np.repeat([100, 200, 800], 4)

        dds.design = "~ group + condition"

        # DE with deseq
        dds = DESeq(dds)
        deseq_res = dds.results()

        # DE with edgepy
        d = DGEList(counts=dds.X.T, group=dds.obs["group"])
        d.design = patsy.dmatrix("~ group + condition", data=dds.obs)
        d = d.estimateGLMCommonDisp()

        # DE with edgepy (LRT)
        edgepy_lrt_res = glmLRT(d.glmFit())

        # DE with edgepy (QL FTest)
        edgepy_ql_res = glmQLFTest(d.glmQLFit())

        # DE with edgepy (exactTest)
        edgepy_et_res = exactTest(d)

        # meta-analysis
        des = [deseq_res, edgepy_lrt_res, edgepy_ql_res, edgepy_et_res]
        res = meta_de(des)

        # combined logFC and confidence intervals are controlled against metafor
        # adjusted p-values have no external control, and are tested for non-regression
        ref = pd.DataFrame(
            {
                "combined logFC (CI_L)": [
                    0.6660657,
                    -2.638616,
                    -2.429432,
                    -0.6488383,
                    -2.917037,
                    -3.52156,
                    -0.01365081,
                    -2.444326,
                    -3.028743,
                    -1.263186,
                    -0.456557,
                    -1.050503,
                    -2.898566,
                    -0.5980744,
                    0.5429505,
                    -2.584285,
                    -1.488159,
                    0.208276,
                    -1.621918,
                    -2.175473,
                    -2.426635,
                    -2.286186,
                    0.6061967,
                    -1.798878,
                    -1.391178,
                    -1.67809,
                    -1.560724,
                    -2.731347,
                    -1.819602,
                    -1.84617,
                    -2.396325,
                    -4.150703,
                    -0.8666001,
                    -1.620893,
                    -1.393245,
                    0.06545047,
                    -0.8614611,
                    -0.8949071,
                    -0.1884833,
                    -2.320647,
                    -1.077905,
                    0.3780096,
                    -0.5536221,
                    -0.2144249,
                    -1.037782,
                    -2.037172,
                    -2.460591,
                    -0.4321364,
                    -0.2907081,
                    -0.853905,
                    -1.234255,
                    -2.715667,
                    -2.858242,
                    -1.274542,
                    -2.231896,
                    -1.827964,
                    -4.48086,
                    -0.8010444,
                    -1.979988,
                    -1.052442,
                    -0.1498251,
                    -2.544939,
                    -1.064094,
                    -0.8654656,
                    -3.137638,
                    -0.1053483,
                    -2.518976,
                    -2.015878,
                    -1.672846,
                    -0.5029531,
                    -2.711308,
                    -1.608055,
                    -0.1274361,
                    -0.8225335,
                    -1.772431,
                    -0.9259632,
                    -2.313224,
                    -2.206875,
                    -1.786641,
                    -1.026217,
                    -1.641969,
                    0.2736535,
                    -1.675496,
                    -2.418858,
                    -1.157725,
                    -2.243299,
                    -1.561799,
                    -2.954499,
                    -1.458976,
                    -2.40793,
                    0.410919,
                    0.7039926,
                    -1.773036,
                    -0.3511326,
                    -2.296659,
                    -1.495351,
                    0.4109465,
                    -1.620848,
                    -4.38571,
                    -1.264747,
                    -1.090455,
                    -1.040299,
                    -1.992165,
                    -1.021515,
                    -1.620087,
                    -2.34976,
                    -0.9989291,
                    -5.33652,
                    -1.062335,
                    -0.4845133,
                    -1.109223,
                    -3.022694,
                    -0.7787927,
                    -1.714529,
                    -1.302861,
                    -3.63546,
                    -1.744977,
                    -0.3736545,
                    -1.006341,
                    -3.121721,
                    -0.959403,
                    -1.106849,
                    -1.497546,
                    -2.515283,
                    -0.9689464,
                    -0.04382822,
                    -0.3715107,
                    0.2678246,
                    -2.38558,
                    -0.915764,
                    -1.830163,
                    0.07465597,
                    -1.835387,
                    -3.390986,
                    0.02305774,
                    -1.99897,
                    -0.6785349,
                    -2.309768,
                    -1.294799,
                    0.3533007,
                    -1.012756,
                    -2.176784,
                    -1.531505,
                    0.6837069,
                    -2.239762,
                    -1.891175,
                    -4.78417,
                    -1.791808,
                    -1.92952,
                    -0.7339697,
                    -1.847703,
                    -2.384345,
                    -1.24246,
                    -1.245264,
                    -1.215858,
                    -1.963194,
                    -1.80148,
                    -0.2661707,
                    -1.559986,
                    -4.881915,
                    -3.749383,
                    -2.673076,
                    -1.536772,
                    -2.191867,
                    -1.949768,
                    -0.1254793,
                    -2.700772,
                    -1.472404,
                    -1.145443,
                    -3.115471,
                    -1.008458,
                    -0.3941016,
                    0.2856675,
                    -1.971123,
                    -3.749761,
                    -2.212603,
                    -0.8542665,
                    -1.928418,
                    -2.264775,
                    -3.727507,
                    -0.5539223,
                    -2.474551,
                    -0.9685612,
                    -0.9891179,
                    -0.7883775,
                    -1.604532,
                    -0.7653837,
                    -4.289158,
                    -3.523464,
                    -1.387753,
                    -0.4355646,
                    -0.4168414,
                    0.09406679,
                    -0.02088534,
                    -0.9952664,
                    -0.09151924,
                    -0.4315687,
                    -2.814548,
                    -0.9964442,
                    -1.393898,
                ],
                "combined logFC (CI_R)": [
                    3.354889,
                    -0.3406019,
                    0.3507641,
                    1.275798,
                    0.9873886,
                    -0.4388773,
                    2.135552,
                    0.507954,
                    -0.5344569,
                    3.472266,
                    1.536055,
                    0.8514408,
                    -0.8177234,
                    1.447342,
                    2.630398,
                    -0.03615024,
                    0.4964041,
                    2.958852,
                    0.3827889,
                    -0.02245263,
                    0.7755823,
                    -0.03230218,
                    2.560625,
                    0.4279998,
                    0.666364,
                    1.033583,
                    0.4703255,
                    -0.7450826,
                    1.282675,
                    0.2234225,
                    -0.4258294,
                    -1.037856,
                    1.474182,
                    0.9832282,
                    0.597971,
                    1.953745,
                    1.409398,
                    1.30454,
                    2.076679,
                    -0.2807324,
                    0.9447316,
                    2.343681,
                    1.818317,
                    1.88609,
                    1.077479,
                    0.01448438,
                    -0.3565443,
                    1.665693,
                    1.737118,
                    1.693466,
                    0.7287407,
                    -0.4582677,
                    0.4721933,
                    0.7525166,
                    -0.05059457,
                    0.6663768,
                    -0.3611993,
                    1.132683,
                    1.909296,
                    1.622502,
                    2.836743,
                    -0.4676246,
                    0.9555605,
                    1.153756,
                    0.4719316,
                    1.894036,
                    -0.3702007,
                    0.5147398,
                    0.3746913,
                    3.582514,
                    1.266965,
                    2.215796,
                    3.071118,
                    1.181279,
                    0.1898259,
                    1.110582,
                    -0.1277235,
                    -0.1845316,
                    0.2583357,
                    1.177484,
                    0.3506867,
                    2.795973,
                    0.6503708,
                    -0.027063,
                    1.571159,
                    0.4519646,
                    0.5671997,
                    0.7660795,
                    0.5643178,
                    -0.2691874,
                    2.366717,
                    2.775334,
                    0.4112966,
                    1.96953,
                    1.284392,
                    0.938036,
                    3.274204,
                    0.6589823,
                    0.7505066,
                    2.018853,
                    1.056194,
                    0.9507686,
                    0.593813,
                    1.049412,
                    1.507697,
                    0.9887645,
                    4.264976,
                    1.032761,
                    0.8621269,
                    4.993459,
                    0.9498576,
                    -0.85167,
                    1.479518,
                    0.8748808,
                    0.7724491,
                    0.8436216,
                    0.3887228,
                    1.699635,
                    1.018062,
                    -0.8432674,
                    1.853741,
                    0.8959239,
                    0.4776082,
                    -0.6123595,
                    0.9675708,
                    1.994197,
                    2.532303,
                    2.613784,
                    0.06386712,
                    1.347378,
                    0.2707202,
                    4.160242,
                    0.32248,
                    -0.9166967,
                    2.691808,
                    0.5290254,
                    1.274141,
                    0.1212208,
                    0.5949143,
                    2.316759,
                    1.011051,
                    0.6586181,
                    3.422986,
                    2.742162,
                    1.551273,
                    0.2595654,
                    0.2017533,
                    0.990346,
                    0.01583118,
                    1.285109,
                    0.7354634,
                    0.8106343,
                    2.436099,
                    1.069948,
                    0.8751374,
                    0.05079275,
                    0.2276947,
                    1.646944,
                    1.8052,
                    -0.6863327,
                    0.7657421,
                    -0.4894167,
                    0.3473246,
                    0.9672352,
                    0.3729598,
                    2.348066,
                    0.2250868,
                    0.606701,
                    0.8955957,
                    -0.6950406,
                    1.313918,
                    1.640593,
                    2.681893,
                    0.7671767,
                    2.819406,
                    -0.1852888,
                    1.047644,
                    0.5922181,
                    -0.08493847,
                    -0.731192,
                    1.335098,
                    -0.4399274,
                    1.151133,
                    1.743973,
                    1.259147,
                    0.4065491,
                    1.260736,
                    -1.182831,
                    -0.9549424,
                    0.5751319,
                    1.47758,
                    1.830319,
                    2.461452,
                    1.929821,
                    1.351807,
                    2.209115,
                    1.532192,
                    -0.4678067,
                    1.005539,
                    0.8993295,
                ],
                "combined logFC": [
                    2.010478,
                    -1.489609,
                    -1.039334,
                    0.3134801,
                    -0.9648241,
                    -1.980219,
                    1.060951,
                    -0.9681862,
                    -1.7816,
                    1.10454,
                    0.5397492,
                    -0.09953092,
                    -1.858145,
                    0.4246338,
                    1.586674,
                    -1.310218,
                    -0.4958774,
                    1.583564,
                    -0.6195647,
                    -1.098963,
                    -0.8255263,
                    -1.159244,
                    1.583411,
                    -0.6854391,
                    -0.3624068,
                    -0.3222534,
                    -0.5451992,
                    -1.738215,
                    -0.2684631,
                    -0.8113736,
                    -1.411077,
                    -2.594279,
                    0.303791,
                    -0.3188325,
                    -0.3976369,
                    1.009598,
                    0.2739685,
                    0.2048163,
                    0.9440976,
                    -1.30069,
                    -0.06658693,
                    1.360845,
                    0.6323475,
                    0.8358326,
                    0.0198485,
                    -1.011344,
                    -1.408568,
                    0.6167781,
                    0.7232051,
                    0.4197804,
                    -0.2527572,
                    -1.586967,
                    -1.193024,
                    -0.2610127,
                    -1.141245,
                    -0.5807935,
                    -2.421029,
                    0.1658193,
                    -0.03534601,
                    0.2850299,
                    1.343459,
                    -1.506282,
                    -0.0542666,
                    0.1441452,
                    -1.332853,
                    0.8943437,
                    -1.444588,
                    -0.7505689,
                    -0.6490772,
                    1.539781,
                    -0.7221715,
                    0.3038704,
                    1.471841,
                    0.1793728,
                    -0.7913028,
                    0.0923096,
                    -1.220474,
                    -1.195704,
                    -0.7641526,
                    0.07563329,
                    -0.645641,
                    1.534813,
                    -0.5125626,
                    -1.22296,
                    0.2067171,
                    -0.8956671,
                    -0.4972997,
                    -1.09421,
                    -0.4473289,
                    -1.338559,
                    1.388818,
                    1.739664,
                    -0.6808697,
                    0.8091988,
                    -0.5061337,
                    -0.2786576,
                    1.842576,
                    -0.480933,
                    -1.817602,
                    0.3770527,
                    -0.01713061,
                    -0.04476523,
                    -0.699176,
                    0.01394839,
                    -0.05619496,
                    -0.6804977,
                    1.633024,
                    -2.15188,
                    -0.1001042,
                    2.254473,
                    -0.07968273,
                    -1.937182,
                    0.3503627,
                    -0.4198238,
                    -0.2652057,
                    -1.395919,
                    -0.678127,
                    0.6629902,
                    0.005860719,
                    -1.982494,
                    0.447169,
                    -0.1054624,
                    -0.509969,
                    -1.563821,
                    -0.0006877722,
                    0.9751843,
                    1.080396,
                    1.440804,
                    -1.160856,
                    0.2158071,
                    -0.7797215,
                    2.117449,
                    -0.7564535,
                    -2.153841,
                    1.357433,
                    -0.7349724,
                    0.297803,
                    -1.094274,
                    -0.3499423,
                    1.33503,
                    -0.0008523571,
                    -0.759083,
                    0.9457402,
                    1.712934,
                    -0.3442446,
                    -0.8158046,
                    -2.291208,
                    -0.4007311,
                    -0.9568442,
                    0.2755698,
                    -0.5561198,
                    -0.7868555,
                    0.59682,
                    -0.08765797,
                    -0.1703605,
                    -0.9562008,
                    -0.7868926,
                    0.6903867,
                    0.1226069,
                    -2.784124,
                    -1.49182,
                    -1.581246,
                    -0.5947239,
                    -0.612316,
                    -0.7884042,
                    1.111293,
                    -1.237843,
                    -0.4328515,
                    -0.1249234,
                    -1.905256,
                    0.15273,
                    0.6232456,
                    1.48378,
                    -0.6019732,
                    -0.4651772,
                    -1.198946,
                    0.09668897,
                    -0.6680998,
                    -1.174857,
                    -2.22935,
                    0.390588,
                    -1.457239,
                    0.09128597,
                    0.3774276,
                    0.2353845,
                    -0.5989912,
                    0.2476762,
                    -2.735994,
                    -2.239203,
                    -0.4063107,
                    0.5210076,
                    0.7067387,
                    1.277759,
                    0.9544677,
                    0.1782704,
                    1.058798,
                    0.5503115,
                    -1.641177,
                    0.004547307,
                    -0.2472841,
                ],
                "adjusted combined pval": [
                    0.0026962055769339036,
                    0.5492995320924478,
                    0.3717988406113749,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.4083482854057524,
                    0.8648125056846707,
                    0.45376604257140674,
                    0.24898009978578023,
                    0.20613484938735,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.24898009978578023,
                    0.9999997373076358,
                    0.4083482854057524,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.6412446477384811,
                    0.9999997373076358,
                    0.8554201391327344,
                    0.5773569285338753,
                    0.8554201391327344,
                    0.3717988406113749,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9337779798059708,
                    0.9999997373076358,
                    0.23199332126061678,
                    0.5323800119077443,
                    0.9337779798059708,
                    0.5069104347963476,
                    0.09169307689370351,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.6950653732452584,
                    0.9999997373076358,
                    0.5638214872001241,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9657733125497636,
                    0.6489853768446933,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.8063045776078286,
                    0.9999997373076358,
                    0.3717988406113749,
                    0.8788695045788074,
                    0.9999997373076358,
                    0.8554201391327344,
                    0.9999997373076358,
                    0.023513048931694414,
                    0.9999997373076358,
                    0.43720476002936304,
                    0.7001493166166863,
                    0.95496623596766,
                    0.5323800119077443,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.19148422048586122,
                    0.9999997373076358,
                    0.6680685982400918,
                    0.7138062253262515,
                    0.9999997373076358,
                    0.14354979249344452,
                    0.5773569285338753,
                    0.9999997373076358,
                    0.5323800119077443,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.8554201391327344,
                    0.6950653732452584,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.6950653732452584,
                    0.9999997373076358,
                    0.45376604257140674,
                    0.9999997373076358,
                    0.5323800119077443,
                    0.9999997373076358,
                    0.1925334445297035,
                    0.9999997373076358,
                    0.7138062253262515,
                    0.5483132749191476,
                    0.34719873490868014,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.5323800119077443,
                    0.9999997373076358,
                    0.01734828761388802,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.8554201391327344,
                    0.5505424235986892,
                    0.1371664212974334,
                    0.014421550092208994,
                    0.9999997373076358,
                    0.24898009978578023,
                    0.9999997373076358,
                    0.3717988406113749,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.18160524927861743,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.24898009978578023,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.24898009978578023,
                    0.9999997373076358,
                    0.95496623596766,
                    0.4513009545412259,
                    0.6760656421075416,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.1476278213988649,
                    0.8654642644197182,
                    0.1371664212974334,
                    0.7951450709166044,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.43720476002936304,
                    0.9999997373076358,
                    0.5638214872001241,
                    0.9999997373076358,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.43720476002936304,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.046911195207150806,
                    0.8654642644197182,
                    0.8554201391327344,
                    0.9999997373076358,
                    0.8513604459312287,
                    0.6412446477384811,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9680888295875392,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.7223520735076792,
                    0.023513048931694414,
                    0.1925334445297035,
                    0.4991530373596115,
                    0.9999997373076358,
                    0.8788695045788074,
                    0.5323800119077443,
                    0.9999997373076358,
                    0.3026815665977687,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.1925334445297035,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.033702016177307635,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.7198760747712619,
                    0.95496623596766,
                    0.18160524927861743,
                    0.9999997373076358,
                    0.5505424235986892,
                    0.9999997373076358,
                    0.7198760747712619,
                    0.9999997373076358,
                    0.9850173529386833,
                    0.9999997373076358,
                    0.046911195207150806,
                    0.1925334445297035,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.8554201391327344,
                    0.9424939688866273,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.9999997373076358,
                    0.5773569285338753,
                    0.9999997373076358,
                    0.9999997373076358,
                ],
            },
            index=[f"gene{i}" for i in range(200)],
        )
        pd.testing.assert_frame_equal(res, ref, rtol=1e-4)

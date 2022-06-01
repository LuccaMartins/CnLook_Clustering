

event_detection_methods = ['I-VT',
                           #TODO:
                           # 'I-DT',
                           # 'REMODNAV',
                           # 'NSLR-HMM'
                           ]

clustering_methods = [
                      'DBSCAN',
                      'K-Means',
                       'FOSC'
                     ]
subsets_of_features = {

                    # -------------- 2 FEATURES -------------------

                    # 0: ['FC', 'AFD'],
                    # 1: ['FC', 'AFDisp'],
                    # 2: ['FC', 'AFDispH'],  # no result over 6.5 silhouette
                    # 3: ['FC', 'AFDispV'],  # no result over 6.5 silhouette
                    # 4: ['FC', 'ASA'],  # no result over 6.5 silhouette
                    # 5: ['FC', 'SPL'],
                    # 6: ['FC', 'ADT'],  # no result over 6.5 silhouette
                    # 7: ['FC', 'ADpFF'],  # no result over 6.5 silhouette
                    # 8: ['FC', 'ADTF'],
                    # 9: ['FC', 'ADB'],
                    #
                    # 10: ['AFD', 'AFDisp'],  # no result over 6.5 silhouette
                    # 11: ['AFD', 'AFDispH'],  # no result over 6.5 silhouette
                    # 12: ['AFD', 'AFDispV'],  # no result over 6.5 silhouette
                    # 13: ['AFD', 'ASA'],  # no result over 6.5 silhouette
                    # 14: ['AFD', 'SPL'],  # no result over 6.5 silhouette
                    # 15: ['AFD', 'ADT'],  # no result over 6.5 silhouette
                    # 16: ['AFD', 'ADpFF'],  # no result over 6.5 silhouette
                    # 17: ['AFD', 'ADTF'],  # no result over 6.5 silhouette
                    # 18: ['AFD', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 19: ['AFDisp', 'AFDispH'],
                    # 20: ['AFDisp', 'AFDispV'],
                    # 21: ['AFDisp', 'ASA'],  # no result over 6.5 silhouette
                    # 22: ['AFDisp', 'SPL'],
                    # 23: ['AFDisp', 'ADT'],  # no result over 6.5 silhouette
                    # 24: ['AFDisp', 'ADpFF'],  # no result over 6.5 silhouette
                    # 25: ['AFDisp', 'ADTF'],  # no result over 6.5 silhouette
                    # 26: ['AFDisp', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 27: ['ASA', 'SPL'],  # no result over 6.5 silhouette
                    # 28: ['ASA', 'ADT'],  # no result over 6.5 silhouette
                    # 29: ['ASA', 'ADpFF'],  # no result over 6.5 silhouette
                    # 30: ['ASA', 'ADTF'],  # no result over 6.5 silhouette
                    # 31: ['ASA', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 32: ['SPL', 'ADT'],  # no result over 6.5 silhouette
                    # 33: ['SPL', 'ADpFF'],  # no result over 6.5 silhouette
                    # 34: ['SPL', 'ADTF'],  # no result over 6.5 silhouette
                    # 35: ['SPL', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 36: ['ADT', 'ADpFF'],  # no result over 6.5 silhouette
                    # 37: ['ADT', 'ADTF'],  # no result over 6.5 silhouette
                    # 39: ['ADT', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 40: ['ADpFF', 'ADTF'],  # no result over 6.5 silhouette
                    # 41: ['ADpFF', 'ADB'],  # no result over 6.5 silhouette
                    #
                    # 42: ['ADTF', 'ADB']


                    # -------------- 3 FEATURES -------------------

                    43: ['FC', 'AFD', 'AFDisp'],  # no result over 6 silhouette
                    44: ['FC', 'AFD', 'AFDispH'],  # no result over 6 silhouette
                    45: ['FC', 'AFD', 'AFDispV'],  # no result over 6 silhouette
                    46: ['FC', 'AFD', 'ASA'],  # no result over 6 silhouette
                    47: ['FC', 'AFD', 'SPL'],  # no result over 6 silhouette
                    48: ['FC', 'AFD', 'ADT'],  # no result over 6 silhouette
                    49: ['FC', 'AFD', 'ADpFF'],  # no result over 6 silhouette
                    50: ['FC', 'AFD', 'ADTF'],  # no result over 6 silhouette
                    51: ['FC', 'AFD', 'ADB'],  # no result over 6 silhouette


                    52: ['FC', 'AFDisp', 'AFDispH'],
                    53: ['FC', 'AFDisp', 'AFDispV'],
                    54: ['FC', 'AFDisp', 'ASA'],  # no result over 6 silhouette
                    55: ['FC', 'AFDisp', 'SPL'],
                    56: ['FC', 'AFDisp', 'ADT'],  # no result over 6 silhouette
                    57: ['FC', 'AFDisp', 'ADpFF'],  # no result over 6 silhouette
                    58: ['FC', 'AFDisp', 'ADTF'],  # no result over 6 silhouette
                    59: ['FC', 'AFDisp', 'ADB'],  # no result over 6 silhouette


                    60: ['FC', 'SPL', 'AFDispH'],
                    61: ['FC', 'SPL', 'AFDispV'],  # no result over 6 silhouette
                    62: ['FC', 'SPL', 'ASA'],  # no result over 6 silhouette
                    63: ['FC', 'SPL', 'ADT'],  # no result over 6 silhouette
                    64: ['FC', 'SPL', 'ADpFF'],  # no result over 6 silhouette
                    65: ['FC', 'SPL', 'ADTF'],  # no result over 6 silhouette
                    66: ['FC', 'SPL', 'ADB'],  # no result over 6 silhouette


                    67: ['FC', 'ADTF', 'AFDispH'],  # no result over 6 silhouette
                    68: ['FC', 'ADTF', 'AFDispV'],  # no result over 6 silhouette
                    69: ['FC', 'ADTF', 'ASA'],  # no result over 6 silhouette
                    70: ['FC', 'ADTF', 'ADT'],  # no result over 6 silhouette
                    71: ['FC', 'ADTF', 'ADpFF'],  # no result over 6 silhouette
                    72: ['FC', 'ADTF', 'ADB'],  # no result over 6 silhouette


                    73: ['FC', 'ADB', 'AFDispH'],  # no result over 6 silhouette
                    74: ['FC', 'ADB', 'AFDispV'],  # no result over 6 silhouette
                    75: ['FC', 'ADB', 'ASA'],  # no result over 6 silhouette
                    76: ['FC', 'ADB', 'ADT'],  # no result over 6 silhouette
                    77: ['FC', 'ADB', 'ADpFF'],  # no result over 6 silhouette
                    # 78: ['FC', 'ADB', 'ADB'], - invalid


                    79: ['AFDisp', 'AFDispH', 'AFD'],  # no result over 6 silhouette
                    80: ['AFDisp', 'AFDispH', 'ASA'],  # no result over 6 silhouette
                    81: ['AFDisp', 'AFDispH', 'SPL'],
                    82: ['AFDisp', 'AFDispH', 'ADT'],  # no result over 6 silhouette
                    83: ['AFDisp', 'AFDispH', 'ADpFF'],  # no result over 6 silhouette
                    84: ['AFDisp', 'AFDispH', 'ADTF'],
                    85: ['AFDisp', 'AFDispH', 'ADB'],


                    86: ['AFDisp', 'AFDispV', 'AFD'],
                    87: ['AFDisp', 'AFDispV', 'ASA'],
                    88: ['AFDisp', 'AFDispV', 'SPL'],
                    89: ['AFDisp', 'AFDispV', 'ADT'],
                    90: ['AFDisp', 'AFDispV', 'ADpFF'],
                    91: ['AFDisp', 'AFDispV', 'ADTF'],
                    92: ['AFDisp', 'AFDispV', 'ADB'],


                    93: ['AFDisp', 'SPL', 'ASA'],  # no result over 6 silhouette
                    94: ['AFDisp', 'SPL', 'ADT'],  # no result over 6 silhouette
                    95: ['AFDisp', 'SPL', 'ADpFF'],  # no result over 6 silhouette
                    96: ['AFDisp', 'SPL', 'ADTF'],
                    97: ['AFDisp', 'SPL', 'ADB'],


                    98: ['ADTF', 'ADB', 'FC'],  # no result over 6 silhouette
                    99: ['ADTF', 'ADB', 'AFD'],  # no result over 6 silhouette
                    100: ['ADTF', 'ADB', 'AFDisp'],  # no result over 6 silhouette
                    101: ['ADTF', 'ADB', 'AFDispH'],  # no result over 6 silhouette
                    102: ['ADTF', 'ADB', 'AFDispV'],  # no result over 6 silhouette
                    103: ['ADTF', 'ADB', 'ASA'],  # no result over 6 silhouette
                    104: ['ADTF', 'ADB', 'SPL'],  # no result over 6 silhouette
                    105: ['ADTF', 'ADB', 'ADT'],  # no result over 6 silhouette
                    106: ['ADTF', 'ADB', 'ADpFF'],  # no result over 6 silhouette


                    107: ['ADT', 'FC', 'AFD'],  # no result over 6 silhouette
                    108: ['ADT', 'FC', 'AFDisp'],  # no result over 6 silhouette
                    109: ['ADT', 'FC', 'AFDispH'],  # no result over 6 silhouette
                    110: ['ADT', 'FC', 'AFDispV'],  # no result over 6 silhouette
                    111: ['ADT', 'FC', 'ASA'],  # no result over 6 silhouette
                    112: ['ADT', 'FC', 'SPL'],  # no result over 6 silhouette
                    113: ['ADT', 'FC', 'ADpFF'],  # no result over 6 silhouette
                    114: ['ADT', 'FC', 'ADTF'],  # no result over 6 silhouette
                    115: ['ADT', 'FC', 'ADB'],  # no result over 6 silhouette

                    116: ['ADT', 'ADB', 'AFD'],  # no result over 6 silhouette
                    117: ['ADT', 'ADB', 'AFDisp'],  # no result over 6 silhouette
                    118: ['ADT', 'ADB', 'AFDispH'],  # no result over 6 silhouette
                    119: ['ADT', 'ADB', 'AFDispV'],  # no result over 6 silhouette
                    120: ['ADT', 'ADB', 'ASA'],  # no result over 6 silhouette
                    121: ['ADT', 'ADB', 'SPL'],  # no result over 6 silhouette
                    122: ['ADT', 'ADB', 'ADpFF'],  # no result over 6 silhouette
                    123: ['ADT', 'ADB', 'ADTF'],  # no result over 6 silhouette
                    124: ['ADT', 'ADB', 'FC'],  # no result over 6 silhouette

                    125: ['ADpFF', 'ADB', 'AFD'],  # no result over 6 silhouette
                    126: ['ADpFF', 'ADB', 'AFDisp'],  # no result over 6 silhouette
                    127: ['ADpFF', 'ADB', 'AFDispH'],  # no result over 6 silhouette
                    128: ['ADpFF', 'ADB', 'AFDispV'],  # no result over 6 silhouette
                    129: ['ADpFF', 'ADB', 'ASA'],  # no result over 6 silhouette
                    130: ['ADpFF', 'ADB', 'SPL'],  # no result over 6 silhouette
                    131: ['ADpFF', 'ADB', 'ADTF'],  # no result over 6 silhouette
                    132: ['ADpFF', 'ADB', 'FC'],  # no result over 6 silhouette





}

eyes_combination = [
                    'both',
                    'left',
                    'right'
                   ]



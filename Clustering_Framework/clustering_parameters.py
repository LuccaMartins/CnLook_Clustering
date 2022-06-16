

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
# subsets_of_features = {
#     0: ['FC', 'ADTF', 'AFD', 'FDMax', 'FDMin'],
#     1: ['FC', 'ADTF', 'AFD', 'ASD', 'FDMin']
# }

#
#                     # -------------- 2 FEATURES -------------------
#
#                     0: ['FC', 'AFD'],
#                     # 1: ['FC', 'AFDisp'],
#                     # 2: ['FC', 'AFDispH'],
#                     # 3: ['FC', 'AFDispV'],
#                     # 4: ['FC', 'ASA'],
#                     5: ['FC', 'SPL'],
#                     6: ['FC', 'ADT'],
#                     7: ['FC', 'ADpFF'],
#                     8: ['FC', 'ADTF'],
#                     9: ['FC', 'ADB'],
#                     # 10: ['FC', 'ADpFFL'],
#                     # 11: ['FC', 'ADpFFR'],
#                     # 11: ['FC', 'ADFF'],
#                     # #
#                     # 10: ['AFD', 'AFDisp'],
#                     # 11: ['AFD', 'AFDispH'],
#                     # 12: ['AFD', 'AFDispV'],
#                     # 13: ['AFD', 'ASA'],
#                     # 14: ['AFD', 'SPL'],
#                     # 15: ['AFD', 'ADT'],
#                     16: ['AFD', 'ADpFF'],
#                     # 17: ['AFD', 'ADTF'],
#                     18: ['AFD', 'ADB'],
#
#                     19: ['AFDisp', 'AFDispH'],
#                     20: ['AFDisp', 'AFDispV'],
#                     # 21: ['AFDisp', 'ASA'],
#                     # 22: ['AFDisp', 'SPL'],
#                     23: ['AFDisp', 'ADT'],
#                     24: ['AFDisp', 'ADpFF'],
#                     # 25: ['AFDisp', 'ADTF'],
#                     26: ['AFDisp', 'ADB'],
#                     #
#                     # 27: ['ASA', 'SPL'],
#                     # 28: ['ASA', 'ADT'],
#                     # 29: ['ASA', 'ADpFF'],
#                     # 30: ['ASA', 'ADTF'],
#                     31: ['ASA', 'ADB'],
#                     #
#                     # 32: ['SPL', 'ADT'],
#                     # 33: ['SPL', 'ADpFF'],
#                     # 34: ['SPL', 'ADTF'],
#                     35: ['SPL', 'ADB'],
#                     #
#                     36: ['ADT', 'ADpFF'],
#                     37: ['ADT', 'ADTF'],
#                     39: ['ADT', 'ADB'],
#                     #
#                     40: ['ADpFF', 'ADTF'],
#                     41: ['ADpFF', 'ADB'],
#                     #
#                     42: ['ADTF', 'ADB'],
#                     #
#                     #
#                     # # -------------- 3 FEATURES -------------------
#                     #
#                     # 43: ['FC', 'AFD', 'AFDisp'],
#                     # 44: ['FC', 'AFD', 'AFDispH'],
#                     # 45: ['FC', 'AFD', 'AFDispV'],
#                     # 46: ['FC', 'AFD', 'ASA'],
#                     # 47: ['FC', 'AFD', 'SPL'],
#                     # 48: ['FC', 'AFD', 'ADT'],
#                     # 49: ['FC', 'AFD', 'ADpFF'],
#                     # 50: ['FC', 'AFD', 'ADTF'],
#                     51: ['FC', 'AFD', 'ADB'],
#                     #
#                     #
#                     # 52: ['FC', 'AFDisp', 'AFDispH'],
#                     53: ['FC', 'AFDisp', 'AFDispV'],
#                     # 54: ['FC', 'AFDisp', 'ASA'],
#                     # 55: ['FC', 'AFDisp', 'SPL'],
#                     # 56: ['FC', 'AFDisp', 'ADT'],
#                     # 57: ['FC', 'AFDisp', 'ADpFF'],
#                     # 58: ['FC', 'AFDisp', 'ADTF'],
#                     59: ['FC', 'AFDisp', 'ADB'],
#                     #
#                     #
#                     # 60: ['FC', 'SPL', 'AFDispH'],
#                     # 61: ['FC', 'SPL', 'AFDispV'],
#                     # 62: ['FC', 'SPL', 'ASA'],
#                     # 63: ['FC', 'SPL', 'ADT'],
#                     # 64: ['FC', 'SPL', 'ADpFF'],
#                     65: ['FC', 'SPL', 'ADTF'],
#                     # 66: ['FC', 'SPL', 'ADB'],
#                     #
#                     #
#                     # 67: ['FC', 'ADTF', 'AFDispH'],
#                     # 68: ['FC', 'ADTF', 'AFDispV'],
#                     # 69: ['FC', 'ADTF', 'ASA'],
#                     70: ['FC', 'ADTF', 'ADT'],
#                     71: ['FC', 'ADTF', 'ADpFF'],
#                     72: ['FC', 'ADTF', 'ADB'],
#                     #
#                     #
#                     # 73: ['FC', 'ADB', 'AFDispH'],
#                     # 74: ['FC', 'ADB', 'AFDispV'],
#                     # 75: ['FC', 'ADB', 'ASA'],
#                     76: ['FC', 'ADB', 'ADT'],
#                     77: ['FC', 'ADB', 'ADpFF'],
#                     # # 78: ['FC', 'ADB', 'ADB'], - invalid
#                     #
#                     #
#                     # 79: ['AFDisp', 'AFDispH', 'AFD'],
#                     # 80: ['AFDisp', 'AFDispH', 'ASA'],
#                     # 81: ['AFDisp', 'AFDispH', 'SPL'],
#                     # 82: ['AFDisp', 'AFDispH', 'ADT'],
#                     # 83: ['AFDisp', 'AFDispH', 'ADpFF'],
#                     # 84: ['AFDisp', 'AFDispH', 'ADTF'],
#                     85: ['AFDisp', 'AFDispH', 'ADB'],
#                     #
#                     #
#                     # 86: ['AFDisp', 'AFDispV', 'AFD'],
#                     # 87: ['AFDisp', 'AFDispV', 'ASA'],
#                     # 88: ['AFDisp', 'AFDispV', 'SPL'],
#                     89: ['AFDisp', 'AFDispV', 'ADT'],
#                     90: ['AFDisp', 'AFDispV', 'ADpFF'],
#                     91: ['AFDisp', 'AFDispV', 'ADTF'],
#                     92: ['AFDisp', 'AFDispV', 'ADB'],
#                     #
#                     #
#                     # 93: ['AFDisp', 'SPL', 'ASA'],
#                     # 94: ['AFDisp', 'SPL', 'ADT'],
#                     # 95: ['AFDisp', 'SPL', 'ADpFF'],
#                     # 96: ['AFDisp', 'SPL', 'ADTF'],
#                     # 97: ['AFDisp', 'SPL', 'ADB'],
#                     #
#                     #
#                     98: ['ADTF', 'ADB', 'FC'],
#                     99: ['ADTF', 'ADB', 'AFD'],
#                     # 100: ['ADTF', 'ADB', 'AFDisp'],
#                     # 101: ['ADTF', 'ADB', 'AFDispH'],
#                     102: ['ADTF', 'ADB', 'AFDispV'],
#                     # 103: ['ADTF', 'ADB', 'ASA'],
#                     # 104: ['ADTF', 'ADB', 'SPL'],
#                     105: ['ADTF', 'ADB', 'ADT'],
#                     106: ['ADTF', 'ADB', 'ADpFF'],
#                     #
#                     #
#                     # 107: ['ADT', 'FC', 'AFD'],
#                     # 108: ['ADT', 'FC', 'AFDisp'],
#                     # 109: ['ADT', 'FC', 'AFDispH'],
#                     # 110: ['ADT', 'FC', 'AFDispV'],
#                     # 111: ['ADT', 'FC', 'ASA'],
#                     # 112: ['ADT', 'FC', 'SPL'],
#                     113: ['ADT', 'FC', 'ADpFF'],
#                     114: ['ADT', 'FC', 'ADTF'],
#                     115: ['ADT', 'FC', 'ADB'],
#                     #
#                     116: ['ADT', 'ADB', 'AFD'],
#                     117: ['ADT', 'ADB', 'AFDisp'],
#                     # 118: ['ADT', 'ADB', 'AFDispH'],
#                     119: ['ADT', 'ADB', 'AFDispV'],
#                     # 120: ['ADT', 'ADB', 'ASA'],
#                     121: ['ADT', 'ADB', 'SPL'],
#                     122: ['ADT', 'ADB', 'ADpFF'],
#                     123: ['ADT', 'ADB', 'ADTF'],
#                     124: ['ADT', 'ADB', 'FC'],
#                     #
#                     125: ['ADpFF', 'ADB', 'AFD'],
#                     126: ['ADpFF', 'ADB', 'AFDisp'],
#                     127: ['ADpFF', 'ADB', 'AFDispH'],
#                     128: ['ADpFF', 'ADB', 'AFDispV'],
#                     129: ['ADpFF', 'ADB', 'ASA'],
#                     130: ['ADpFF', 'ADB', 'SPL'],
#                     131: ['ADpFF', 'ADB', 'ADTF'],
#                     132: ['ADpFF', 'ADB', 'FC'],
#
#
#
#
#
# }

eyes_combination = [
                    # 'both',
                    'left',
                    'right'
                   ]



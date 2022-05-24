

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
                    #only fixation info
                    0: ['FC', 'AFD', 'FDMax', 'FDMin', 'AFDisp', 'AFDispH', 'AFDispV', 'ADTF'],
                    1: ['FC', 'AFD', 'FDMax', 'FDMin', 'AFDisp', 'AFDispH', 'AFDispV'],
                    2: ['FC', 'AFD', 'AFDisp', 'AFDispH', 'AFDispV'],
                    3: ['FC', 'AFD', 'AFDispH', 'AFDispV'],
                    4: ['FC', 'AFDisp', 'AFDispH', 'AFDispV'],
                    5: ['FC', 'AFD', 'AFDisp'],
                    6: ['AFD', 'FDMax', 'FDMin', 'AFDisp', 'AFDispH', 'AFDispV'],
                    7: ['AFD', 'AFDispH', 'AFDispV'],

                    #only saccade info
                    8: ['SC', 'ASD', 'SDMax', 'SDMin', 'ASA', 'SAMax', 'SAMin'],
                    9: ['SC', 'ASD', 'ASA'],

                    #only saccades and fixations info
                    10: ['FC', 'AFD', 'FDMax', 'FDMin', 'AFDisp', 'AFDispH', 'AFDispV', 'ADTF',
                         'SC', 'ASD', 'SDMax', 'SDMin', 'ASA', 'SAMax', 'SAMin'],
                    11: ['FC', 'AFD', 'AFDisp', 'AFDispH', 'AFDispV', 'ADTF',
                         'SC', 'ASD', 'ASA'],
                    12: ['FC', 'AFD', 'AFDisp', 'ADTF',
                         'SC', 'ASD', 'ASA'],
                    13: ['FC', 'AFD', 'AFDisp',
                         'SC', 'ASD', 'ASA'],
                    14: ['FC', 'AFD', 'AFDispH', 'AFDispV'],
                    15: ['FC', 'AFD', 'AFDispH', 'AFDispV',
                         'SC', 'ASD', 'ASA'],

                    #probably the most relevant ones
                    16: ['FC', 'AFD', 'AFDisp', 'ADTF',
                         'SPL', 'ADT', 'ADB'],
                    17: ['FC', 'AFD', 'AFDispH', 'AFDispV', 'ADTF',
                         'SPL', 'ADT', 'ADB'],
                    18: ['AFD', 'AFDisp', 'ADTF',
                         'SPL', 'ADT', 'ADB'],
                    19: ['FC', 'AFDisp', 'ADTF',
                         'ADT', 'ADB'],
                    20: ['FC', 'AFDispH', 'AFDispV', 'ADTF',
                         'ADT', 'ADB'],
                    21: ['FC', 'AFDisp', 'ADTF', 'ADT'],
                    22: ['FC', 'AFDispH', 'AFDispV', 'ADB'],
                    23: ['FC', 'AFDisp', 'ADT', 'ADB'],
                    24: ['AFD', 'AFDisp', 'AFDispH', 'AFDispV', 'ADTF',
                         'ADT', 'ADB'],
                    25: ['AFD', 'AFDispH', 'AFDispV', 'ADT'],
                    26: ['FC', 'ADTF', 'SPL'],
                    27: ['FC', 'ADTF', 'SPL', 'ADB'],
                    28: ['FC', 'ADT', 'SPL'],
                    29: ['FC', 'ADTF',
                         'ADT', 'SPL', 'ADB'],


                    #all features but ADpFF
                    30: ['FC', 'AFD', 'FDMax', 'FDMin', 'AFDisp', 'AFDispH', 'AFDispV', 'ADTF',
                         'SC', 'ASD', 'SDMax', 'SDMin', 'ASA', 'SAMax', 'SAMin',
                         'SPL', 'ADT', 'ADB']




                    # #  #only ADpFF
                    #TODO: ADpFF not supported anymore...
                    # 9: ['ADpFF'],
            }

eyes_combination = [
                    'both',
                    'left',
                    'right'
                   ]





event_detection_methods = ['I-VT',
                           #TODO:
                           # 'I-DT',
                           # 'REMODNAV',
                           # 'NSLR-HMM'
                           ]

clustering_methods = [
                      # 'DBSCAN',
                      # 'K-Means',
                       'FOSC'
                     ]
subsets_of_features = {
                    #only fixations
                    0: ['FC', 'AFD', 'FDMax', 'FDMin', 'FDA', 'ADTF', 'ADB'],
                    # 1: ['FC', 'AFD', 'FDA', 'ADT', 'ADTF', 'ADB'],
                    # 2: ['FC', 'AFD', 'FDMax', 'FDMin', 'FDA', 'ADB'],
                    # #
                    # # #only saccades
                    # 3: ['SC', 'ASD', 'SDMax', 'SDMin', 'SDA', 'ASA', 'SAMax', 'SAMin'],
                    # 4: ['SC', 'ASD', 'ASA', 'SAMax'],
                    # #
                    # # #only fixations and saccades
                    # 5: ['FC', 'AFD', 'FDA', 'ADTF', 'SC', 'ASD', 'ASA', 'ADB'],
                    # 6: ['FC', 'FDA', 'ADTF', 'SC', 'SDA', 'ADB'],
                    # 7: ['FC', 'SC', 'ADT', 'ADTF', 'ADB'],
                    # #
                    # # #all but ADpFF
                    # 8: ['FC', 'AFD', 'FDMax', 'FDMin', 'FDA',
                    #   'SC', 'ASD', 'SDMax', 'SDMin', 'SDA', 'ASA', 'SAMax', 'SAMin',
                    #   'SPL', 'ADT', 'ADTF'],
                    #
                    # #  #only ADpFF
                    # 9: ['ADpFF'],
                    10: ['FC', 'AFD', 'FDA', 'ADT', 'ADTF', 'ADB'],
                    11: ['ADB', 'ADT', 'FC', 'ADTF']
            }

eyes_combination = [
                    'both',
                    'left',
                    'right'
                   ]



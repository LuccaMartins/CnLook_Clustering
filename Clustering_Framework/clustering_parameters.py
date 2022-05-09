

event_detection_methods = ['I-VT',
                           # 'I-DT',
                           # 'REMODNAV',
                           # 'NSLR-HMM'
                           ]

clustering_methods = ['FOSC',
                      # 'K-Means'
                      ]

subsets_of_features = [#the working ones...

                        ['FC', 'AFD', 'ADTF', 'ADT', 'FDA'],

                        ['FC', 'AFD', 'FDMax', 'FDMin', 'FDA',
                         'SC', 'ASD', 'SDMax', 'SDMin', 'SDA', 'ASA', 'SAMax', 'SAMin'],

                        #only ADpFF
                        # ['ADpFF'],

                        #only fixations
                        ['FC', 'AFD', 'FDMax', 'FDMin', 'FDA'],

                        #only saccades
                        ['SC', 'ASD', 'SDMax', 'SDMin', 'SDA', 'ASA', 'SAMax', 'SAMin'],

                        #others
                        ['FC', 'SPL', 'ADT'],
                       ]

eyes_combination = ['both',
                    'left',
                    'right'
                   ]



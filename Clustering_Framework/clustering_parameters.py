

event_detection_methods = ['I-VT',
                           # 'I-DT',
                           # 'REMODNAV',
                           # 'NSLR-HMM'
                           ]

clustering_methods = ['FOSC',
                      # 'K-Means'
                      ]

subsets_of_features = [#the working ones...
                        ['FC', 'AFD', 'FDMax', 'FDMin',
                         'SC', 'ASD', 'SDMax', 'SDMin',
                         'ASL', ],
                        ['ADpFF'],
                        ['ADpFF', 'ADT'],

                        #only fixations
                        # ['FC', 'AFD', 'FDMax', 'FDMin', 'FDT', 'FDA'],

                        #only saccades
                        # ['SC', 'ASC', 'SFC', 'SDMax', 'SDMin', 'SDT',
                        # 'SDA', 'SAT', 'ASA', 'SAMax', 'SAMin', 'SSV',
                        # 'SVMax', 'SVMin', 'ASL',],
                       ]

eyes_combination = ['both',
                    'left',
                    'right'
                   ]



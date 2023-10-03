"""
This module is aimed at laboratories performing interventional procedures in the electrophysiology department.
This module contains functions for mapping the description content (column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The mapped procedures column is used to organize the description into useful categories.
"""

def map_old_procedures(df_data, verbose=False):
    """
    This function performs mapping of older procedures if they are detected by the map_procedures function.
    """

    # Create a dictionary with the old procedures to be mapped:    
    mapping_old = { 'RGA Ablasjon SVT'                  : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
                    
                    'RGA Ablasjon Atrieflimmer'         : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',
                    
                    'RGA Ablasjon Atrieflutter'         : 'RGA Cor Ablasjon Atrieflutter (int.)',

                    'RGA Ablasjon VT'                   : 'RGA Cor Ablasjon VT m 3D (int.)',

                    'RGA CRYO Ablasjon Atrieflimmer'    : 'RGA Cor Cryo Ablasjon Atrieflimmer (int.)',

                    'RGA Elfys SVT'                     : 'RGA Cor Elfys VT el. SVT (int.)',
                    'RGA Elfys VT'                      : 'RGA Cor Elfys VT el. SVT (int.)',

                    'RGA CRT-D'                         : 'RGA Cor CRT-D (int.)',

                    'RGA CRT-P'                         : 'RGA Cor CRT-P (int.)',

                    'RGA ICD1'                          : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',

                    'RGA ICD2'                          : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                    'RGA PM1'                           : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                    'RGA PM2'                           : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                    'RGA TPM'                           : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM'}
        
    df_data['Mapped Procedures'] = df_data['Beskrivelse'].replace(mapping_old)
    
    if verbose:
        print('Detecting old procedures from before the new Sectra PACS.')
        print('Mapping these old procedure names to new names...\n')
        for key, value in mapping_old.items():
             print(f'{key} -> {value}')
    
    return df_data

def map_procedures(df_data, verbose=False):
    """
    This function will map similar procedures into the same category.
    This list is generated through conversations with the department.
    """

    # Check to see if mapping of older procedures is needed:
    if (df_data['Beskrivelse'].str.contains('RGA Ablasjon').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA CRYO').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA Elfys').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA CRT').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA ICD').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA PM').any()) or \
       (df_data['Beskrivelse'].str.contains('RGA TPM').any()):
        
        df_data = map_old_procedures(df_data, verbose=verbose)
    
    # Create a dictionary with the procedures to be mapped:    
    mapping = { 'RGA Cor Ablasjon SVT (int.)'                   : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
                'RGA Cor Ablasjon SVT m 3D (int.)'              : 'RGA Cor Ablasjon SVT (int.) m og u 3D',
            
                'RGA Cor Ablasjon Atrieflimmer (int.)'          : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',
                'RGA Cor Ablasjon Atrieflimmer med 3D (int.)'   : 'RGA Cor Ablasjon Atrieflimmer (int.) m og u 3D',

                'RGA Cor Elfys SVT (int.)'                      : 'RGA Cor Elfys VT el. SVT (int.)',
                'RGA Cor Elfys VT (int.)'                       : 'RGA Cor Elfys VT el. SVT (int.)',

                'RGA Cor 2-k PM (int.)'                         : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                'RGA Cor 1-k PM (int.)'                         : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                'RGA Cor Implantasjon PM/ICD (int.)'            : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM'}

    df_data['Mapped Procedures'] = df_data['Beskrivelse'].replace(mapping)

    if verbose:
        print('Mapping procedures...\n')
        for key, value in mapping.items():
             print(f'{key} -> {value}')

    return df_data

def filter_procedures(df_data, verbose=False):
    """
    This function removes the procedures which the department is not interested in analyzing.
    """

    # Create a list of procedures to be kept:
    procedures_to_keep =   ['RGA Cor Ablasjon SVT \(int\.\) m og u 3D',
                            'RGA Cor Ablasjon Atrieflimmer \(int\.\) m og u 3D',
                            'RGA Cor Ablasjon Atrieflutter \(int\.\)',
                            'RGA Cor Ablasjon VT m 3D \(int\.\)',
                            'RGA Cor Cryo Ablasjon Atrieflimmer \(int\.\)',
                            'RGA Cor Elfys VT el. SVT \(int\.\)',
                            'RGA Cor CRT-D \(int\.\)',
                            'RGA Cor CRT-P \(int\.\)',
                            'RGA Cor Implantasjon PM/ICD \(int\.\) ink\. 2k og 1k PM']
   
    # the 'keep' column will be true if any of the procedures above is in a substring of the 'Mapped Procedures' column:
    df_data['keep'] = df_data['Mapped Procedures'].str.contains('|'.join(procedures_to_keep))

    if verbose:
        # Print the totoal number of unique procedures:
        print('The total number of unique procedures is %d' % len(df_data['Mapped Procedures'].unique()))
        print('\n')

        # Print all the procedures which will be kept:
        print('The following %d unique procedures or procedure-combinations will be kept:' % len(df_data[df_data['keep']]['Mapped Procedures'].unique()))
        for procedure in df_data[df_data['keep']]['Beskrivelse'].unique():
            # Print the number of procedures which will be kept:
            print(procedure)

        print('\n')
        print('The following %d unique procedures or procedure-combinations will be dropped:' % len(df_data[~df_data['keep']]['Mapped Procedures'].unique()))
        # Print all the procedures which will be removed:
        for procedure in df_data[~df_data['keep']]['Mapped Procedures'].unique():
            print(procedure)
    
    return (df_data[df_data['keep']]).drop(columns=['keep'])
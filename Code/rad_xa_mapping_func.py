"""
This module is aimed at laboratories performing interventional procedures in the radiology department.
This module contains functions for mapping the description content (column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The mapped procedures column is used to organize the description into useful categories.
"""

def map_procedures(df_data, verbose=False):
    """
    In the inteventional radiology department, the description column (column: 'Beskrivelse') usually contains
    several different procedure codes. These codes have been concatinated into one string.
    This results in multiple different strings representing the same procedure, with only minor variations.
    For instance if ultrasound was used, the string will contain 'UL ...', or some 
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
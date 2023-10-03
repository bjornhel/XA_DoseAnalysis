"""
This module is aimed at laboratories performing interventional procedures in the radiology department.
This module contains functions for mapping the description content (column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The mapped procedures column is used to organize the description into useful categories.
"""

def _perform_mapping(df_data, key, value):
    """
    This utility function performs the mapping according to the following rules:
    First the key is separated in to a list of criteria, separated by ' & '.
    Then each criteria is checked for the presence of '~' which indicates an exclusion criteria.
    """

    def _check_criteria(description):
        """
        This utility function checks whether all the inclusion and exclusion criteria are satisfied in
        the description column 'Beskrivelse'.
        """
        # Check if all inclusion criteria are present in the description:
        if all(elem.lower() in description.lower() for elem in inclusion_criteria) & \
            ~any(elem.lower() in description.lower() for elem in exclusion_criteria):
            return True
        else:
            return False

    # Get the inclusion and exclusion criteria:
    key_list = key.split(' & ')
    inclusion_criteria = [x for x in key_list if not x.startswith('~')]
    exclusion_criteria = [x[1:] for x in key_list if x.startswith('~')]

    # Check df_data's 'Beskrivelse' column for substrings of all the inclusion and exclusion criteria:
    # 'Mapping Target' is set to True if all inclusion criteria are present and no exclusion criteria are present:
    # This is a temporary column that is used to check whether we are mapping allready mapped columns.
    df_data['Mapping Target'] = False
    df_data.loc[df_data['Beskrivelse'].apply(_check_criteria), 'Mapping Target'] = True

    # Check if no procedures were targeted by the mapping:
    if sum(df_data['Mapping Target'] == True) == 0:
        print('WARNING! No procedures were targeted by this mapping!')
        print('\n')
        df_data.drop('Mapping Target', axis=1, inplace=True)
        return df_data

    # Check if the mapping target is already mapped and give a warning and information if it is:
    if sum((df_data['Mapping Target'] == True) & (df_data['Mapped Procedures'] != 'Unmapped')) > 0:
        print('\n')
        print('WARNING! Some or all mapping targets are already mapped!')
        print('\n')
        # Print all the inclusion criteria with an ' & ' between them:
        print('The current inclusion criteria are: ' + ' & '.join(inclusion_criteria))
        print('The current exclusion criteria are: ' + ' & '.join(exclusion_criteria))
        # Print a unique list of the already mapped procedures:
        print('\n')
        print('The following procedures are already mapped:')
        mapped_list = df_data['Beskrivelse'][(df_data['Mapping Target'] == True) &  
                                             (df_data['Mapped Procedures'] != 'Unmapped')].unique().tolist()
        print('\n')
        for item in mapped_list:
            # Print the 'Beskrivelse' column ' -> ' the 'Mapped Procedures' column:
            print(f'{item}   --->   {df_data["Mapped Procedures"][df_data["Beskrivelse"] == item].unique()[0]}')
        print('\n')

        print('Please check the mapping dictionary and refine it to avoid mapping the same procedure twice.')
        df_data.drop('Mapping Target', axis=1, inplace=True)
        return df_data    

    # Map the procedures:
    df_data.loc[df_data['Mapping Target'] == True, 'Mapped Procedures'] = value

    # Remove the temporary column:
    df_data.drop('Mapping Target', axis=1, inplace=True)

    return df_data

def map_rad_xa_procedures(df_data, verbose=False):
    """
    In the inteventional radiology department, the description column (column: 'Beskrivelse') usually contains
    several different procedure codes. These codes have been concatinated into one string with each procedure 
    separated by a comma. This results in multiple different strings representing the same procedure, 
    with only minor variations. For instance if ultrasound was used, the string will contain ', UL ...'.

    This function involves a mapping dictionary that maps the different strings to the same procedure.
    If a substring is found in the description column, the corresponding value in the mapping dictionary.
    The mapped procedures are put in a new column (column: 'Mapped Procedures').

    For some procedures it is nessecary to use several criteria to identify the procedure.
    For instance: Nefrostomi med innleggelse av dren, as this can be a complex procedure.
    For such cases the key in the mapping dictionary use ' & ' to separate the criteria.
    Example: mapping = {'Nefrostomi & innleggelse av dren' : 'Nefrostomi innleggelse'}

    Other procedures are similar but musch less complex.
    For instance: Nefrostomi med skifte av dren eller fjerning av dren.
    For such cases the key in the mapping dictionary can use ' & ' to separate the criteria,
    but also use a '~' in front of the criteria that is an exclusion criteria.
    So to make a Nefrostomi med skifte av dren eller fjerning av dren procedure, 
    the mapping dictionary can be:
    Example: mapping = {'Nefrostomi & ~innleggelse av dren' : 'Nefrostomi skifte eller fjerning'}
    
    To change or add to the mapping of procedures, edit the 'mapping' dictionary below.
    """

    # Check the 'Beskrivelse' column for the following characters '&', '~':
    if sum(df_data['Beskrivelse'].str.contains('&')) > 0:
        print('WARNING! The "Beskrivelse" column contains the character "&".')
        print('This character is used to separate criteria for identifying procedures.')
        print('We need to find another separator character.')
        return
    
    if sum(df_data['Beskrivelse'].str.contains('~')) > 0:
        print('WARNING! The "Beskrivelse" column contains the character "~".')
        print('This character is used to exclude criteria for identifying procedures.')
        print('We need to find another separator character.')
        return

    # Initialize the 'Mapped Procedures' column:
    df_data['Mapped Procedures'] = 'Unmapped'

    # Move the 'Mapped Procedures' column to the front:
    cols = df_data.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Mapped Procedures')))
    df_data = df_data.reindex(columns=cols)
   
    # Create the mapping dictionary:
    mapping = { 'Nefrostomi & innleggelse av dren'      : 'Nefrostomi innleggelse', 
                'Nefrostomi & ~innleggelse av dren'     : 'Nefrostomi skifte eller fjerning',
                'Caput Embolisering'                    : 'Caput Embolisering',
                'Caput Trombektomi'                     : 'Trombektomi',
                'RG Tinningben'                         : 'Cochlia',
                'Caput og collum & ~Caput Embolisering & ~Caput Trombektomi'    : 'Caput og collum',
                'Lever TACE'                            : 'TACE',
                'Myelografi'                            : 'Myelografi',
                'PTC, diagnostikk'                      : 'PTC/PTBD',
                'Galleveier - PTBD & ~PTC, diagnostikk' : 'PTC/PTBD',
                'RGV Pulmonalarterier'                  : 'Pulmonalarterier',
                'Øsofagus'                              : 'Øsofagus',
                'Urethragrafi'                          : 'Urethragrafi',
                'RG Shunt'                              : 'Shunt',
                'RG Scoliose'                           : 'Scoliose',
                'Cor TAVI'                              : 'TAVI'} 

    # Map the procedures:
    if verbose:
        print('Mapping procedures...\n')

    for key, value in mapping.items():
        if verbose:
            print(f'{key} -> {value}')
        df_data = _perform_mapping(df_data, key, value)

    return df_data
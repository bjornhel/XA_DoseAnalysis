"""
This module contains a functions for returning a mapping dictionary to facilitate interpretation of the decription column 
(column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The 'Mapped Procedures' column is used to organize the description into useful categories, make relevant plots, etc.
"""

def get_xa_dsa_mapping_dict(include_old_procedure_names=False):
    """
    Here the user can hardcode the mapping dictionary for the xa procedures DSA raquires:

    If the dataset includes procedure names from the era before IDS7 PACS, pass the argument True to the function.
    
    The description column (column: 'Beskrivelse') can potentially contain
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

    mapping = { 'RGA Cor PCI & ~RGA Cor ECMO & ~RGA Cor TAVI'   : 'PCI',
                'Caput Trombektomi'                     : 'Trombektomi',
                'Nefrostomi & innleggelse av dren'      : 'Nefrostomi innleggelse', 
                'EVAR'            : 'EVAR',
                'RGA Cor 2-k PM (int.)'                         : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                'RGA Cor 1-k PM (int.)'                         : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM',
                'RGA Cor Implantasjon PM/ICD (int.)'            : 'RGA Cor Implantasjon PM/ICD (int.) ink. 2k og 1k PM'
            }

    if include_old_procedure_names:
        """
        Append this section if the data includes procedure names from the era before IDS7 PACS.
        """
        # Create a dictionary with the old procedures to be mapped:    
        mapping_old = { }
        
        # append the mapping_old to the mapping dictionary:
        mapping.update(mapping_old)
    return mapping

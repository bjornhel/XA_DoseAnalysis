"""
This module contains a functions for returning a mapping dictionary to facilitate interpretation of the decription column 
(column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The 'Mapped Procedures' column is used to organize the description into useful categories, make relevant plots, etc.
"""

def get_rad_xa_mapping_dict():
    """
    Here the user can hardcode the mapping dictionary for interventional radiology procedures:

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
                'Cor TAVI'                              : 'TAVI',
                'EVAR'                                  : 'EVAR',
                'RGV Underex'                           : 'Underex',
                'RGV Overex'                            : 'Overex',
                'Diafragmabevegelse'                    : 'Diafragmabevegelse',
                'Bekken Embolisering'                   : 'Bekken Embolisering'} 

    return mapping
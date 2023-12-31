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
    mapping = { # Caput og Collum prosedyrer:
                'Caput Embolisering'                    : 'Caput Embolisering',
                'Caput Trombektomi'                     : 'Trombektomi',
                'Caput og collum & ~Caput Embolisering & ~Caput Trombektomi'    : 'Caput og collum',
                'Myelografi'                            : 'Myelografi',
                'Columna & ~Myelografi & ~Caput'        : 'RG Columna eks. Myelografi',
                
                # IVS Operasjon:
                'RG Tinningben'                         : 'Cochlia',
                'RG Scoliose'                           : 'Scoliose',
                
                # RF Prosedyrer:
                'RG Shunt'                              : 'Shunt',
                'Diafragmabevegelse'                    : 'Diafragmabevegelse',
                'Hysterosalpingografi'                  : 'HSG',
                'Øsofagus'                              : 'Øsofagus/ØVD Enkeltkontrast',
                'RG ØVD enkeltkontrast'                 : 'Øsofagus/ØVD Enkeltkontrast',
                'Urethragrafi'                          : 'Urethragrafi/Urografi/Urinveier/MUCG',
                'RG Urografi'                           : 'Urethragrafi/Urografi/Urinveier/MUCG',
                'RG MUCG'                               : 'Urethragrafi/Urografi/Urinveier/MUCG',
                'RG Urinveier & ~Nefrostomi & ~Pyelografi'            : 'Urethragrafi/Urografi/Urinveier/MUCG',   
                
                # Abdomen/Bekken prosedyrer:
                'Nefrostomi & innleggelse av dren'      : 'Nefrostomi innleggelse', 
                'Nefrostomi & ~innleggelse av dren'     : 'Nefrostomi/Pyelografi skifte eller fjerning',
                'Pyelografi & ~Nefrostomi'                            : 'Nefrostomi/Pyelografi skifte eller fjerning',
                'Lever TACE'                            : 'TACE',
                'PTC, diagnostikk'                      : 'PTC/PTBD',
                'Galleveier - PTBD'                     : 'PTC/PTBD',
                'RGV Pulmonalarterier'                  : 'Pulmonalarterier/PTA/Embolisering',
                'BEVAR/FEVAR'                           : 'BEVAR/FEVAR',
                'TEVAR & ~BEVAR/FEVAR'                  : 'TEVAR',
                'EVAR & ~TEVAR & ~BEVAR/FEVAR'          : '-EVAR',
                'RGA Abdomen PTA'                       : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Abdomen Embolisering & ~EVAR'      : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Aorta PTA'                         : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Abdomen Stent & ~EVAR'             : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Aorta Stent'                       : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'Bekken Embolisering'                   : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Bekken PTA'                        : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Bekken Stent'                      : 'Abdomen/Bekken/Aorta PTA/Embolisering/Stent/Stentgraft',
                'RGA Lever & ~Lever TACE & ~LeverTX'    : 'Lever',
                'RGA Milt'                              : 'Milt/Nyrer',
                'RGA Nyrer & ~RGA Abdomen Stent & ~EVAR & ~Aorta & ~Bekken Embolisering'
                                                        : 'Milt/Nyrer',
                'RGA Nyrer PTA & ~RGA Abdomen Stent & ~EVAR & ~Aorta & ~Bekken Embolisering'                        
                                                        : 'Milt/Nyrer',

                'RG Abdomen - Abscessografi & ~PTC, diagnostikk & ~Galleveier - PTBD & ~Nefrostomi'
                                                        : 'RG Abdomen - Abscessografi, Fjerning/Skifte av dren',
                'RG Abdomen - Skifte av dren & ~PTC, diagnostikk & ~Galleveier - PTBD & ~Nefrostomi'
                                                        : 'RG Abdomen - Abscessografi, Fjerning/Skifte av dren',
                'RG Abdomen - Fjerning av dren & ~PTC, diagnostikk & ~Galleveier - PTBD & ~Nefrostomi'
                                                        : 'RG Abdomen - Abscessografi, Fjerning/Skifte av dren',

                # Ekstremiteter:                                        
                'RGV Underex'                           : 'Underex',
                'RGA Underex'                           : 'Underex',
                'RGV Overex'                            : 'Overex',
                'RGA Overex & ~EVAR & ~Caput'           : 'Overex',
                
                # Hjerteprosedyrer tatt på IVS:
                'Cor TAVI'                              : 'TAVI'
                } 

    return mapping
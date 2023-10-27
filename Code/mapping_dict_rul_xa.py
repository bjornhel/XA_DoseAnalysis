"""
This module contains a functions for returning a mapping dictionary to facilitate interpretation of the decription column 
(column: 'Beskrivelse') to a new column (column: 'Mapped Procedures').
The 'Mapped Procedures' column is used to organize the description into useful categories, make relevant plots, etc.
"""

def get_rul_xa_mapping_dict():
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
                'Caput Trombektomi'                     : 'Trombektomi',
                'Cervical Nerverotsinjeksjon'           : 'Cervical Nerverotsinjeksjon',
                'RG Columna - Vertebroplastikk (int.)'  : 'Vertebroplastikk',
                'RG Columna & ~Vertebroplastikk'        : 'Div. RG Columna u. Vertebroplastikk',
                'RG Shuntveier'                         : 'Shuntveier',
                
                # RF1 og 2  Prosedyrer:
                'Nefrostomi & innleggelse av dren'      : 'Nefrostomi innleggelse', 
                'Nefrostomi & ~innleggelse av dren'     : 'Nefrostomi/Pyelografi skifte eller fjerning',
                
                'PTC, diagnostikk & ~Nefrostomi'                      : 'PTC/PTBD/ERCP',
                'Galleveier - PTBD & ~Nefrostomi'                     : 'PTC/PTBD/ERCP',      
                'PTC Stentinnleggelse & ~Nefrostomi'                  : 'PTC/PTBD/ERCP',
                'ERCP & ~Nefrostomi'                                  : 'PTC/PTBD/ERCP',

                'RG Defecografi'                        : 'Defecografi',    
                
                'Øsophagus'                             : 'Øsofagus/ØVD, enkelt og dobbelt',
                'Øsofagus'                              : 'Øsofagus/ØVD, enkelt og dobbelt',
                'RG ØVD'                                : 'Øsofagus/ØVD, enkelt og dobbelt',

                'RG Videofluoroskopi & ~Øsofagus'       : 'Videofluoroskopi',

                'RG Nedleggelse av ventrikkelsonde & ~ØVD' : 'Nedleggelse av ventrikkelsonde',

                'RG Abdomen & ~PTC, diagnostikk (int.) & ~ERCP & ~ØVD & ~RG Galleblære & ~Embolisering & ~RGL' : 'RG Abdomen diverse',
                'RG Galleblære & ~PTC & ~Galleveier'    : 'RG Galleblære u. PTC eller Galleveier',

                'RGL'                                   : 'Lymfangiografi', 

               

                # Abdomen/Bekken prosedyrer:
                'RGV Thorax'                            : 'RGV Thorax',
                'RGA Bekken Stent/stentgraft (int.)'    : 'Bekken Stentgraft',
                'Embolisering (int.) & ~Stent/Stentgraft & ~Caput & ~RGA Overex & ~RGA Underex'     : 'Abdomen/Bekken Embolisering',

                # Ekstremiteter:                                        
                'RGV Underex'                           : 'Ekstremiteter',
                'RGA Underex & ~RGA Bekken'             : 'Ekstremiteter',
                'RGV Overex & ~RGV Thorax'              : 'Ekstremiteter',
                'RGA Overex'                            : 'Ekstremiteter',
                } 

    return mapping
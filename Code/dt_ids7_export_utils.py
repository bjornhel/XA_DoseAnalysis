"""
This module contains functions for working with exports from DoseTrack and IDS7. 
The following functions are included in this module:
"""

import pandas as pd
import re

def filter_NaT(df_ids7):
    """
    This function removes row with NaT in the column 'Bestilt dato og tidspunkt
    """
    df_ids7 = df_ids7[df_ids7['Bestilt dato og tidspunkt'].notnull()]
    return df_ids7

def check_accession_no(df_ids7, verbose=False):
    """
    This function checks if the accession number has a correct start and length.
    The currently allowed accession numbers are:
    (NORRH|NRRH|NRAK|NIRH|NKRH|NNRH|NRRA)
    Additionally the length of the accession number must be 16 characters.
    """
    valid_formats = r'^(NORRH|NRRH|NRAK|NIRH|NKRH|NNRH|NRRA)'
    patten = re.compile(valid_formats)

    is_valid_format = (df_ids7['Henvisnings-ID'].str.match(patten)) & (df_ids7['Henvisnings-ID'].str.len() == 16)

    if verbose:
        print('Number of rows with invalid accession number: {}'.format(sum(~is_valid_format)))
        # Print the invalid accession numbers:
        if sum(~is_valid_format) > 0:
            print(df_ids7[~is_valid_format]['Henvisnings-ID'])
    
    return df_ids7[is_valid_format]
    
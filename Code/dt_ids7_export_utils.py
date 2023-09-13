"""
This module contains functions for working with exports from DoseTrack and IDS7. 
The following functions are included in this module:
"""

import pandas as pd
import re

def filter_NaT(df_ids7):
    """
    This function removes row with NaT in the column 'Bestilt dato og tidspunkt'
    """
    df_ids7 = df_ids7[df_ids7['Bestilt dato og tidspunkt'].notnull()]
    return df_ids7

def check_accession_format(df_ids7, verbose=False):
    """
    This function checks if the accession number has a correct start and length.
    The currently allowed accession numbers are:
    (NORRH|NRRH|NRAK|NIRH|NKRH|NNRH|NRRA)
    Additionally the length of the accession number must be 16 characters.
    If verbose is True, the function will print the number of invalid accession numbers
    and the invalid accession numbers.
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

def check_accession_ids7_vs_dt(df_ids7, df_dt, verbose=False):
    """
    This function check whether the accession numbers in IDS7 are in DoseTrack.
    It will add a column to the ids7 dataframe called Henvisning_i_dt which is 
    True if the accession number is in DoseTrack and False otherwise.
    If verbose is True, the function will print the number of accession numbers in IDS7
    and the number of accession numbers in IDS7 not in DoseTrack.
    """
    df_ids7['Henvisning_i_dt'] = df_ids7['Henvisnings-ID'].isin(df_dt['Accession Number'].values)
    
    if verbose:
        print('Number of accession numbers in IDS7: {}'.format(len(df_ids7['Henvisnings-ID'].drop_duplicates())))
        print('Number of accession numbers in IDS7 not in DoseTrack: {}'.format(len(df_ids7[df_ids7['Henvisning_i_dt'] == False]['Henvisnings-ID'].drop_duplicates())))

    return df_ids7
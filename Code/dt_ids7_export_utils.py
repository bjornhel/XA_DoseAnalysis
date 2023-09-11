"""
This module contains functions for working with exports from DoseTrack and IDS7. 
The following functions are included in this module:
"""

import pandas as pd

def filter_NaT(df_ids7):
    """ This function removes row with NaT in the column 'Bestilt dato og tidspunkt'"""
    df_ids7 = df_ids7[df_ids7['Bestilt dato og tidspunkt'].notnull()]
    return df_ids7
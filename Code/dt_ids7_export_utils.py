"""
This module contains functions for working with exports from DoseTrack and IDS7. 
The following functions are included in this module:
"""

import pandas as pd
import re

def filter_NaT(df_ids7, verbose=False):
    """
    This function removes row with NaT in the column 'Bestilt dato og tidspunkt'
    """
    if verbose:
        print('Number of rows with NaT in the column "Bestilt dato og tidspunkt": {}'.format(sum(df_ids7['Bestilt dato og tidspunkt'].isnull())))

    df_ids7 = df_ids7[df_ids7['Bestilt dato og tidspunkt'].notnull()]
    return df_ids7

def remove_unnecessary_columns(df_ids7, verbose=False):
    """
    This function removes columns that are automatically included in the export but not needed for analysis, these are:
    Prioritet- og lesemerkeikon
    Lagt til i demonstrasjon-ikon
    """
    if 'Prioritet- og lesemerkeikon' in df_ids7.columns:
        if verbose:
            print('Dropping unnecessary column: Prioritet- og lesemerkeikon')
        df_ids7.drop('Prioritet- og lesemerkeikon', axis=1, inplace=True)

    if 'Lagt til i demonstrasjon-ikon' in df_ids7.columns:
        if verbose:
            print('Dropping unnecessary column: Lagt til i demonstrasjon-ikon')
        df_ids7.drop('Lagt til i demonstrasjon-ikon', axis=1, inplace=True)

    if 'Status' in df_ids7.columns:
        if verbose:
            print('Dropping unnecessary column: Status')
        df_ids7.drop('Status', axis=1, inplace=True)
    
    return df_ids7


def filter_cancelled(df_ids7, verbose=False):
    """ 
    This function removes rows where the procedures have been cancelled.
    """
    if verbose:
        print('Number of cancelled procedures: {}'.format(sum(df_ids7['Avbrutt'] == 'Avbrutt')))

    df_ids7 = df_ids7[df_ids7['Avbrutt'] != 'Avbrutt']
    return df_ids7

def filter_phantom_etc(df_ids7, verbose=False):
    """ 
    This function removes rows representing non-human subjects (phantoms, animals, etc.).
    """
    if verbose:
        print('Number of non-human subjects: {}'.format(sum(df_ids7['Henvisningskategori (RIS)'] == 'X Fantom/objekt/dyr/test')))

    df_ids7 = df_ids7[df_ids7['Henvisningskategori (RIS)'] != 'X Fantom/objekt/dyr/test']
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
    valid_formats = r'^(NORRH|NRRH|NRAK|NIRH|NKRH|NNRH|NRRA|NRUL)'
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



# Utility functions primarily used to check the data for abnormalities:
def check_patents_with_multiple_bookings_on_same_time_with_different_accession(df_ids7):
    """
    This function is used to report whether there are patients with multiple bookings on the
    same time with different accession numbers. This is useful in order to check whether there is a large 
    number of patients with multiple rows of data that must be merged.
    A previous run on over 4000 lines of PACS data revealed 20 cases of different accession no on the same time.
    Many of these were cancelled procedusres, and should be removed in data filtration.
    Others were infact the same procedure. These shoudl have their accession number changed to the one
    reported in the dosetrack data.
    """

    # Make a list of all patients with multiple bookings on the same day with different accession numbers:
    patient_list = df_ids7['Pasient'].drop_duplicates()
    for patient in patient_list:
        # Get the booking times for this patient:
        booking_times = df_ids7[df_ids7['Pasient'] == patient]['Bestilt dato og tidspunkt']
        # Sort the booking times:
        booking_times = booking_times.sort_values()
        # if there is more than one booking:
        if len(booking_times) > 1:
            # loop through all bookings:
            for i in range(len(booking_times)-1):
                # Check if the booking times are on the same day but different time with different accesstion numbers:
                if (booking_times.iloc[i] == booking_times.iloc[i+1]):
                    # Get the accession numbers:
                    acc_no = df_ids7[(df_ids7['Pasient'] == patient) & (df_ids7['Bestilt dato og tidspunkt'] == booking_times.iloc[i])]['Henvisnings-ID'].drop_duplicates()
                    # Check if there are multiple accession numbers:
                    if len(acc_no) > 1:
                        print('Patient: ' + str(patient) + ' has multiple accession numbers at ' + str(booking_times.iloc[i]) + ':')
                        print(acc_no)
                        print('')





def check_patents_with_multiple_bookings_on_same_day_with_different_accession(df_ids7):
    """
    This function is used to report whether there are patients with multiple bookings on the
    same day (not on the same time, as they are included in the data curation) with
    different accession numbers. This is useful in order to check whether there is a large 
    number of patients with multiple rows of data that must be merged.
    On an earlier run with 4000 lines from the PACS only two cases was found.
    Both cases included cancelled procedures.
    """

    # Make a list of all patients with multiple bookings on the same day with different accession numbers:
    patient_list = df_ids7['Pasient'].drop_duplicates()
    for patient in patient_list:
        # Get the booking times for this patient:
        booking_times = df_ids7[df_ids7['Pasient'] == patient]['Bestilt dato og tidspunkt']
        # Sort the booking times:
        booking_times = booking_times.sort_values()
        # if there is more than one booking:
        if len(booking_times) > 1:
            # loop through all bookings:
            for i in range(len(booking_times)-1):
                # Check if the booking times are on the same day but different time with different accesstion numbers:
                if (booking_times.iloc[i].date() == booking_times.iloc[i+1].date()) & (booking_times.iloc[i].time() != booking_times.iloc[i+1].time()):
                    # Get the accession numbers:
                    acc_no = df_ids7[(df_ids7['Pasient'] == patient) & (df_ids7['Bestilt dato og tidspunkt'] == booking_times.iloc[i])]['Henvisnings-ID'].drop_duplicates()
                    # Check if there are multiple accession numbers:
                    if len(acc_no) > 1:
                        print('Patient: ' + str(patient) + ' has multiple accession numbers at ' + str(booking_times.iloc[i].date()) + ':')
                        print(acc_no)
                        print('')
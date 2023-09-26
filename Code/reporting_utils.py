# This module contains utility function to report various properties of the data.

import pandas as pd

def print_obs_per_lab(data):
    for lab in data['Modality Room'].unique():
        print(lab + ': n = ' + str(len(data[data['Modality Room'] == lab])))

def print_median_dap_per_lab(data):
    for lab in data['Modality Room'].unique():
        print(lab + ': DAP = ' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].median(), 2)) + ' Gy*cm2')

def print_summary_per_lab(data):
    for lab in data['Modality Room'].unique():
        print(lab + ': n = {:4}'.format(len(data[data['Modality Room'] == lab])) + \
              ', DAP: Median ' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].median(), 2)) + \
              # 25 th percentile:
              '[' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].quantile(0.25), 2)) + \
              ' - ' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].quantile(0.75), 2)) + '] (Gy*cm2) ' + \
              'range (' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].min(), 2)) + \
              ' - ' + str(round(data[data['Modality Room'] == lab]['DAP Total (Gy*cm2)'].max(), 2)) + ')')
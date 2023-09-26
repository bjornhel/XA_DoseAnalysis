import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import reporting_utils as bh_report

# This module contains functions for performing the various common plots.

def plot_representative_dose(data, procedure, y_max=20, save=False):
    """
    This function will create a boxplot with whiskers.
    The line in the middle will represent the median.
    The box will represent the interquartile range (IQR) of the data.
    The whiskers will represent the 2.5th to 97.5th percentile.
    The dots will represent the outliers.
    There will be one box per room that has performed the procedure.
    """

    # Create a dataframe with the data for the procedure:
    data = data[data['Beskrivelse'] == procedure]
    data = data.sort_values(by=['Modality Room'])
    
    # Make a boxplot:
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.boxplot(x='Modality Room', y='DAP Total (Gy*cm2)', data=data, ax=ax)
    print('Reporting doses for ' + procedure + ':')
    print('\n')
    bh_report.print_summary_per_lab(data[data['Beskrivelse'] == procedure])
    # Reduce the range of the y-axis:
    if y_max > 0:
        ax.set_ylim([0, y_max])
    else:
        y_max = data['DAP Total (Gy*cm2)'].max()

    # add an annotation to the top of the axis with the maximum value and number of observations outside the plot area:
    list_max = []
    list_n_outside = []
    for xtick in ax.get_xticklabels():
        list_max.append(data[data['Modality Room'] == xtick.get_text()]['DAP Total (Gy*cm2)'].max())
        list_n_outside.append(data[data['Modality Room'] == xtick.get_text()]['DAP Total (Gy*cm2)'].gt(y_max).sum())
        
    # Put an annotation on the axis:
    for i, xtick in enumerate(ax.get_xticklabels()):
        if list_max[i] > y_max:
            ax.annotate('Maks: ' + str(round(list_max[i], 2)) + '\n' + 'n-utenfor = ' + str(list_n_outside[i]), xy=(i, y_max), xytext=(i, y_max + y_max/20), ha='center', va='bottom', fontsize=15 , arrowprops=dict(facecolor='black', shrink=0.05))


    # Add a different string to each x-ticklabel:
    labels = []
    for i, xtick in enumerate(ax.get_xticklabels()):
        n_obs = len(data[data['Modality Room'] == xtick.get_text()])
        labels.append(xtick.get_text() + '\n' +'(' + 'n = ' + str(n_obs) + ')')
    _ = ax.set_xticklabels(labels)

    # Add a title:
    _ = plt.suptitle(procedure, fontsize=25, y=1.011)
    # Set new label for the x-axis:
    _ = ax.set_xlabel('Lab')
    # Set new label for the y-axis:
    _ = ax.set_ylabel('DAP (Gy*cm2)')
    # Increase the size of the title and labels:
    _ = ax.title.set_size(20)
    _ = ax.xaxis.label.set_size(20)
    _ = ax.yaxis.label.set_size(20)

    # Increase the font size of the x-ticklabels:
    _ = ax.tick_params(labelsize=15)   
    print('-'*50)
    print('\n')

    return

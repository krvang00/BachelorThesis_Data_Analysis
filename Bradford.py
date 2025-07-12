
######################################################
## Bradford.py                                      ##
## created by Kristin Vaeth - 2025/07/12            ##
######################################################

######################## Library Imports ################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
import os
import matplotlib.pyplot as plt
from pathlib import Path

########################### Main Part ###################################

def make_plot(file_location: str, dilution:float, show:bool=True, save:bool=True, save_folder:str=".") -> None:

    df = pd.read_excel(file_location, skiprows=10)
    df.head()

    # take file name
    file_name = file_location.split("/")[-1].split(".")[0]

    # create standard line 
    df_standardgerade = df[['Content']] #,'Average based on Blank corrected (595)'
    df_standardgerade = df_standardgerade[df_standardgerade['Content'].str.startswith('Standard', na=False)]
    df_standardgerade = df_standardgerade.groupby('Content')
    df_standardgerade.head()

    # plot standard values
    standard_werte = {'Standard S1' : 1.5, 'Standard S2' : 1.0,'Standard S3' : 0.75, 'Standard S4' : 0.5, 'Standard S5' : 0.25}
    x_values = list(standard_werte.values())
    y_values = [ df[df['Content'] == standardwert]['Average based on Blank corrected (595)'].unique()[0] for standardwert in standard_werte.keys()]

    plt.figure(figsize=(10, 6))  
    plt.subplots_adjust(right=0.61)  
    plt.subplots_adjust(left=0.09)
    plt.subplots_adjust(top=0.9, bottom=0.1)
    plt.scatter(x=x_values, y=y_values,color="C0", marker="D", label="Standard Solutions")

    z = np.polyfit((x_values), y_values, 1)
    p = np.poly1d(z)
    r2 = r2_score(y_values, p(x_values))
    plt.plot(x_values,p(x_values),"b--")

    # read number of sample from file
    Nsamples = max( set( [int(element.split("X")[-1]) for element in df['Content'] if element.startswith("Sample")] ) )

    # plot samples
    sample_list = [ f'Sample X{i_sample+1}' for i_sample in range(Nsamples) ]
    sample_values = [ df[df['Content'] == sample_key]['Average based on Blank corrected (595)'].unique()[0] for sample_key in sample_list]
    sample_names = [ df[df['Content'] == sample_key]['Sample Name'].unique()[0] for sample_key in sample_list]
    samples_x_values = (sample_values - z[1]) / z[0]

    index_good_values = [i for i,sample_x in enumerate(samples_x_values) if sample_x >= 0.25 and sample_x <=1.5]
    index_bad_values = [i for i,sample_x in enumerate(samples_x_values) if sample_x < 0.25 or sample_x >1.5]

    sample_x_values_good = np.array( [samples_x_values[i] for i in index_good_values] )
    sample_values_good = np.array( [sample_values[i] for i in index_good_values] )

    sample_x_values_bad = np.array( [samples_x_values[i] for i in index_bad_values] )
    sample_values_bad = np.array( [sample_values[i] for i in index_bad_values] )
    
    samples_x_values = np.array(samples_x_values)  

    if len(index_good_values)>0:
        plt.scatter(x=sample_x_values_good, y=sample_values_good, color="orange", marker="o", label="Samples Included")
    if len(index_bad_values)>0:
        plt.scatter(x=sample_x_values_bad, y=sample_values_bad, color="red", marker=".", label="Samples Excluded")

    # standard equation and R^2 position
    plt.text(0.05, 0.95, f"y = {z[0]:.3f} x + {z[1]:.3f}\nR² = {r2:.3f}",
            transform=plt.gca().transAxes,
            fontsize=11, verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

    # define step for y offset
    y_step = 1.1 / int((Nsamples+1.5)/2)

    # define step for offset x
    x_offset_step = 0.45
    x_offset_start = 1.25

    for i, (sample, x_val, name) in enumerate( zip(sample_list,samples_x_values, sample_names) ):

        # sample i
        Konzentrationen = samples_x_values[i]
        verduennung = x_val * dilution
        probe = 10 / verduennung
        wasser = 11.25 - probe
        text = f"{name}:\nConcentration $[mg/mL]$= {Konzentrationen:.3f}\nDilution $[mg/mL]$ = {verduennung:.3f}\n Sample $[µL]$ = {probe:.3f}\n  Water $[µL]$ = {wasser:.3f}"

        x_pos = x_offset_start + (i%2) * x_offset_step 
        y_offset = 1.0 - y_step * int(i/2)
        plt.text(x_pos, y_offset, text, ha='center', va='top', transform=plt.gca().transAxes, fontsize=11 - 0.5*int(Nsamples/2),color="black" if i in index_good_values else "red" )

    # positions
    plt.ylim(min(y_values) - 1, max(y_values) + 1)

    # change lower limit of the y-axis -> avoid negative values
    plt.ylim(bottom=0) 
    plt.ylim(top=0.5)

    # axes label
    plt.xlabel(r"Concentration $[mg/mL]$", labelpad=10.0)
    plt.ylabel(r"Absorption $[595 \,\, nm]$", labelpad=10.0)

    # fig title
    #plt.title(" ".join(file_name.split("_")) + f"\nDilution={dilution}")

    # turn on the grid
    plt.grid()

    # turn on the legend
    plt.legend()

    # save the figure if save is True
    if save==True:
        plt.savefig(f"{save_folder}/{file_name}.jpeg", format="jpeg", bbox_inches="tight")

    # show the plot if show is True
    if show==True:
        plt.show()

def dilution_from_filename(filename:str) -> int:
    if 'zu' not in filename:
        dilution = 1
    else:
        try:
            dilution = int(filename.split('zu')[1][:2])
        except:
            dilution = int(filename.split('zu')[1][:1])
    return dilution

# define folder where to find the data 
data_folder = 'Bradford_data'
data_path = Path(data_folder)

# create a list with all the files 
files_list = [ data_folder+"/"+file.name for file in data_path.iterdir()]

for file in files_list:
    if file.endswith("xlsx") == False:
        continue

    dilution = dilution_from_filename(file)

    make_plot(file_location=file, dilution=dilution, show=False, save=True, save_folder="Bradford_results")

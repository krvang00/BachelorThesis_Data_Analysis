
######################################################
## ChemiDoc.py                                      ##
## created by Kristin Vaeth - 2025/07/13            ##
######################################################

######################## Library Imports ################################
import matplotlib.pyplot as plt

########################### Main Part ###################################
# Raw data of the filters list
filters_name = [
    "532/28", "590/110", "602/50", "647SP", "700/50", "715/30", "835/50"
]

# dictionary filter name to applications
filter_to_applications = {
    "590/110": ["SYPRO Ruby", "GelRed", "Fast Blast", "Silver Stain", "Ponceau S"],
    "602/50": ["Alexa 546", "Cy3", "DyLight 550", "Rhodamine"],
    "532/28": ["Alexa 488", "Fluorescein", "Cy2", "DyLight 488"],
    "700/50": ["Alexa 647", "Cy5", "DyLight 650"],
    "715/30": ["Alexa 680", "Cy5.5", "DyLight 680", "IRDye 680RD"],
    "835/50": ["Alexa 790", "Cy7", "DyLight 800", "IRDye 800CW"],
    "647SP": ["Chemiluminescence (cutoff)"]
}

# wavelenghts of the secondaries antibodies
secondaries_antibodies_wavelenghts = [555, 594]

# function used to convert the filers_name into the wavelenght range related to the filter
def filters_name_to_wavelenghts(filters_name:str) -> tuple[float,float]:
    """
    Function used to convert the string containing the filter name into
    the related range of wavelenghts the filter can be used for.
    
    Input:
    ------
        - filters_name: str, the string with the filter name
    
    Output:
    -------
        - w_min,w_max: tuple of floats, the minimum and maximum wavelenghts
    """

    # if the filter is of the kind shortpass, then the min is zero and the max is in the name
    if "SP" in filters_name:  # Shortpass
        w_min = 0
        w_max = int(filters_name.replace("SP", ""))
    
    # if not shortpass the name contains info regarding central value and width of the wavelenght range
    else:  # Bandpass
        center, width = map(int, filters_name.split("/"))
        w_min = center - width / 2
        w_max = center + width / 2

    # return the min and max value of the wavelenghts 
    return w_min, w_max


# create a list with the max values of the wavelenghts of the filters
max_w_lists = [filters_name_to_wavelenghts(f)[1] for f  in filters_name]

# instantiate the figure
fig, ax = plt.subplots(1,1,figsize=(11, 6))

# loop over the filters and for each add somenting on the plot
for i, filter_name in enumerate(filters_name):

    # wavelenghts range related to the filter
    w_min, w_max = filters_name_to_wavelenghts(filter_name)
    
    # plot a horizontal line for the filter
    ax.hlines(i, w_min, w_max, colors='gray', linewidth=4)
    
    # add the name of the filter on the right side of the line
    ax.text(w_max + 5, i, filter_name, verticalalignment='center', fontsize=10)

    # put outside the plot the text with the application of the filters
    applications = filter_to_applications.get(filter_name, [])
    if applications:
        ax.text(max(max_w_lists)+250, i, ', '.join(applications), verticalalignment='center', fontsize=8)

        # plot an X or a V to specify whether the filter is detecting the antibody
        marker = 'X'
        color = 'red'

        # loop over the antibodies and plot a marker
        for i_ant, w_ant in enumerate(secondaries_antibodies_wavelenghts):

            # if the range is correct - plot a V, else anx X
            if w_min <= w_ant <= w_max:
                ax.text(max(max_w_lists)+220+10*i_ant, i, '\u2713', verticalalignment='center', color='green', fontsize=10)
            else:
                ax.text(max(max_w_lists)+220+10*i_ant, i, '\u2717', verticalalignment='center', color='red', fontsize=8)




# legend for the antoboides lines
label_antibodies = "Secondary Antibodies"

# vertical line for secondary antibodie
for i, w in enumerate(secondaries_antibodies_wavelenghts):

    # add a vertical line
    ax.vlines(w, -0.5, len(filters_name), colors="green", linewidth=1, linestyle='dashed', alpha=0.4, label= label_antibodies)

    # add the name of the secondary antibody on the right side of the line
    ax.text(w, len(filters_name) - 0.5, f"{w}", color="green", verticalalignment='center', fontsize=8)

    # updae the legend
    label_antibodies = None

# set x limits of the plot
ax.set_xlim(ax.get_xlim()[0]*0.9, ax.get_xlim()[1]*1.1)

# set x and y labels
ax.set_xlabel(r"Wavelength [$nm$]", fontsize=12)
ax.set_ylabel("Types of\nFilters", fontsize=12)

# set the title of the plot
# ax.set_title("Detectability of Secondary Antibodies with Available Filters", fontsize=14)

# suppress the y ticks
ax.set_yticks([])

# set the legend on
ax.legend()

plt.savefig("filters_plot.png", dpi=300, bbox_inches='tight')
#plt.show()

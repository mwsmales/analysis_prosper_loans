# Some useful plot functions - saved in a separate module for cleanliness
# Michael Smales Aug 2022

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


# define histogram plotting function
def hist_plot(chart_data, xlabel=None, ylabel=None, title=None, bin_step=None, maj_tick_step=None, min_tick_step=None, xlim=None):

    if xlim == None:
        max_val = chart_data.max()
        min_val = chart_data.min()
    else:
        max_val = xlim[1]
        min_val = xlim[0]

    if bin_step==None:
        bin_step = (max_val) / 10
    
    if maj_tick_step == None:
        maj_tick_step = bin_step

    # set bin edge and tick locations
    bin_edges = np.arange(0, max_val+ 2 * bin_step, bin_step)
    maj_tick_locn = np.arange(0, max_val+ 2 * bin_step, maj_tick_step)
    if min_tick_step != None:
        min_tick_locn = np.arange(0, max_val+ 2 * bin_step, min_tick_step)

    # set tick labels
    tick_labels = []
    if max_val > 1000:
        for label in maj_tick_locn:
            tick_labels.append("{:.1f}k".format(label/1000))
    elif max_val > 1000000:
        for label in maj_tick_locn:
            tick_labels.append("{:.1f}m".format(label/1000000))
    else:
        for label in maj_tick_locn:
            tick_labels.append("{:.2f}".format(label))

    # create histoagram plot
    fig, ax = plt.subplots(figsize=[8,5])
    ax.hist(chart_data, bins=bin_edges);

    # set x-axis ticks and labels, offsetting to center of each bin
    ax.set_xticks(maj_tick_locn, labels=tick_labels);
    if min_tick_step != None: 
        ax.set_xticks(min_tick_locn, minor=True);

    # add labels etc
    sns.despine()
    ax.set_xlabel(xlabel);
    ax.set_ylabel(ylabel);
    ax.set_title(title);

    # set xlimit
    ax.set_xlim(xlim)



# define function to reformat an axis as %
def tick_format(axis='x', format_type='pct'):
    format_string=""
    format_multiple=1
    if format_type=='pct':
        format_string = '{:.0f}%'
        format_multiple = 100
    if format_type=='k':
        format_string = '{:.1f}k'
        format_multiple = 0.001
    if format_type=='m':
        format_string = '{:.1f}m'
        format_multiple = 0.000001
    if format_type=='bn':
        format_string = '{:.1f}bn'
        format_multiple = 0.000000001

    ax = plt.gca()

    if axis == 'x':
        xtick_locs, xtick_labels = plt.xticks()
        xtick_labels=[]
        for loc in xtick_locs:
            xtick_labels.append(format_string.format(loc*format_multiple))
        ax.set_xticks(ticks=xtick_locs, labels=xtick_labels);
    elif axis == 'y':
        ytick_locs, ytick_labels = plt.yticks()
        ytick_labels=[]
        for loc in ytick_locs:
            ytick_labels.append(format_string.format(loc*format_multiple))
        ax.set_yticks(ticks=ytick_locs, labels=ytick_labels);



# define function for plotting a (vertical) column chart with relative y axis
def rel_col_chart(chart_data, xlabel=None, ylabel=None, title=None, plot_order=None):
    base_color = sns.color_palette()[0]
    fig, ax = plt.subplots(figsize=[8,5])
    sns.countplot(x=chart_data, color=base_color, order=plot_order, ax=ax);

    # set up y axis which goes up to 100%
    y_ticks_max = chart_data.value_counts().max() / chart_data.count()
    if y_ticks_max > 0.5:
        y_tick_step = 0.1
    else:
        y_tick_step = 0.05
    y_tick_props = np.arange(0, y_ticks_max, y_tick_step) 
    y_tick_names = ['{:0.0f}%'.format(v * 100) for v in y_tick_props]

    # set x and y labels
    sns.despine();
    ax.set_xlabel(xlabel);
    ax.set_ylabel(ylabel);
    ax.set_title(title);

    # set ticks etc
    ax.set_yticks(y_tick_props * chart_data.count(), labels=y_tick_names)



# define function for plotting a (horizontal) bar chart with relative x axis
def rel_bar_chart(chart_data, xlabel=None, ylabel=None, title=None, plot_order=[]):
    # convert plot order to a list if needed
    if isinstance(plot_order, pd.Index):
        plot_order = list(plot_order.values)

    # if plot order is not provided, take the top 10 categories ranked largest to smallest
    if plot_order == []:
        plot_order = chart_data.value_counts().index.to_list()[:10]

    base_color = sns.color_palette()[0]
    # plt.figure(figsize=[8,5])
    fix, ax = plt.subplots(figsize=[8,5])
    sns.countplot(y=chart_data, color=base_color, order=plot_order, ax=ax);

    # set up y axis which goes up to 100%
    x_ticks_max = chart_data.value_counts().max() / chart_data.count()
    if x_ticks_max > 0.5:
        x_tick_step = 0.1
    else:
        x_tick_step = 0.05
    x_tick_props = np.arange(0, x_ticks_max, x_tick_step) 
    x_tick_names = ['{:0.0f}%'.format(v * 100) for v in x_tick_props]

    # set x and y labels
    sns.despine();
    ax.set_xlabel(xlabel);
    ax.set_ylabel(ylabel);
    ax.set_title(title);

    # set tick labels
    ax.set_xticks(x_tick_props * chart_data.count(), labels=x_tick_names)

    # Logic to print the proportion text on the bars
    counts = chart_data.value_counts()

    for i in range(len(plot_order)):
        count = counts.loc[plot_order[i]]
        # Convert count into a percentage, and then into string
        pct_string = '{:0.1f}%'.format(100 * count / chart_data.count())
        # Print the string value on the bar. 
        ax.text(count + counts.max()*0.01, i, pct_string, va='center')


# function to plot heatmap of counts from dataframe, with relative scale (i.e. counts add to 100%)
def count_heatmap_relative(data, xrange, yrange, xlabel=None, ylabel=None, title=None, xbin_step=None, ybin_step=None):
    
    df=data
    fig, ax = plt.subplots(figsize=[9,7])
    # plt.figure(figsize=[9,7])

    # arrange bin edges and tick locations
    x_bin_edges = np.arange(0, df[xrange].max() + xbin_step, xbin_step)
    y_bin_edges = np.arange(0, df[yrange].max() + ybin_step, ybin_step)

    # plot histogram
    hist, xbins, ybins, im = ax.hist2d(
        data = df, 
        x = xrange, 
        y = yrange, 
        cmap='YlOrRd', 
        cmin=15, 
        bins=[x_bin_edges, y_bin_edges]
    );

    # align x and y ticks to bin edges
    ax.set_xticks(x_bin_edges)
    ax.set_yticks(y_bin_edges)

    # add text to histogram with scale set to 100%
    hist = hist / len(df) * 100
    for i in range(len(ybins)-1):
        for j in range(len(xbins)-1):
            if pd.isna(hist.T[i,j]):
                pass
            elif hist.T[i,j] > 10:
                ax.text(xbins[j]+xbin_step/5, ybins[i]+ybin_step/2, '{:.0f}%'.format(hist.T[i,j]), 
                        color="w", ha="left", va="center", fontweight='bold')
            else:
                ax.text(xbins[j]+xbin_step/5, ybins[i]+ybin_step/2, '{:.0f}%'.format(hist.T[i,j]), 
                        color="k", ha="left", va="center")

    # add title and axis labels
    sns.despine();
    ax.set_title(title, loc='left');
    ax.set_xlabel(xlabel);
    ax.set_ylabel(ylabel);

    # format tick labels
    tick_format(axis='x', format_type='k')
    tick_format(axis='y', format_type='pct')

    # apply some aesthetic formatting
    ax.grid(which="major", color="w", linestyle='-', linewidth=5)
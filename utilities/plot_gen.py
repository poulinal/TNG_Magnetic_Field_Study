#import matplotlib as plt
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.legend_handler import HandlerTuple
from utilities.bin_data import removeNans



def plot_gen(isoCen_mass, isoCen_bfld, nonIsoCen_mass, nonIsoCen_bfld, 
             preInf_mass, preInf_bfld, postInf_mass, postInf_bfld, filename, 
             log=True, ylabel="$log_{(10)}$(Magnetic Field Strength) (MicroGauss)", xlabel="$log_{(10)}(Mass) M_* (M_\odot)$",
             title=""):
    #plot isolated centrals
    plt.scatter(isoCen_mass, isoCen_bfld, color='blue', label='Isolated Central Galaxies', marker='.')

    #plot non-isolated centrals
    plt.scatter(nonIsoCen_mass, nonIsoCen_bfld, color='red', label='Non-Isolated Central Galaxies', marker='.')

    #plot pre-infall satellites
    plt.scatter(preInf_mass, preInf_bfld, color='green', label='Pre-Infall Satellite Galaxies', marker='*')

    #plot post-infall satellites
    plt.scatter(postInf_mass, postInf_bfld, color='purple', label='Post-Infall Satellite Galaxies', marker='2')

    if log:
        plt.xscale('log')
        plt.yscale('log')

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.title('Scatter Plot of Two Groups')
    
    if title != "":
        plt.title(title)

    # Add a legend
    # plt.legend()
    
    handles, labels = plt.gca().get_legend_handles_labels()
    
    # Wrap each handle in a tuple to force reordering
    tuple_handles = [(h,) for h in handles]

    # Set custom legend with swapped label-marker order
    plt.legend(tuple_handles, labels, handler_map={tuple: HandlerTuple(ndivide=None)})

    
    #change y upper limit
    plt.ylim(min(isoCen_bfld) - 0.5, max(postInf_bfld) + 1)


    #save plot
    dir = 'images/' + filename
    plt.savefig(dir, bbox_inches='tight')


    # Show the plot
    plt.show()


def plot_wcontour(isoCen_mass, isoCen_bfld, 
                  nonIsoCen_mass, nonIsoCen_bfld, 
                  preInf_mass, preInf_bfld, 
                  postInf_mass, postInf_bfld, 
                  isoCen_mass_er, isoCen_bfld_er, 
                  nonIsoCen_mass_er, nonIsoCen_bfld_er, 
                  preInf_mass_er, preInf_bfld_er, 
                  postInf_mass_er, postInf_bfld_er, 
                  preInf_mass_nonBin, preInf_bfld_nonBin,
                  postInf_mass_nonBin = None, postInf_bfld_nonBin = None,
                  filename = "", log=True,  
                  ylabel="$\log_{10}$ ( $\langle$B$\\rangle$ / $\mu G$)", xlabel="$\log_{10}$($M_*$ / $M_\odot$)",
                  title="", fs=12, contAlph=0.2, alph = 0.3):
    # xdat = preInf_mass_nonBin
    # ydat = preInf_bfld_nonBin
    xdat, ydat = removeNans(preInf_mass_nonBin, preInf_bfld_nonBin)
    concol = 'green'
    concol2 = 'purple'
    linewidth = 0.75
    # alph = 0.5
    
    binsize=130
    deltaX=(max(xdat)-min(xdat))/binsize
    deltaY=(max(ydat)-min(ydat))/binsize

    xmin=min(xdat)-deltaX
    xmax=max(xdat)+deltaX
    ymin=min(ydat)-deltaY
    ymax=max(ydat)+deltaY

    xx,yy=np.mgrid[xmin:xmax:100j,ymin:ymax:100j]
    positions=np.vstack([xx.ravel(),yy.ravel()])
    values=np.vstack([xdat,ydat])

    kernel=st.gaussian_kde(values)
    Z=np.reshape(kernel(positions).T,xx.shape)
    #print(Z.shape)

    if concol=='blue': linestyle='dashed'
    elif concol=='green': linestyle='dashdot'
    else: linestyle='solid'
        
    #Z=np.reshape(kernel(positions).T,X.shape)
    #delSFR.reshape((len(s_mass),len(SFR)))    
    
    #contour
    plt.contour(xx,yy,Z,colors=concol,linewidths=linewidth,levels=7,alpha=contAlph)
    
    if postInf_mass_nonBin is not None or postInf_bfld_nonBin is not None:
        xdat2, ydat2 = removeNans(postInf_mass_nonBin, postInf_bfld_nonBin)
        deltaX2=(max(xdat2)-min(xdat2))/binsize
        deltaY2=(max(ydat2)-min(ydat2))/binsize
        xmin2=min(xdat2)-deltaX2
        xmax2=max(xdat2)+deltaX2
        ymin2=min(ydat2)-deltaY2
        ymax2=max(ydat2)+deltaY2
        
        xx2,yy2=np.mgrid[xmin2:xmax2:100j,ymin2:ymax2:100j]
        positions2=np.vstack([xx2.ravel(),yy2.ravel()])
        values2=np.vstack([xdat2,ydat2])
        kernel2=st.gaussian_kde(values2)
        Z2=np.reshape(kernel2(positions2).T,xx2.shape)
        plt.contour(xx2,yy2,Z2,colors=concol2,linewidths=linewidth,levels=7,alpha=contAlph)
    
    

    #plot non-isolated centrals
    nonIsoBar = plt.errorbar(nonIsoCen_mass, nonIsoCen_bfld, xerr=nonIsoCen_mass_er, yerr=nonIsoCen_bfld_er, fmt='.', color='red', label='Non-Isolated Central Galaxies', elinewidth = 0.2)
    #plt.scatter(nonIsoCen_mass, nonIsoCen_bfld, color='red', label='Non-Isolated Central Galaxies', marker='.')
    
    # Manually Adjust Error Bar Transparency
    for bar in nonIsoBar[2]:  # bars[2] contains the error bar lines
        bar.set_alpha(alph)  # Set transparency for error bars only
    
    #plot isolated centrals include error
    isoBar = plt.errorbar(isoCen_mass, isoCen_bfld, xerr=isoCen_mass_er, yerr=isoCen_bfld_er, fmt='.', color='blue', label='Isolated Central Galaxies', elinewidth = 0.2)
    #plt.scatter(isoCen_mass, isoCen_bfld, color='blue', label='Isolated Central Galaxies', marker='.')

    # Manually Adjust Error Bar Transparency
    for bar in isoBar[2]:  # bars[2] contains the error bar lines
        bar.set_alpha(alph)  # Set transparency for error bars only

    #plot pre-infall satellites
    preInfBar = plt.errorbar(preInf_mass, preInf_bfld, xerr=preInf_mass_er, yerr=preInf_bfld_er, fmt='*', color='green', label='Pre-Infall Satellite Galaxies', elinewidth = 0.2)
    #plt.scatter(preInf_mass, preInf_bfld, color='green', label='Pre-Infall Satellites', marker='*')

    # Manually Adjust Error Bar Transparency
    for bar in preInfBar[2]:  # bars[2] contains the error bar lines
        bar.set_alpha(alph)  # Set transparency for error bars only

    #plot post-infall satellites
    postInfBar = plt.errorbar(postInf_mass, postInf_bfld, xerr=postInf_mass_er, yerr=postInf_bfld_er, fmt='2', color='purple', label='Post-Infall Satellite Galaxies', elinewidth = 0.2)
    #plt.scatter(postInf_mass, postInf_bfld, color='purple', label='Post-Infall Satellites', marker='2')
    
    # Manually Adjust Error Bar Transparency
    for bar in postInfBar[2]:  # bars[2] contains the error bar lines
        bar.set_alpha(alph)  # Set transparency for error bars only
    
    if log:
        plt.xscale('log')
        plt.yscale('log')

    # Add labels and title
    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    #plt.title('Scatter Plot of Two Groups')
    
    
    # for ax in axs:
    #     ax.tick_params(axis='both', which='major', labelsize=fs, direction='in', top=True, right=True, left = True, bottom = True, length =7)
    #     ax.tick_params(axis='both', which='minor', labelsize=fs, direction='in', top=True, right=True, left = True, bottom =True)
    #     ax.minorticks_on()
    plt.tick_params(axis='both', which='major', labelsize=fs, direction='in', top=True, right=True, left = True, bottom = True, length =7)
    plt.tick_params(axis='both', which='minor', labelsize=fs, direction='in', top=True, right=True, left = True, bottom =True)
    plt.minorticks_on()
    # plt.yaxis.set_tick_params(which='both', labelright=True)
    
    
    
    if title != "":
        plt.title(title)

    # Add a legend
    plt.legend()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)


    #save plot
    dir = 'images/' + filename
    plt.savefig(dir, bbox_inches='tight')


    # Show the plot
    plt.show()
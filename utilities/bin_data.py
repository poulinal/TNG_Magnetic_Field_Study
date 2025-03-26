import numpy as np

#given some array, find the average of the array
def avg(array): #note we treate nan as 0
    return np.sum(np.nan_to_num(array, nan=0))/len(array)

def avgNonNan(array):
    return np.sum(array)/len(array)

def stdev(array):
    return np.std(np.nan_to_num(array, nan=0))

#print(all(pre_infall_mass[i] <= pre_infall_mass[i + 1] for i in range(len(pre_infall_mass) - 1)))
##prints true if already sorted

def bin_data(data, bin_size):
    binned_data = []
    st_error = []
    sem_error = []
    for i in range(0, len(data), bin_size):
        binned_data.append(avg(data[i:i+bin_size]))
        st_error.append(stdev(data[i:i+bin_size]))
        sem_error.append(stdev(data[i:i+bin_size])/np.sqrt(len(data[i:i+bin_size])))
    return binned_data, st_error, sem_error

#given mass array and bfld array, sort by mass but change bfld based on sorting mass
def sort_mass(mass, bfld, sfri="", removeNan=True):
    mass, bfld = removeNans(mass, bfld)
    #sort the mass array
    sorted_mass = np.sort(mass)
    #create a new array to store the sorted bfld
    sorted_bfld = np.zeros(len(bfld))
    if type(sfri) != list:
        sorted_sfri = np.zeros(len(sfri))
    #iterate over the sorted mass array
    for i in range(0,len(sorted_mass)):
        #find the index of the mass in the unsorted mass array
        index = np.where(mass == sorted_mass[i])
        #store the bfld in the sorted bfld array
        sorted_bfld[i] = bfld[index[0][0]]
        if type(sfri) != list:
            sorted_sfri[i] = sfri[index[0][0]]
    if type(sfri) != list:
        return sorted_mass, sorted_bfld, sorted_sfri
    else:
        return sorted_mass, sorted_bfld
    
def removeNans(mass, bfld):
    #make sure mass and bfld are the same length
    #and remove any nan values
    new_mass = []
    new_bfld = []
    for i in range(0,len(mass)):
        if not np.isnan(mass[i]) and not np.isnan(bfld[i]):
            new_mass.append(mass[i])
            new_bfld.append(bfld[i])
    return np.array(new_mass), np.array(new_bfld)
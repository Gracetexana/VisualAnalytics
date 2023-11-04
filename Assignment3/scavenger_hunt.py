# /Users/ykbics/Library/CloudStorage/GoogleDrive-ykbics@g.rit.edu/My Drive/ISTE782/Activities/Data for Scaventer Hunt

import matplotlib.pyplot as plt
import numpy as np

def read_waveforms(LA, RV, RA) :
    infile = open('waveforms.csv', 'r')

    line = infile.readline()
    wf = 0 # which waveform are we trying to read (0 = LA, 1 = RV, 2 = RA)

    while line :
        line = line.strip()
        data = line.split(',')

        for i in range(0, len(data)) : 
            data[i] = float(data[i])

        if(wf == 0) :
            LA.append(data)
        elif(wf == 1) :
            RV.append(data)
        elif(wf == 2) :
            RA.append(data)
        
        wf = (wf + 1) % 3
        line = infile.readline()

    infile.close()

def read_times(TL, TR) :
    infile = open('times.csv', 'r')
    line = infile.readline()
    data = line.strip().split(',')

    for i in range(0, len(data)) : 
        data[i] = float(data[i]) * 1000

    TL.append(data)

    line = infile.readline()
    data = line.strip().split(',')

    for i in range(0, len(data)) : 
        data[i] = float(data[i]) * 1000

    TR.append(data)
    infile.close()

def plot_waveforms(LA, RV, RA, TL, TR) :
    for i in range(0, len(LA)):
        # LA subplot
        plt.subplot(311)
        plt.plot(TL, LA[i])
        plt.title("Waveforms for Instance " + str(i+1))
        plt.ylabel("Lin Accel (g)")
        plt.xticks(np.arange(0,55,step=5))

        # RV subplot
        plt.subplot(312)
        plt.plot(TR, RV[i])
        plt.ylabel("Rot Vel (rad/s)")
        plt.xticks(np.arange(0,55,step=5))

        # RA subplot
        plt.subplot(313)
        plt.plot(TR, RA[i])
        plt.ylabel("Rot Accel (rad/s\N{SUPERSCRIPT TWO})")
        plt.xticks(np.arange(0,55,step=5))

        plt.xlabel("Time (ms)")
        plt.savefig("Instance" + str(i+1) + ".png")
        plt.close()

"""
calculates the min, max, and mean of each instance of a waveform
creates a list of mins (the min of each instance is in the list)
creates a list of maxes (the max of each instance is in the list)
creates a list of means (the mean of each instance is in the list)
returns an array of arrays for a waveform
[[min], [max], [mean]]
"""
def features(waveform):
    min = []
    max = []
    mean = []

    for i in range(0, len(waveform)):
        min.append(np.min(waveform[i]))
        max.append(np.max(waveform[i]))
        mean.append(np.mean(waveform[i]))
    
    return [np.array(min), np.array(max), np.array(mean)]

def all_features(LA, RV, RA):
    return np.array([features(LA), features(RV), features(RA)])

"""
returns the min, max, and mean of an array
in this case, the array is a waveform feature (e.g. the list of mins for each instance of LA)
"""
def feature_statistics(waveform_feature):
    return np.min(waveform_feature), np.max(waveform_feature), np.mean(waveform_feature)

"""
Iteratively prints summary statistics of each feature of each waveform
"""
def print_feature_stats(array_of_features): # an array of arrays of arrays [LA[[mins], [maxes], [means]], RV[[mins], [maxes], [means]], RA[[mins], [maxes], [means]]] 
    waveform_name = ["LA", "RV", "RA"]
    min_max_mean = ["M", "P", "A"]

    for i in range(0, len(array_of_features)):
        for j in range(0, len(array_of_features[i])):
            min, max, mean = feature_statistics(array_of_features[i][j]) # the min, max, and mean for each feature for each waveform

            print(min_max_mean[j] + waveform_name[i] + ": min = " + str(min) + ", max = " + str(max) + ", mean = " + str(mean))
        print()

def plot_features(array_of_features): # an array of arrays of arrays [LA[[mins], [maxes], [means]], RV[[mins], [maxes], [means]], RA[[mins], [maxes], [means]]]
    waveform_name = ["LA", "RV", "RA"]
    units = [" (g)", " rad/s", " rad/s\N{SUPERSCRIPT TWO}"]
    min_max_mean = ["Minimum ", "Maximum ", "Mean "]
    k = 1
    
    for i in range(0, len(array_of_features)):        
        for j in range(0, len(array_of_features[i])):
            plt.subplot(330 + k)
            plt.plot(range(0,len(array_of_features[i][j])), array_of_features[i][j])
            if (k<4): plt.title(min_max_mean[j])
            if ((k-1)%3 == 0): plt.ylabel(waveform_name[i] + units[i])
            if (k>6): plt.xlabel("Instance")
            
            k += 1

    plt.savefig("All_Features.png")        
    plt.close()
    plt.show()

def select_three(array_of_features):
    return array_of_features[0][1], array_of_features[1][1], array_of_features[2][1] # LA max, RV max, and RA max
    
def scatter_plot_features(F1, F2, F3):    
    plt.scatter(F1, F2)
    plt.title("Max Linear Acceleration vs Max Rotational Velocity")
    plt.xlabel("Max Linear Acceleration (g)")
    plt.ylabel("Max Rotational Velocity (rad/s)")
    plt.savefig("F1_vs_F2")
    plt.close()

    plt.scatter(F2, F3)
    plt.title("Max Rotational Velocity vs Max Rotational Acceleration")
    plt.xlabel("Max Rotational Velocity (rad/s)")
    plt.ylabel("Max Rotational Acceleration (rad/s\N{SUPERSCRIPT TWO})")
    plt.savefig("F2_vs_F3")
    plt.close()

    plt.scatter(F3, F1)
    plt.title("Max Rotational Acceleration vs Max Linear Acceleration")
    plt.xlabel("Max Rotational Acceleration (rad/s\N{SUPERSCRIPT TWO})")
    plt.ylabel("Max Linear Acceleration (g)")
    plt.savefig("F3_vs_F1")
    plt.close()

def top_five(F1, F2, F3):
    F1_values = np.copy(F1)
    F1_values[::-1].sort()

    F2_values = np.copy(F2)
    F2_values[::-1].sort()

    F3_values = np.copy(F3)
    F3_values[::-1].sort()
    
    F1_indices = []
    F2_indices = []
    F3_indices = []

    for i in range(0, 5):
        F1_indices.append(np.where(F1 == F1_values[i])[0][0])
        F2_indices.append(np.where(F2 == F2_values[i])[0][0])
        F3_indices.append(np.where(F3 == F3_values[i])[0][0])

    F1_indices.reverse()
    F2_indices.reverse()
    F3_indices.reverse()

    print(F1_indices)
    print(F2_indices)
    print(F3_indices)

# make empty data and time Lists
LA_list = []
RV_list = []
RA_list = []
TL_list = []
TR_list = []

read_waveforms(LA_list, RV_list, RA_list)
read_times(TL_list, TR_list)

# convert all data and time lists to numpy arrays for plotting
LA = np.array(LA_list)
RV = np.array(RV_list)
RA = np.array(RA_list)
TL = np.array(TL_list[0])
TR = np.array(TR_list[0])



plot_waveforms(LA, RV, RA, TL, TR)

print_feature_stats(all_features(LA, RV, RA))
plot_features(all_features(LA, RV, RA))

F1, F2, F3 = select_three(all_features(LA, RV, RA))
scatter_plot_features(F1, F2, F3)
top_five(F1, F2, F3)

"""
print("LA")
print(LA)
print(np.min(LA))
print(np.max(LA))
print(np.mean(LA))
print()

print("RV")
print(RV)
print(np.min(RV))
print(np.max(RV))
print(np.mean(RV))
print()

print("RA")
print(RA)
print(np.min(RA))
print(np.max(RA))
print(np.mean(RA))
print()

print("TL")
print(TL)
print()

print("TR")
print(TR)
print()

plt.plot(TL, LA[6])
plt.title("Linear Acceleration of Instance 7")
plt.xlabel("Time (ms)")
plt.ylabel("Lin Accel (g)")
plt.xticks(np.arange(0,55,step=5))
plt.savefig("Instance 7.png")
plt.close()

"""
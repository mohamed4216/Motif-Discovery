import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy.io as sio
import matplotlib.pylab as pylab
from SAXAlgo import SAX


#Load dataset
Data = sio.loadmat('ActivityDense.mat')['ActivityDense'] #Or use data: ActivitySparse.mat
DataAndLabels = Data[0,0]
RealLife = DataAndLabels[:,0]
Labels = DataAndLabels[:,1]


#Default WordSize(SAX)= 1000
Real_sx = SAX()
Real_Symbols = Real_sx.to_letter_rep(RealLife)
String = Real_Symbols[0]



Window_Size=6 #window size i.e. number of symbols in window
motif_list = [] # list of motif
time_list = [] # list of time stamp
x=[]
y=[]

#padding motif_list 
for index in range((len(String)-Window_Size+1)):
    s=String[index:index+Window_Size] 
    if not(s in motif_list):
        motif_list.append(s)
        list_temp = []
        list_temp.append(index)
        time_list.append(list_temp)
    else:
        time_list[motif_list.index(s)].append(index)

#sort motif_list and time_list 
Sorted_time = sorted(time_list, key=len, reverse=True)
Sorted_motif= []
for i in range(len(Sorted_time)):
	Sorted_motif.append(motif_list[time_list.index(Sorted_time[i])])

for i in range(len(Sorted_motif)):
    print Sorted_motif[i],Sorted_time[i]



#set up the list of clusters 
R=2
i=0
j=0
sx=SAX()
while i<len(Sorted_motif):
    j=i+1
    while j < len(Sorted_motif):
        d=sx.compare_strings(Sorted_motif[i],Sorted_motif[j])
        if(d<R):
            Sorted_motif.remove(Sorted_motif[j])
            Sorted_time.remove(Sorted_time[j])
 	j=j+1
    i=i+1

#motif search
motif_index=[]
motif_val=[]
for i in range(len(String)/Window_Size):
    i=i*Window_Size
    s= String[i:i+Window_Size]
    dmin=2
    val=0
    for motif in Sorted_motif:
        d=sx.compare_strings(s,motif)
        if(d<dmin):
            dmin=d
            val=Sorted_motif.index(motif)+1
	    
    motif_index.append(i)
    motif_val.append(val)
    motif_index.append(i)
    motif_val.append(val)

motif_index.append(i+Window_Size)
temp=[x *(len(RealLife)/1000.0)  for x in motif_index]

#plot(RealLife data, ground truth, predicted motifs)
plt.plot(RealLife, label = "ReallifeData", color = 'b')
plt.plot(Labels, label = "Ground Truth", linewidth = 3, color = 'g')
plt.plot(temp[1:],motif_val[:len(motif_val)],label = "Predicted", linewidth = 3, color = 'r')
plt.legend()
plt.xlabel('samples')
plt.ylabel('units')
plt.show()

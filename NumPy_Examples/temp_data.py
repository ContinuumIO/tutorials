
import glob
import datetime
import os.path

import numpy as np
from numba import autojit

start = datetime.date(1995, 1, 1)
stop = datetime.date(2013, 3, 1)

dates = np.arange(start, stop, dtype='datetime64[D]')
files = glob.glob('allsites/*.txt')
names = [os.path.splitext(os.path.basename(file))[0] for file in files]

temps = np.empty((len(dates), len(files)), float)
temps.fill(-99)
dt = np.dtype([('Month', 'int8'), ('Day', 'int8'), ('Year', 'int16'), ('Temp', 'float64')])

@autojit
def findN(vec, num, N):
    result = False
    count = 0
    for i in range(vec.shape[0]):
        if vec[i] == num:
            count += 1
        else:
            count = 0
        if count >= N:
            result = True
            break
    return result
        

# detect all duplicate entries
# detect entries with skipped days
# detect all 0-valued days
# detect data that doesn't fill the entire length of dates
def _detect(data, file, i):
    valid = True
    start = 0
    stop = len(data)+1
    indx0 = np.where(data['Day']==0)[0].tolist()
    if indx0:
        print indx0
        print "0-valued entries... %s, %i" % (file, i)
        valid = False
    
    datestrs = ['%d-%02d-%02d' % (x, y, z) for (x,y,z) in 
                zip(data['Year'], data['Month'], data['Day']) if z != 0]
    td = np.array(datestrs, dtype='datetime64[D]')

    if np.any(dates != td):
        print "Dates do not match... %s, %i" % (file, i)
        start = np.searchsorted(dates, td[0])
        stop = np.searchsorted(dates, td[-1]) + 1
        if td[-1] > dates[-1]:
            valid = False

    diff = td[1:] - td[:-1]
    indxs = np.where(diff == 0)[0].tolist()
    if indxs:
        print indxs
        print "Duplicates in %s, %i" % (file, i)
        valid = False

    indxd = np.where(diff > 1)[0].tolist()
    if indxd:
        print indxd
        print "Skipped dates in %s, %i" % (file, i)
        valid = False

    # Too many missing data...
    if findN(data['Temp'], -99.0, 5):
        valid = False
        print "Too many missing data in %s, %i" % (file, i)
        print np.where(data['Temp']==-99.0)[0].tolist()

    return start, stop, valid

kept = []

for i, file in enumerate(files):
    data = np.loadtxt(file, dtype=dt)
    start, stop, valid = _detect(data, file, i)
    if valid:
        temps[start:stop,i] = data['Temp']
        kept.append(i)
        
good = temps[:,kept]
good_names = [name for (i, name) in enumerate(names) if i in kept]

@autojit
def replace_bad_days(temp, val):
    M, N = temp.shape
    for place in range(N):
        day = 0
        while day < M:
            if temp[day, place] == val:
                top = 0
                start = day
                if (start == 0):
                    top = 1
                while (temp[day, place] == val) and day < M-1:
                    day += 1
                end = day
                if temp[end, place] == val: # bottom
                    for i in range(start, end+1):
                        temp[i,place] = temp[start-1,place]
                elif top == 1:
                    for i in range(start, end):
                        temp[i,place] = temp[end,place]

                else:
                    val1 = temp[start-1, val]
                    val2 = temp[end, val]
                    for i in range(start, end):
                        temp[i, place] = (val2*(i-start) + val1*(end-i))/(end-start)
            else:
                day += 1
                
replace_bad_days(good, -99.0)

print good.mean(axis=0)  # average over the dates
print good.mean(axis=-1)  # average over the locations on each day
print good.mean()   # total average over all the data.

month_values = np.unique(data['Month'])
months = {i: good[data['Month']==i,:].mean(axis=0) for i in month_values}
UTSALTLK = good_names.index('UTSALTLK')
print good_names[UTSALTLK]
for k in month_values:
    print "%d\t%f" % (k, months[k][UTSALTLK])


import pandas
df = pandas.DataFrame(good, dates, good_names)
monthly_means = df.groupby(data['Month']).mean()
print monthly_means.UTSALTLK

print monthly_means.TXWACO
print monthly_means.AGBUENOS
print monthly_means.AKJUNEAU

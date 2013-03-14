
import glob
import datetime
import os.path

import numpy as np

start = datetime.date(1995, 1, 1)
stop = datetime.date(2013, 3, 1)

dates = np.arange(start, stop, dtype='datetime64[D]')
files = glob.glob('allsites/*.txt')
names = [os.path.splitext(os.path.basename(file))[0] for file in files]

temps = np.empty((len(dates), len(files)), float)
dt = np.dtype([('Month', 'int8'), ('Day', 'int8'), ('Year', 'int16'), ('Temp', 'float64')])

for i, file in enumerate(files):
    data = np.loadtxt(file, dtype=dt)
    if len(data) < len(dates):
        datestrs = ['%d-%02d-%02d' % (x, y, z) for (x,y,z) in 
                    zip(data['Year'], data['Month'], data['Day'])]
        this_dates = np.array(datestrs, dtype='datetime64[D]')
        if (this_dates[-1]-this_dates[0] + 1) == len(this_dates):
            indxs = np.searchsorted(dates, [this_dates[0], this_dates[-1]])
            temps[indxs[0]:indxs[1]+1,i] = data['Temp']
        else:
            raise ValueError("Non monotonic dates in %s" % file)         
    else:
        temps[:,i] = data['Temp']
        

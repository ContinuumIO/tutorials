'''Each frame of the animation represents one minute of tweets. The animation runs at ten frames per second. 
I represent each tweet as a small white circle at two percent opacity. At the moment a tweet occurs I plot 
it at ten point size. Every minute that passes I drop the marker size by one point until it disappears.
'''

import numpy as np
import matplotlib.pyplot as plt
import datetime, time, pytz
from mpl_toolkits.basemap import Basemap, shiftgrid
import matplotlib.animation as animation
import csv

fig = plt.figure()

# lon_0 is central longitude of robinson projection.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='robin',lon_0=0,resolution='c')
#set a background colour
m.drawmapboundary(fill_color='#85A6D9')

# draw coastlines, country boundaries, fill continents.
m.fillcontinents(color='black',lake_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawcountries(color='#6D5F47', linewidth=.4)

# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(-180, 180, 30), color='#bbbbbb')
m.drawparallels(np.arange(-90, 90, 30), color='#bbbbbb')

scat_list = []
time = []
lat = []
lon = []

est=pytz.timezone('US/Eastern')        
with open('GeoBases_Output/geo_loc.csv', 'rb') as csvfile:
    geo_loc = csv.reader(csvfile, delimiter=',')
    for row in geo_loc:
        time.append(datetime.datetime.fromtimestamp(int(row[0]),est))
        lat.append(float(row[1]))
        lon.append(float(row[2]))

delta = time[0]-time[-1]
frame_size = 100
n_frames = delta.seconds/frame_size

# x,y = m(lon[:200],lat[:200])

# # scatter scaled circles at the city locations
# scat_plot = m.scatter(
#     x,
#     y,
#     c='white', #color
#     marker='o', #symbol
#     s=20,
#     alpha=0.2, #transparency
#     zorder = 2, #plotting order
#     )

plt.title('ClickStream Bitly USA ')

# def decay(n):
#     for i in range(n):
#         if i == 0:
#             x,y = m(lon[:frame_size-1],lat[:frame_size-1])
#             m.scatter(
#                 x,
#                 y,
#                 c='white', #color
#                 marker='o', #symbol
#                 s=max(20-n,0), #decay to 0
#                 alpha=0.2, #transparency
#                 zorder = 2, #plotting order
#                 )

#         else:
#             start = n*frame_size
#             stop = start+frame_size-1
#             x,y = m(lon[start:stop],lat[start:stop])
#             m.scatter(
#                 x,
#                 y,
#                 c='white', #color
#                 marker='o', #symbol
#                 s=max(20-n,0), #decay to 0
#                 alpha=0.2, #transparency
#                 zorder = 2, #plotting order
#                 )

def update(n):
    print n
    if n == 0:
        x,y = m(lon[:frame_size-1],lat[:frame_size-1])
    else:
        # decay(n)
        if scat_list == None:
            pass
        else:
            for s_plot in scat_list:
                pass
                # alpha = s_plot.get_alpha()
                # s_plot.set_alpha(max(alpha-0.01,0))
                s_plot._sizes -= 1
                if s_plot._sizes == 0:
                    scat_list.remove(s_plot)
                # s_plot._sizes = np.ma.masked_array(data = [np.random.randint(100,1000))
        start = n*frame_size
        stop = start+frame_size-1
        x,y = m(lon[start:stop],lat[start:stop])
        scat_plot = m.scatter(
            x,
            y,
            c='white', #color
            marker='o', #symbol
            alpha=0.2, #transparency
            s=20,
            zorder = 2, #plotting order
            )
        # scat_plot
        scat_list.append(scat_plot)



print 'num frames: ', n_frames
anim = animation.FuncAnimation(fig, update, frames=n_frames) #blit=True
anim.save('movie-1.mp4', fps=10, extra_args=['-vcodec', 'libx264'])

# anim.save('movie.mp4')

plt.show()
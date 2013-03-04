import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def main():
    global lst
    numframes = 100
    numpoints = 10
    color_data = np.random.random((numframes, numpoints))
    x, y, c = np.random.random((3, numpoints))

    fig = plt.figure()
    scat = plt.scatter(x, y, c=c, s=100)
    lst = []

    ani = animation.FuncAnimation(fig, update_plot, frames=xrange(numframes),
                                  fargs=(color_data, scat))
    
    # anim = animation.FuncAnimation(fig, update, frames=n_frames) #blit=True
    # ani.save('movie-1.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    print lst
    plt.show()

def update_plot(i, data, scat):
    global lst
    lst.append(i)
    print lst
    a = scat.set_array(data[i])
    scat.set_alpha(np.random.random(1))
    # return scat,

main()

# # example using matplotlib.animation to create a movie
# # reads data over http - needs an active internet connection.

# import numpy as np
# import matplotlib.pyplot as plt
# import numpy.ma as ma
# import datetime, time, pytz
# from mpl_toolkits.basemap import Basemap, shiftgrid
# from netCDF4 import Dataset as NetCDFFile, date2index, num2date
# import matplotlib.animation as animation

# # times for March 1993 'storm of the century'
# date1 = datetime.datetime(1993,3,10,0)
# date2 = datetime.datetime(1993,3,17,0)

# time = []
# lat = []
# lon = []
# est=pytz.timezone('US/Eastern')        
# with open('GeoBases_Output/geo_loc.csv', 'rb') as csvfile:
#     geo_loc = csv.reader(csvfile, delimiter=',')
#     for row in geo_loc:
#         time.append(datetime.datetime.fromtimestamp(int(row[0]),est))
#         lat.append(float(row[1]))
#         lon.append(float(row[2]))

# # read lats,lons,times.
# latitudes = lat
# longitudes = lon
# times = time


# m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)

# fig = plt.figure()
# ax = fig.add_axes([0.1,0.1,0.7,0.7])
# # set desired contour levels.
# clevs = np.arange(960,1061,5)
# # compute native x,y coordinates of grid.
# x, y = m(lons, lats)
# # define parallels and meridians to draw.
# parallels = np.arange(-80.,90,20.)
# meridians = np.arange(0.,360.,20.)
# # number of repeated frames at beginning and end is n1.
# nframe = 0; n1 = 10
# pos = ax.get_position()
# l, b, w, h = pos.bounds
# # loop over times, make contour plots, draw coastlines, 
# # parallels, meridians and title.
# nt = 0; date = dates[nt]
# CS1 = m.contour(x,y,slp[nt,:,:],clevs,linewidths=0.5,colors='k')
# CS2 = m.contourf(x,y,slp[nt,:,:],clevs,cmap=plt.cm.RdBu_r)
# # plot wind vectors on lat/lon grid.
# # rotate wind vectors to map projection coordinates.
# #urot,vrot = m.rotate_vector(u[nt,:,:],v[nt,:,:],lons,lats)
# # plot wind vectors over map.
# #Q = m.quiver(x,y,urot,vrot,scale=500) 
# # plot wind vectors on projection grid (looks better).
# # first, shift grid so it goes from -180 to 180 (instead of 0 to 360
# # in longitude).  Otherwise, interpolation is messed up.
# ugrid,newlons = shiftgrid(180.,u[nt,:,:],longitudes,start=False)
# vgrid,newlons = shiftgrid(180.,v[nt,:,:],longitudes,start=False)
# # transform vectors to projection grid.
# urot,vrot,xx,yy = m.transform_vector(ugrid,vgrid,newlons,latitudes,51,51,returnxy=True,masked=True)
# # plot wind vectors over map.
# Q = m.quiver(xx,yy,urot,vrot,scale=500,zorder=10)
# # make quiver key.
# qk = plt.quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
# # draw coastlines, parallels, meridians, title.
# m.drawcoastlines(linewidth=1.5)
# m.drawparallels(parallels)
# m.drawmeridians(meridians)
# txt = plt.title('SLP and Wind Vectors '+str(date))
# # plot colorbar on a separate axes (only for first frame)
# cax = plt.axes([l+w-0.05, b, 0.03, h]) # setup colorbar axes
# fig.colorbar(CS2,drawedges=True, cax=cax) # draw colorbar
# cax.text(0.0,-0.05,'mb')
# plt.axes(ax) # reset current axes

# def updatefig(nt):
#     global CS1,CS2,Q
#     date = dates[nt]
#     for c in CS1.collections: c.remove()
#     CS1 = m.contour(x,y,slp[nt,:,:],clevs,linewidths=0.5,colors='k')
#     for c in CS2.collections: c.remove()
#     CS2 = m.contourf(x,y,slp[nt,:,:],clevs,cmap=plt.cm.RdBu_r)
#     ugrid,newlons = shiftgrid(180.,u[nt,:,:],longitudes,start=False)
#     vgrid,newlons = shiftgrid(180.,v[nt,:,:],longitudes,start=False)
#     urot,vrot,xx,yy = m.transform_vector(ugrid,vgrid,newlons,latitudes,51,51,returnxy=True,masked=True)
#     txt.set_text('SLP and Wind Vectors '+str(date))
#     Q.set_UVC(urot,vrot)

# ani = animation.FuncAnimation(fig, updatefig, frames=len(dates))

# ani.save('movie.mp4')

# plt.show()
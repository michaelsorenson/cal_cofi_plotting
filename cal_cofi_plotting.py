import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import netCDF4 as ncdf
import numpy as np
import pandas as pd
import scipy as sp

def plot_cal_cofi_stations(path_to_stations, path_to_plot=None):
    """
    Plots Cal COFI stations as points on a geo map
    path_to_stations: absolute or relative path to the stations csv
    path_to_plot: absolute or relative path to save the plot (should be .png)
    """
    sites = pd.read_csv(path_to_stations)
    # Clean up dataframe
    sites["Line"] = "0" + sites["Line"].astype(str)
    sites["Sta"] = "0" + sites["Sta"].astype(str)
    sites["Sta"] = sites["Sta"].replace("0100.0", "100.0")
    sites["Sta"] = sites["Sta"].replace("0110.0", "110.0")
    sites["Sta"] = sites["Sta"].replace("0120.0", "120.0")
    sites['Sta_ID'] = sites['Line'].astype(str) + ' ' + sites['Sta'].astype(str)
    # Plot figure
    fig = plt.figure(figsize=(8, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    # add geo features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    # add gridlines and labels
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    # set the min and max longitude and latitude
    ax.set_extent([-127, -116, 29, 42], crs=ccrs.PlateCarree())
    # plot station points on map
    ax.scatter(x=sites['Lon (dec)'], y=sites['Lat (dec)'], color='black', s=7, transform=ccrs.PlateCarree())
    # save fig as png or return it
    if path_to_plot:
        fig.savefig(path_to_plot)
    else:
        return fig
    
def plot_cal_cofi_chlor(path_to_netcdf, path_to_plot=None):
    """
    Plots Cal COFI chlorophyll levels
    path_to_netcdf: absolute or relative path to the netcdf csv
    path_to_plot: absolute or relative path to save the plot (should be .png)
    """
    # Load netcdf
    file = ncdf.Dataset(path_to_netcdf)
    lat = file.variables['lat'][:]
    lon = file.variables['lon'][:]
    lon = lon - 360
    chl = file.variables['MWchla'][0][0][:][:]
    # Plot figure
    fig = plt.figure(figsize=(8, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    # create chlorophyl contours
    plt.contourf(lon, lat, chl, 60,
                 transform=ccrs.PlateCarree())
    # create meshgrid
    x, y = np.meshgrid(lon, lat)
    # set the min and max longitude and latitude
    ax.set_extent([-127, -116, 29, 42], crs=ccrs.PlateCarree())
    # add geo features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    # create chlorophyll color map
    cmap = ax.pcolormesh(x,y,chl,norm=colors.LogNorm(vmin=0.1,vmax=10), rasterized=True, transform=ccrs.PlateCarree())
    # add legend color bar and label
    cbar = plt.colorbar(cmap, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Chlorophyll $\mathit{a}$ (mg $\mathregular{m^{-3}}$)', fontsize=14)
    # save fig as png or return it
    if path_to_plot:
        fig.savefig(path_to_plot)
    else:
        return fig
    
def main():
    plot_cal_cofi_stations('CalCOFIStationOrder.csv', 'CalCOFIStations.png')
    plot_cal_cofi_chlor('MW2022275_2022275_chla.nc', 'CalCOFIChlorophyll.png')

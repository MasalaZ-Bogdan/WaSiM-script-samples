#   A simple script that takes a glacier cover raster clipped to the extent
#   of your catchment in your WaSiM project, and creates the glc and glid raster files from it.
#   Created when GIS functions were frustrating me

import numpy as np
import os
# import pandas as pd
import rasterio

#set directory paths and filenames
path_init = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup\\Init'
path_input = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup\\Input'
fname_test = '1850_eurac.asc'
#fname_control = 'glc_2006_larger_domain.asc'
fname_ezg = 'dem_25_2006_large.ezg'

#open clipped glacier raster
gi_1850_ds = rasterio.open(os.path.join(path_init,fname_test))
gi_1850 = gi_1850_ds.read(1)
#make copy with data values set to 0
gi_1850_0 = gi_1850.copy()
gi_1850_0[gi_1850_0 >= 0] = 0
#create glc raster variable and set all data values in glacier raster to 1
glc_1850 = gi_1850.copy()
glc_1850[glc_1850 >= 0] = 1

#open subcatchment raster ezg
ezg_ds = rasterio.open(os.path.join(path_input,fname_ezg))
ezg = ezg_ds.read(1)
#make copy with data values set to 0 
ezg_0 = ezg.copy()
ezg_0[ezg_0 >= 0] = 0

#add glc raster and zeroed subcatchment raster
glc_1850_ezg = glc_1850 + ezg_0
#set all negative values to nodata values of -9999
glc_1850_ezg[glc_1850_ezg < 0] = -9999
#make copy of glc ezg raster with data values set to 0
glc_1850_ezg_0 = glc_1850_ezg.copy()
glc_1850_ezg_0[glc_1850_ezg_0 > 0] = 0
#add subcatchment raster to zeroed glc ezg raster to get glid raster
glid_1850_ezg = glc_1850_ezg_0 + ezg
#set all negative values to nodata values of -9999
glid_1850_ezg[glid_1850_ezg < 0] = -9999 

#print rasters
#set profile
kwds_ezg = ezg_ds.profile
#kwds_ezg['driver'] = 'GTiff'
#check which driver is best

#glc raster
glc_file = rasterio.open(os.path.join(path_init,'glc_1850.asc'), 'w', **kwds_ezg)
glc_file.write(glc_1850_ezg,1)
glc_file.close()
#glid raster
glid_file = rasterio.open(os.path.join(path_init,'glid_1850.asc'), 'w', **kwds_ezg)
glid_file.write(glid_1850_ezg,1)
glid_file.close()

gi_1850_ds.close()
ezg_ds.close()










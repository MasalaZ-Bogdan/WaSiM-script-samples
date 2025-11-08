'''
This script takes ASCII files of Langenferner glacier extent (or your glacier of interest) which may have
data values outside of your catchment area, and "clips" them to the extent of your catchment defined in your
WaSiM project. Needs an existing subcatchment file (ending in ".ezg").

'''

import numpy as np
import os
import pandas as pd
from datetime import datetime as dt
import re
import rasterio
path = os.getcwd() 
import sys
sys.path.insert(0, path)
import shutil as sh

#needed: dictionaries for file names and functions for raster operations

#set directory paths and filenames
path_init = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup\\Init' #WaSiM init folder
path_input = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup\\Input' #WaSiM input folder
path_langenferner = os.path.join(path_init,'langenferner')

#variable names of langenferner raster files, derived from langenferner shapefiles cut from glims and sudtirol datasets

lang_1997_fname = 'langenferner_1997_buergernetz.asc'
lang_2000_fname = 'langenferner_2000_glims.asc'
lang_2003_fname = 'langenferner_2003_glims.asc'
lang_2005_fname = 'langenferner_2005_buergernetz.asc'
lang_2014_fname = 'langenferner_2014_glims.asc'
lang_2017_fname = 'langenferner_2017_buergernetz.asc'

#subcatchment raster as base
fname_ezg = 'dem_25_2006_large.ezg'

#open subcatchment raster
ezg_ds = rasterio.open(os.path.join(path_input, fname_ezg))
ezg = ezg_ds.read(1)
#make copy with data values set to 0
ezg_0 = ezg.copy()
ezg_0[ezg_0 >= 0] = 0

#clip langenferner glaciers to extent of subcatchment
#################### 1997 raster ###############################
lang_1997_ds = rasterio.open(os.path.join(path_langenferner, lang_1997_fname))
lang_1997 = lang_1997_ds.read(1)
#make copy with data values set to 0
lang_1997_0 = lang_1997.copy()
lang_1997_0[lang_1997_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_1997_ezg = lang_1997_0 + ezg_0
#set all negative values to nodata value of -9999
lang_1997_ezg[lang_1997_ezg < 0] = -9999

##################### 2000 raster ##############################
lang_2000_ds = rasterio.open(os.path.join(path_langenferner, lang_2000_fname))
lang_2000 = lang_2000_ds.read(1)
#make copy with data values set to 0
lang_2000_0 = lang_2000.copy()
lang_2000_0[lang_2000_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_2000_ezg = lang_2000_0 + ezg_0
#set all negative values to nodata value of -9999
lang_2000_ezg[lang_2000_ezg < 0] = -9999

##################### 2003 raster ##############################
lang_2003_ds = rasterio.open(os.path.join(path_langenferner, lang_2003_fname))
lang_2003 = lang_2003_ds.read(1)
#make copy with data values set to 0
lang_2003_0 = lang_2003.copy()
lang_2003_0[lang_2003_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_2003_ezg = lang_2003_0 + ezg_0
#set all negative values to nodata value of -9999
lang_2003_ezg[lang_2003_ezg < 0] = -9999

##################### 2005 raster ##############################
lang_2005_ds = rasterio.open(os.path.join(path_langenferner, lang_2005_fname))
lang_2005 = lang_2005_ds.read(1)
#make copy with data values set to 0
lang_2005_0 = lang_2005.copy()
lang_2005_0[lang_2005_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_2005_ezg = lang_2005_0 + ezg_0
#set all negative values to nodata value of -9999
lang_2005_ezg[lang_2005_ezg < 0] = -9999

##################### 2014 raster ##############################
lang_2014_ds = rasterio.open(os.path.join(path_langenferner, lang_2014_fname))
lang_2014 = lang_2014_ds.read(1)
#make copy with data values set to 0
lang_2014_0 = lang_2014.copy()
lang_2014_0[lang_2014_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_2014_ezg = lang_2014_0 + ezg_0
#set all negative values to nodata value of -9999
lang_2014_ezg[lang_2014_ezg < 0] = -9999

##################### 2017 raster ##############################
lang_2017_ds = rasterio.open(os.path.join(path_langenferner, lang_2017_fname))
lang_2017 = lang_2017_ds.read(1)
#make copy with data values set to 0
lang_2017_0 = lang_2017.copy()
lang_2017_0[lang_2017_0 >= 0] = 0

#add langenferner raster and zeroed  subcatchment raster
lang_2017_ezg = lang_2017_0 + ezg_0
#set all negative values to nodata value of -9999
lang_2017_ezg[lang_2017_ezg < 0] = -9999

#write rasters
#set profile
kwds_ezg = ezg_ds.profile

#1997
lang_1997_file = rasterio.open(os.path.join(path_init,'langenferner_1997.asc'), 'w', **kwds_ezg)
lang_1997_file.write(lang_1997_ezg,1)
lang_1997_file.close()
#2000
lang_2000_file = rasterio.open(os.path.join(path_init,'langenferner_2000.asc'), 'w', **kwds_ezg)
lang_2000_file.write(lang_2000_ezg,1)
lang_2000_file.close()
#2003
lang_2003_file = rasterio.open(os.path.join(path_init,'langenferner_2003.asc'), 'w', **kwds_ezg)
lang_2003_file.write(lang_2003_ezg,1)
lang_2003_file.close()
#2005
lang_2005_file = rasterio.open(os.path.join(path_init,'langenferner_2005.asc'), 'w', **kwds_ezg)
lang_2005_file.write(lang_2005_ezg,1)
lang_2005_file.close()
#2014
lang_2014_file = rasterio.open(os.path.join(path_init,'langenferner_2014.asc'), 'w', **kwds_ezg)
lang_2014_file.write(lang_2014_ezg,1)
lang_2014_file.close()
#2017
lang_2017_file = rasterio.open(os.path.join(path_init,'langenferner_2017.asc'), 'w', **kwds_ezg)
lang_2017_file.write(lang_2017_ezg,1)
lang_2017_file.close()

#close open datasets
lang_1997_ds
lang_2000_ds
lang_2003_ds
lang_2005_ds
lang_2014_ds
lang_2017_ds
ezg_ds.close()

#end!







#   Script for computing fractional snow-covered area and 
#   snow cover duration for your catchment
import spotpy
import numpy as np
import os
import pandas as pd
import subprocess
from datetime import datetime as dt
import re
import rasterio
path = os.getcwd() 
import sys
sys.path.insert(0, path)
import shutil as sh
from dateutil.parser import parse

#numerous functions and additional loops needed for efficiency and aesthetics of code

#working directory change to output folder for calculations or not?
path = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup'

#Folder names and parameter configuration
folder_names = []
i=0
for i in range(1010):
    folder_names.append('output_run_thesis_cal' + str(i+1))

#Read the glacier extents raster
path_input = 'C:\\Users\\Asus\\Documents\\Thesis\\WaSiM_setup\\Input'
glc_2006_ds = rasterio.open(os.path.join(path_input,'glc_2006_larger_domain.asc'))
glc_2006 = glc_2006_ds.read(1)
glc_2006[glc_2006 == -9999] = 0
glc_2006[glc_2006 == 1] = 10

for n in range(1010):
    #print(n)
    ssto_list = []    
    output_folder = os.path.join(path, folder_names[n])
    #for individual folders
    output_folder = os.path.join(path, 'output_run_snowSA_748_9year')
    ssto_list = []
    print(output_folder)
    
    for ssto_file in os.listdir(output_folder):
        if ssto_file.startswith('sstodem_25_2006_large_'):
            ssto_list.append(os.path.join(output_folder, ssto_file))
    
    fsc_values = pd.DataFrame({'date': [], 'fsc_mean': [], 'fsc_sd': []})
  
    date_pattern = r'(\d{4}\.\d{2})'
    date_search = []
    for s in ssto_list:
        date_search.append(re.search(date_pattern,s).group())
    fsc_values['date'] = pd.to_datetime(date_search,format='%y%m.%d')
    fsc_values['date'] = pd.to_datetime(fsc_values['date']).dt.date
    
    ssto_list_fsc = ssto_list.copy()

    for x in range(len(ssto_list_fsc)):
        
        ssto_raster_ds = rasterio.open(ssto_list_fsc[x])#(ssto_list[1])
        ssto_raster = ssto_raster_ds.read(1)
        ssto_raster_glc = ssto_raster + glc_2006

        ssto_raster_glc_final = ssto_raster_glc.copy()
        ssto_raster_glc_final[(ssto_raster_glc_final>=0) & (ssto_raster_glc_final<5)] = 0
        ssto_raster_glc_final[(ssto_raster_glc_final>=5) & (ssto_raster_glc_final<1000)] = 1
        ssto_raster_glc_final[(ssto_raster_glc_final>=1000) & (ssto_raster_glc_final<50000)] = 1
        
        #mask_ssto_raster_glc_final = ssto_raster_glc_final<0
        
        ssto_raster_glc_final_calc = ssto_raster_glc_final.copy()
        ssto_raster_glc_final_calc[ssto_raster_glc_final_calc == -9999] = 'nan'

        fsc_values.iloc[x,1] = round(np.nanmean(ssto_raster_glc_final_calc),2)
        fsc_values.iloc[x,2] = round(np.nanstd(ssto_raster_glc_final_calc),2)

        kwds_fsc = ssto_raster_ds.profile

        snow_map_raster_file_path =  output_folder + '\\Snow_maps_' + str(fsc_values.loc[x,'date']) + '.asc'
        
        snow_map_raster_file = rasterio.open(snow_map_raster_file_path, mode = 'w', **kwds_fsc)
        #snow_map_raster_file = rasterio.open(snow_map_raster_file_path, mode='w', driver='GTiff', width = ssto_raster_ds.shape[1], height = ssto_raster_ds.shape[0], count = 1, dtype = 'float32', transform = ssto_raster_ds.transform)#crs = ssto_raster_ds.crs
        snow_map_raster_file.write(ssto_raster_glc_final,1)
        snow_map_raster_file.close()
        
    fsc_values_table_path = output_folder + '\\table_fsc.csv'
    fsc_values.to_csv(fsc_values_table_path, sep = ',', index = False)

    snow_maps_list = []    

    for snow_maps_file in os.listdir(output_folder):
        if snow_maps_file.startswith('Snow_maps_'):
            snow_maps_list.append(os.path.join(output_folder, snow_maps_file))

    snow_maps_list_allyears = snow_maps_list
    snow_maps_list_hyear1 = snow_maps_list[0:365] 
    snow_maps_list_hyear2 = snow_maps_list[365:731] 
    snow_maps_list_hyear3 = snow_maps_list[731:1096]
    snow_maps_list_hyear4 = snow_maps_list[1096:1461]

    # snow_maps_raster_allyears_ds = rasterio.open(snow_maps_list_allyears[0])#(ssto_list[1])
    # snow_maps_raster_allyears = snow_maps_raster_allyears_ds.read(1)
    # loop_allyears = len(snow_maps_list_allyears)-1
    
    snow_maps_raster_hyear1_ds = rasterio.open(snow_maps_list_hyear1[0])#(ssto_list[1])
    snow_maps_raster_hyear1 = snow_maps_raster_hyear1_ds.read(1)
    loop_hyear1 = len(snow_maps_list_hyear1)-1
    
    snow_maps_raster_hyear2_ds = rasterio.open(snow_maps_list_hyear2[0])#(ssto_list[1])
    snow_maps_raster_hyear2 = snow_maps_raster_hyear2_ds.read(1)
    loop_hyear2 = len(snow_maps_list_hyear2)-1
    
    snow_maps_raster_hyear3_ds = rasterio.open(snow_maps_list_hyear3[0])#(ssto_list[1])
    snow_maps_raster_hyear3 = snow_maps_raster_hyear3_ds.read(1)
    loop_hyear3 = len(snow_maps_list_hyear3)-1
    
    snow_maps_raster_hyear4_ds = rasterio.open(snow_maps_list_hyear4[0])#(ssto_list[1])
    snow_maps_raster_hyear4 = snow_maps_raster_hyear4_ds.read(1)
    loop_hyear4 = len(snow_maps_list_hyear4)-1
    
    scd_values = pd.DataFrame({'hydrological year': [], 'scd_mean': [], 'scd_sd': [], 'scd_norm_mean':[], 'scd_norm_sd':[]})
    scd_values['hydrological year']=['all years',1,2,3,4]

    kwds_scd = ssto_raster_ds.profile
        
    for b in range(loop_hyear1):
        snow_maps_raster_hyear1_add_ds = rasterio.open(snow_maps_list_hyear1[b+1])
        snow_maps_raster_hyear1_add = snow_maps_raster_hyear1_add_ds.read(1)
        snow_maps_raster_hyear1_add[snow_maps_raster_hyear1_add == -9999] = 0
        snow_maps_raster_hyear1 = snow_maps_raster_hyear1 + snow_maps_raster_hyear1_add
        
    snow_maps_raster_hyear1_norm = snow_maps_raster_hyear1.astype(float, copy = True)
    snow_maps_raster_hyear1_norm = snow_maps_raster_hyear1_norm/365
    snow_maps_raster_hyear1_norm[snow_maps_raster_hyear1_norm < 0] = -9999
    snow_maps_raster_hyear1_norm = np.round(snow_maps_raster_hyear1_norm,2)
          
    scd_raster_file_path_hyear1 =  output_folder + '\\Snow_cover_duration_hyear1.asc'       
    scd_raster_file_hyear1 = rasterio.open(scd_raster_file_path_hyear1, mode = 'w', **kwds_scd )
    scd_raster_file_hyear1.write(snow_maps_raster_hyear1,1)
    scd_raster_file_hyear1.close()
               
    scd_raster_file_path_hyear1_norm =  output_folder + '\\Snow_cover_duration_hyear1_normalized.asc'       
    scd_raster_file_hyear1_norm = rasterio.open(scd_raster_file_path_hyear1_norm, mode = 'w', **kwds_scd )
    scd_raster_file_hyear1_norm.write(snow_maps_raster_hyear1_norm,1)
    scd_raster_file_hyear1_norm.close()
        #rounding problem in written raster
        
    snow_maps_raster_hyear1_calc = snow_maps_raster_hyear1.astype(float, copy = True)
    #np.float(snow_maps_raster_hyear1.copy())
    snow_maps_raster_hyear1_calc[snow_maps_raster_hyear1_calc == -9999] = 'nan'
    scd_values.iloc[1,1] = round(np.nanmean(snow_maps_raster_hyear1_calc),2)
    scd_values.iloc[1,2] = round(np.nanstd(snow_maps_raster_hyear1_calc),2)
        
    snow_maps_raster_hyear1_norm_calc = snow_maps_raster_hyear1_norm.copy()
    snow_maps_raster_hyear1_norm_calc[snow_maps_raster_hyear1_norm_calc == -9999] = 'nan'
    scd_values.iloc[1,3] = round(np.nanmean(snow_maps_raster_hyear1_norm_calc),2)
    scd_values.iloc[1,4] = round(np.nanstd(snow_maps_raster_hyear1_norm_calc),2)
        
    for c in range(loop_hyear2):
        snow_maps_raster_hyear2_add_ds = rasterio.open(snow_maps_list_hyear2[c+1])
        snow_maps_raster_hyear2_add = snow_maps_raster_hyear2_add_ds.read(1)
        snow_maps_raster_hyear2_add[snow_maps_raster_hyear2_add == -9999] = 0
        snow_maps_raster_hyear2 = snow_maps_raster_hyear2 + snow_maps_raster_hyear2_add
        
    snow_maps_raster_hyear2_norm = snow_maps_raster_hyear2.astype(float, copy = True)
    snow_maps_raster_hyear2_norm = snow_maps_raster_hyear2_norm/366
    snow_maps_raster_hyear2_norm[snow_maps_raster_hyear2_norm < 0] = -9999
    snow_maps_raster_hyear2_norm = np.round(snow_maps_raster_hyear2_norm,2)
        
    
    scd_raster_file_path_hyear2 =  output_folder + '\\Snow_cover_duration_hyear2.asc'       
    scd_raster_file_hyear2 = rasterio.open(scd_raster_file_path_hyear2, mode = 'w', **kwds_scd )
    scd_raster_file_hyear2.write(snow_maps_raster_hyear2,1)
    scd_raster_file_hyear2.close()
               
    scd_raster_file_path_hyear2_norm =  output_folder + '\\Snow_cover_duration_hyear2_normalized.asc'       
    scd_raster_file_hyear2_norm = rasterio.open(scd_raster_file_path_hyear2_norm, mode = 'w', **kwds_scd )
    scd_raster_file_hyear2_norm.write(snow_maps_raster_hyear2_norm,1)
    scd_raster_file_hyear2_norm.close()
        #rounding problem in written raster
        
    snow_maps_raster_hyear2_calc = snow_maps_raster_hyear2.astype(float, copy = True)
    snow_maps_raster_hyear2_calc[snow_maps_raster_hyear2_calc <0] = 'nan'
    scd_values.iloc[2,1] = round(np.nanmean(snow_maps_raster_hyear2_calc),2)
    scd_values.iloc[2,2] = round(np.nanstd(snow_maps_raster_hyear2_calc),2)
        
    snow_maps_raster_hyear2_norm_calc = snow_maps_raster_hyear2_norm.copy()
    snow_maps_raster_hyear2_norm_calc[snow_maps_raster_hyear2_norm_calc == -9999] = 'nan'
    scd_values.iloc[2,3] = round(np.nanmean(snow_maps_raster_hyear2_norm_calc),2)
    scd_values.iloc[2,4] = round(np.nanstd(snow_maps_raster_hyear2_norm_calc),2)
        
    for d in range(loop_hyear3):
        snow_maps_raster_hyear3_add_ds = rasterio.open(snow_maps_list_hyear3[d+1])
        snow_maps_raster_hyear3_add = snow_maps_raster_hyear3_add_ds.read(1)
        snow_maps_raster_hyear3_add[snow_maps_raster_hyear3_add == -9999] = 0
        snow_maps_raster_hyear3 = snow_maps_raster_hyear3 + snow_maps_raster_hyear3_add
        
    snow_maps_raster_hyear3_norm = snow_maps_raster_hyear3.astype(float, copy = True)
    snow_maps_raster_hyear3_norm = snow_maps_raster_hyear3_norm/365
    snow_maps_raster_hyear3_norm[snow_maps_raster_hyear3_norm < 0] = -9999
    snow_maps_raster_hyear3_norm = np.round(snow_maps_raster_hyear3_norm,2)
    
    scd_raster_file_path_hyear3 =  output_folder + '\\Snow_cover_duration_hyear3.asc'       
    scd_raster_file_hyear3 = rasterio.open(scd_raster_file_path_hyear3, mode = 'w', **kwds_scd )
    scd_raster_file_hyear3.write(snow_maps_raster_hyear3,1)
    scd_raster_file_hyear3.close()
               
    scd_raster_file_path_hyear3_norm =  output_folder + '\\Snow_cover_duration_hyear3_normalized.asc'       
    scd_raster_file_hyear3_norm = rasterio.open(scd_raster_file_path_hyear3_norm, mode = 'w', **kwds_scd )
    scd_raster_file_hyear3_norm.write(snow_maps_raster_hyear3_norm,1)
    scd_raster_file_hyear3_norm.close()
        #rounding problem in written raster
        
    snow_maps_raster_hyear3_calc = snow_maps_raster_hyear3.astype(float, copy = True)
    snow_maps_raster_hyear3_calc[snow_maps_raster_hyear3_calc == -9999] = 'nan'
    scd_values.iloc[3,1] = round(np.nanmean(snow_maps_raster_hyear3_calc),2)
    scd_values.iloc[3,2] = round(np.nanstd(snow_maps_raster_hyear3_calc),2)
        
    snow_maps_raster_hyear3_norm_calc = snow_maps_raster_hyear3_norm.copy()
    snow_maps_raster_hyear3_norm_calc[snow_maps_raster_hyear3_norm_calc == -9999] = 'nan'
    scd_values.iloc[3,3] = round(np.nanmean(snow_maps_raster_hyear3_norm_calc),2)
    scd_values.iloc[3,4] = round(np.nanstd(snow_maps_raster_hyear3_norm_calc),2)
        
    for e in range(loop_hyear4):
        snow_maps_raster_hyear4_add_ds = rasterio.open(snow_maps_list_hyear4[e+1])
        snow_maps_raster_hyear4_add = snow_maps_raster_hyear4_add_ds.read(1)
        snow_maps_raster_hyear4_add[snow_maps_raster_hyear4_add == -9999] = 0
        snow_maps_raster_hyear4 = snow_maps_raster_hyear4 + snow_maps_raster_hyear4_add
        
    snow_maps_raster_hyear4_norm = snow_maps_raster_hyear4.astype(float, copy = True)
    snow_maps_raster_hyear4_norm = snow_maps_raster_hyear4_norm/365
    snow_maps_raster_hyear4_norm[snow_maps_raster_hyear4_norm < 0] = -9999
    snow_maps_raster_hyear4_norm = np.round(snow_maps_raster_hyear4_norm,2)
    
    scd_raster_file_path_hyear4 =  output_folder + '\\Snow_cover_duration_hyear4.asc'       
    scd_raster_file_hyear4 = rasterio.open(scd_raster_file_path_hyear4, mode = 'w', **kwds_scd )
    scd_raster_file_hyear4.write(snow_maps_raster_hyear4,1)
    scd_raster_file_hyear4.close()
               
    scd_raster_file_path_hyear4_norm =  output_folder + '\\Snow_cover_duration_hyear4_normalized.asc'       
    scd_raster_file_hyear4_norm = rasterio.open(scd_raster_file_path_hyear4_norm, mode = 'w', **kwds_scd )
    scd_raster_file_hyear4_norm.write(snow_maps_raster_hyear4_norm,1)
    scd_raster_file_hyear4_norm.close()
        #rounding problem in written raster
        
    snow_maps_raster_hyear4_calc = snow_maps_raster_hyear4.astype(float, copy = True)
    snow_maps_raster_hyear4_calc[snow_maps_raster_hyear4_calc == -9999] = 'nan'
    scd_values.iloc[4,1] = round(np.nanmean(snow_maps_raster_hyear4_calc),2)
    scd_values.iloc[4,2] = round(np.nanstd(snow_maps_raster_hyear4_calc),2)
        
    snow_maps_raster_hyear4_norm_calc = snow_maps_raster_hyear4_norm.copy()
    snow_maps_raster_hyear4_norm_calc[snow_maps_raster_hyear4_norm_calc == -9999] = 'nan'
    scd_values.iloc[4,3] = round(np.nanmean(snow_maps_raster_hyear4_norm_calc),2)
    scd_values.iloc[4,4] = round(np.nanstd(snow_maps_raster_hyear4_norm_calc),2)
        
    # for a in len(snow_maps_list_allyears):
    #     snow_maps_raster_allyears_add_ds = rasterio.open(snow_maps_list_allyears[a+1])
    #     snow_maps_raster_allyears_add = snow_maps_raster_allyears_add_ds.read(1)
    #     snow_maps_raster_allyears = snow_maps_raster_allyears + snow_maps_raster_allyears_add
        
    #     snow_maps_raster_allyears_norm = snow_maps_raster_allyears/1461 #len(snow_maps_list_allyears)
    
    snow_maps_raster_allyears = snow_maps_raster_hyear1 + snow_maps_raster_hyear2 + snow_maps_raster_hyear3 + snow_maps_raster_hyear4
    snow_maps_raster_allyears[snow_maps_raster_allyears<0] = -9999
    snow_maps_raster_allyears_norm = snow_maps_raster_allyears.astype(float, copy = True)
    snow_maps_raster_allyears_norm = snow_maps_raster_allyears_norm/1461
    snow_maps_raster_allyears_norm[snow_maps_raster_allyears_norm < 0] = -9999
    snow_maps_raster_allyears_norm = np.round(snow_maps_raster_allyears_norm,2)
    
    scd_raster_file_path_allyears =  output_folder + '\\Snow_cover_duration_allyears.asc'       
    scd_raster_file_allyears = rasterio.open(scd_raster_file_path_allyears, mode = 'w', **kwds_scd )
    scd_raster_file_allyears.write(snow_maps_raster_allyears,1)
    scd_raster_file_allyears.close()
               
    scd_raster_file_path_allyears_norm =  output_folder + '\\Snow_cover_duration_allyears_normalized.asc'       
    scd_raster_file_allyears_norm = rasterio.open(scd_raster_file_path_allyears_norm, mode = 'w', **kwds_scd )
    scd_raster_file_allyears_norm.write(snow_maps_raster_allyears_norm,1)
    scd_raster_file_allyears_norm.close()
    
    snow_maps_raster_allyears_calc = snow_maps_raster_allyears.astype(float, copy = True)
    snow_maps_raster_allyears_calc[snow_maps_raster_allyears_calc == -9999] = 'nan'
    scd_values.iloc[0,1] = round(np.nanmean(snow_maps_raster_allyears_calc),2)
    scd_values.iloc[0,2] = round(np.nanstd(snow_maps_raster_allyears_calc),2)
        
    snow_maps_raster_allyears_norm_calc = snow_maps_raster_allyears_norm.copy()
    snow_maps_raster_allyears_norm_calc[snow_maps_raster_allyears_norm_calc == -9999] = 'nan'
    scd_values.iloc[0,3] = round(np.nanmean(snow_maps_raster_allyears_norm_calc),2)
    scd_values.iloc[0,4] = round(np.nanstd(snow_maps_raster_allyears_norm_calc),2)
    
    scd_values_table_path = output_folder + '\\table_scd.csv'
    scd_values.to_csv(scd_values_table_path, sep = ',', index = False)

    ssto_raster_ds.close()

    for ssto_file_del in os.listdir(output_folder):
        if ssto_file_del.startswith('sstodem_25_2006_large_'):
            os.unlink(os.path.join(output_folder,ssto_file_del))   #ssto_list.append(os.path.join(output_folder, ssto_file))
      
    snow_maps_raster_hyear1_ds.close() 
    snow_maps_raster_hyear2_ds.close() 
    snow_maps_raster_hyear3_ds.close() 
    snow_maps_raster_hyear4_ds.close() 
    snow_maps_raster_hyear1_add_ds.close()
    snow_maps_raster_hyear2_add_ds.close()
    snow_maps_raster_hyear3_add_ds.close()
    snow_maps_raster_hyear4_add_ds.close()

    for snow_maps_file_del in os.listdir(output_folder):
        if snow_maps_file_del.startswith('Snow_maps_'):
            os.unlink(os.path.join(output_folder, snow_maps_file_del))
                
#end?


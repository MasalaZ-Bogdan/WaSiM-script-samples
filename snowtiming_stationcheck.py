'''
When using model-based weather data, ground observation time series can not necessarily be used for goodness-of-fit
testing. This script computes the "snow days" of observed and simulated time series for a particular measurement 
station. Snow days are defined as days where SWE (snow water equivalent) is increasing. Goodness-of-fit between 
the observed and simulated snow day time series is then computed.
This script can also be generalized for goodness-of-fit testing of any time series.
'''

#import libraries
import numpy as np
import pandas as pd
import os
from datetime import datetime as dt
from dateutil.parser import parse
import math
import matplotlib.pyplot as plt   

#set path of working directory
path = os.getcwd() 

#set directory paths and filenames
#path to the observations file
observations_filepath = 'observed_SWE.txt'
#path to the output file
output_filepath = 'simulated_ssto_SWE_sday.stat'

#list of simulated series to be used for comparison against observations:
#sday, snow rate for subcatchment, otherSnowData at specific grid cell, point from WRF data, 

#complete function
##############################################################################################################################################################################
def snow_days_timing(observations_filepath, output_filepath):
    
    #calculate days of increasing SWE (snow water equivalent), or just snow depth, in observations
    station_snow_observations = pd.read_csv(observations_filepath, sep = ',', engine = 'python', parse_dates = True) #defaults: ',' sep, 'python' engine, 'parse_dates=True'
    
    #select the time period from the observational time series that corresponds to the simulation period
    observations_period_simulation = station_snow_observations[Nstart:Nend]
    
    #initialize array for snow days, with binary values: 1 for a day of increasing SWE, 0 for a day of decreasing SWE
    observed_snow_days = np.zeros(len(observations_relevant))
    a = 0
    
    for a in range(len(observed_snow_days)-1):
        if float(observations_period_simulation.loc[a+Nstart+1, 'select_column']) > float(observations_period_simulation[a+Nstart, 'select_column']):
            observed_snow_days[a+1] = 1
        else:
            observed_snow_days[a+1] = 0    

    #then, calculate days of increasing SWE in an output series
    output_snow_series = np.loadtxt(output_filepath, dtype = str, skiprows = Nskip, usecols = (N1...Nn)) #look through file to select Nskip and usecols(N1...Nn)
    
    #initialize array for snow days, with binary values: 1 for a day of increasing SWE, 0 for a day of decreasing SWE    
    output_snow_days = np.zeros(len(output_snow_series))
    b = 0
    
    for b in range(len(output_snow_days)-1):
        if output_snow_series[b+2, Nselect_column] > output_snow_series[b+1, Nselect_column]:
            output_snow_days[b+1] = 1
        else:
            output_snow_days[b+1] = 0

    #use root mean squared error (RMSE) as default, other criteria can be used  
    RMSE = math.sqrt(np.square(observed_snow_days - output_snow_days).mean())
    
    #optional step: create dataframe
    SWE_compare = pd.DataFrame({'date':[], 'observed_SWE':[], 'output_SWE':[]})
    SWE_compare['date'] = pd.date_range(start = 'YYYY-MM-DD', end = 'YYYY-MM-DD', freq = 'D') #start and end dates of the simulation period
    SWE_compare['date'] = SWE_compare['date'].dt.date
    SWE_compare['observed_SWE'] = observations_period_simulation
    SWE_compare['output_SWE'] = output_snow_series

    #optional step: plot time series
    SWE_compare = SWE_compare.set_index('date')
    
    #Adjusting the figure size
    fig = plt.subplots(figsize=(10, 5))
    #x axis
    plt.xlim(SWE_compare.index.min(), SWE_compare.index.max())
    ticks = list(SWE_compare.index)
    plt.xticks(ticks, rotation=45)
    #Rotaing axis ticks and customizing their font size
    plt.xticks(rotation=30, fontsize=15)
    
    for column in ['observed_SWE', 'output_SWE']:
        plt.plot(SWE_compare.index, SWE_compare[column], markersize = 1)
    
    #return RMSE, or as many goodness-of-fit criteria as applicable
    return RMSE
    
    #end function
##############################################################################################################################################################################
        
#run function
RMSE = snow_days_timing(observations_filepath, output_filepath)
    
#end

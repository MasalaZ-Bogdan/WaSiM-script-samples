'''
Early and basic version of a script that runs a batch a WaSiM simulations. Needs an array of parameter combinations,
which can be created using the SAFE Toolbox. Does not include data processing. The script has three basic steps:
1.  Creates an output folder for each simulation
2.  Modifies the WaSiM control file, creates a copy in each simulation folder, 
3.  Runs the WaSiM executable with the corresponding control file.

'''

#import libraries
import numpy as np
import os
import subprocess
import shutil as sh

#get and set path of working directory
path = os.getcwd() 
os.chdir(working directory)

#set directory paths and filepaths
parameter_set_matrix_filepath = 'parameter matrix filepath'
WaSiM_main_directory = 'main_directory'
WaSiM_control_folder = 'control folder'
#define names of WaSiM executables and control file
wasim_executable = 'wasim executable' #.exe
control_file = 'control file' #.bash

##############################################################################################################################################################################
def substitute_line(oldline, newline, txtfile):   
    
    f1 = open(txtfile, 'r')
    f2 = open(txtfile + '.temp', 'w')
    
    try:
        for line in f1:
            
            if oldline in line:
#                print oldline
                # You need to include a newline if you're replacing the whole line
                line = newline              
#                print newline
                f2.write(line + "\n")
            else:
                f2.write(line)

    except:
        print ("Line substitution in file: " + txtfile + " failed!!")
        
    f1.close()
    f2.close()
    
    try:    
        sh.copyfile(txtfile + '.temp', txtfile)
    except:
        print ("KOPPIERROR")
        
    #end function
##############################################################################################################################################################################  
def change_parameters(string, parameter):     
    
    #introduce new variable for use in other function
    param = parameter
    
    #change relevant lines in control file
    fun_substitute_line(string, string + '	' + str(param), WaSiM_control_folder + '\\' + control_file )
    
    return param
    
    #end function
##############################################################################################################################################################################

#load parameter set matrix from text file, with number of rows equal to number of parameter combinations
parameter_set = np.loadtxt(parameter_set_matrix_filepath)
#reduce decimal places to max. 2
np.round(parameter_set[:,:], decimals = 2, out = parameter_set[:,:])

#copy text from each line for parameter of interest in the control file and define string variables
Ttrans = '$set $Ttrans		='
TRS = '$set $TRS			='
lwincorr = '$set $LWINcorr 		='
lwoutcorr = '$set $LWOUTcorr		='
MF = '$set $MF			='
VA_scal = '$set $VA_Scal		='

#define array with parameter names
parameter_labels = [Ttrans, TRS, lwincorr, lwoutcorr, MF, VA_scal]

#initialize run number and other loop
run_number = 0
i = 0

#create output folder and run wasim with the modified control file
for run_number in range(len(parameter_set[:, 1])): #number of simulations corresponding to number of parameter combinations

    #define name of output folder for each simulation
    output_folder_filename = 'output folder name base' + str(run_number + 1)
    #variable for output folder filepath
    output_folder_filepath = os.path.join(WaSiM_main_directory, output_folder_filename)
    
    #change default output directory in control file for each simulation
    oldline = '$set $DefaultOutputDirectory = $mainpath//'
    newline = oldline + output_folder_filename + '/'
    substitute_line(oldline, newline, WaSiM_control_folder + '\\' + control_file)
    
    #print error if output folders already exist, need delete folders function here!
    try:
        os.mkdir(output_folder_filepath)
    except OSError as error:
        print(error)
    #print runNumber+1 for easy reference in IDE   
    print('run ' + str(run_number + 1))

    #change calibration parameters in control file    
    for i in range(len(parameter_labels)): #number of parameters 
        #define variables for change_parameters function
        string = parameter_labels[i]
        parameter = (parameter_set[run_number, i])
        change_parameters((string), (parameter))
        
    #copy modified control file of each simulation into corresponding output folder
    sh.copy(control_file, output_folder_filepath)
    
    #run WaSiM executable with control file
    p = subprocess.Popen([wasim_executable, control_file])
    p.communicate()

    #delete unneeded files after each run
    for delete_file in os.listdir(output_folder_filepath):
        if not delete_file.startswith(('file start', 'file start 2', 'file start N')):
            os.unlink(os.path.join(output_folder_filepath, delete_file))
        if delete_file.startswith(('file start', 'file start 2', 'file start N')):
            os.unlink(os.path.join(output_folder_filepath, delete_file))

#end
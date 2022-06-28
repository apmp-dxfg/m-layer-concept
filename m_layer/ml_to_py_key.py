"""
Script to display name-UID tuples that can be 
copied into a python module and edited to give appropriate 
local names for the tuples. 

A sequence of JSON file names can be given on the command line.
    
"""
import json 
import sys 
import glob 
import os.path

# set as appropriate 
# root_dir = r"C:\proj_py\m-layer-concept\m_layer\json\scales"
# fmt = r"{} = Scale( ('{}', {}) )"

root_dir = r"C:\proj_py\m-layer-concept\m_layer\json\aspects"
fmt = r"{} = Aspect( ('{}', {}) )"

# One or more JSON file names (without extension)
if len(sys.argv) > 1:
    for a_i in sys.argv[1:]:

        file_path = os.path.join(
            root_dir,
            a_i + '.json'
        )
        
        with open(file_path,'r') as f:
            data = json.load(f)        
        
        for d_i in data:
            
            d = d_i['uid']
            new_name = d[0].replace('-','_')
            str_exp = fmt.format(new_name,d[0],d[1])
        
            print(str_exp)
            
        print()
else:
    file_path = os.path.join( root_dir,'*.json' )
    
    for f_json in glob.glob( file_path ):
        print(f_json)
        with open(f_json,'r') as f:
            data = json.load(f)        
        
        for d_i in data:
            
            d = d_i['uid']
            new_name = d[0].replace('-','_')
            str_exp = fmt.format(new_name,d[0],d[1])
        
            print(str_exp)
            
        print()
"""
``ml_to_py_key`` is a command line script that displays name-UID declarations which could be copied directly into a  module. 

The names can be changed to appropriate local names. 

Usage:

.. code:: text

    C:\m_layer>python ml_to_py_key.py

    C:\m_layer\json\\aspects\physical_aspects.json
    ml_mass = Aspect( ('ml-mass', 321881801928222308627062904049725548287) )
    ml_length = Aspect( ('ml-length', 993853592179723568440264076369400241) )
    ml_frequency = Aspect( ('ml-frequency', 153247472008167864427404739264717558529) )
    
    C:\m_layer\json\scales\\frequency_scales.json
    ml_si_hertz_ratio = Scale( ('ml-si-hertz-ratio', 307647520921278207356294979342476646905) )
    ml_si_terahertz_ratio = Scale( ('ml-si-terahertz-ratio', 271382954339420591832277422907953823861) )
    
    C:\m_layer\json\scales\length_scales.json
    ml_si_metre_ratio = Scale( ('ml-si-metre-ratio', 17771593641054934856197983478245767638) )
    ml_si_nanometre_ratio = Scale( ('ml-si-nanometre-ratio', 257091757625055920788370123828667027186) )
    
    ...
    
"""
import json 
import sys 
import glob 
import os.path

fmt = dict( 
    aspects=r"{} = Aspect( ('{}', {}) )",
    scales=r"{} = Scale( ('{}', {}) )"
)

if __name__ == '__main__':

    here = os.path.dirname(__file__)
    root_dir = os.path.join( here, r'json')

    # print("Root: ", root_dir)
    print()

    for sa in ('aspects','scales'):

        file_path = os.path.join( root_dir,sa,'*.json' )
        # print(file_path,'\n')
        
        for f_json in glob.glob( file_path ):
            print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)        
            
            for d_i in data:
                
                d = d_i['uid']
                new_name = d[0].replace('-','_')
                str_exp = fmt[sa].format(new_name,d[0],d[1])
            
                print(str_exp)
                
            print()
import unittest
import os
import glob
import json
import sys

from m_layer import * 

#----------------------------------------------------------------------------
# Identify the directory path on the current system
#
import m_layer
here = os.path.dirname(m_layer.__file__)
json_files = os.path.join( here, r'json')
 
#----------------------------------------------------------------------------
class TestInit(unittest.TestCase):

    """
    Tests that make sure the UUID values are all different and that 
    cross references do match with something
    """

    def _make_UUID_mapping(self,ml_type):
        self.assertTrue(os.path.isdir(json_files),msg=os.getcwd())
        
        mapping = dict() 
        type_dir = os.path.join(json_files,ml_type)
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # In each dict there should be a 'uid' element
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if UUID in mapping:
                        msg = "{} is used for {}".format(name,mapping[UUID])
                        self.fail(msg)
                    else:
                        mapping[UUID] = name 
        return mapping 
        
    def test_UUIDs(self):
        """
        In a particular aspect/scale/reference directory defined my `ml_type`,
        run through all the entries and make sure that each UUID is indeed different 
        from all the others.
        
        """
        
        aspects = self._make_UUID_mapping('aspects')                        
        # print(aspects.values())                
                                
        references = self._make_UUID_mapping('references')                        
        # print(references.values())   
        for r_i in references:
            self.assertFalse( r_i in aspects, msg = "{}, {}".format(r_i,references[r_i]) )

        # scales will refer to a reference which can be cross checked
        scales = dict() 
        type_dir = os.path.join(json_files,'scales')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # In each dict there should be a 'uid' element
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if UUID in scales:
                        msg = "{} is used for {}".format(name,scales[UUID])
                        self.fail(msg)
                    else:
                        scales[UUID] = name   

                    # Cross check
                    ref = i['reference']
                    self.assertTrue( str(ref[1]) in references, msg=ref )
           
        for s_i in scales:
            self.assertFalse( s_i in aspects, msg = "{}, {}".format(s_i,scales[s_i]) )
            self.assertFalse( s_i in references, msg = "{}, {}".format(s_i,scales[s_i]) )

        # conversion and casting can be cross checked
        type_dir = os.path.join(json_files,'conversion_casting')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'ScalesForAspect':
                        a = i['aspect']
                        self.assertTrue( str(a[1]) in aspects )
                        
                        s_lst = i['scales']
                        for s in s_lst:
                            msg = "{} in {}".format(s[0],f_json)
                            self.assertTrue( str(s[1]) in scales, msg=msg )
                            
                    elif i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[1]) in scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[1]) in scales, msg=s )
                    elif i['__entry__'] == 'Cast':
                        # aspects follow scales in the JSON files 
                        x = i['src']
                        self.assertTrue( str(x[0][1]) in scales, msg=x )
                        self.assertTrue( str(x[1][1]) in aspects, msg=x )
                        
                        x = i['dst']
                        self.assertTrue( str(x[0][1]) in scales, msg=x )
                        self.assertTrue( str(x[1][1]) in aspects, msg=x )
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)
                    
    def _make_name_mapping(self,ml_type):
        self.assertTrue(os.path.isdir(json_files),msg=os.getcwd())
        
        mapping = dict() 
        type_dir = os.path.join(json_files,ml_type)
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # In each dict there should be a 'uid' element
                # which has two components: a `name` and a UUID
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if name in mapping:
                        msg = "{} is used for {}".format(name,mapping[name])
                        self.fail(msg)
                    else:
                        mapping[name] = UUID 
        return mapping 
        
    def test_names(self):
        """
        In a particular aspect/scale/reference directory defined my `ml_type`,
        run through all the entries and make sure that each name is indeed different 
        from all the others.
        
        This is not really a strict requirement for the M-layer, but for the 
        proof of concept it is desirable to keep things tidy. 
        
        """
        
        aspects = self._make_name_mapping('aspects')                        
        # print(aspects.keys())                
                                
        references = self._make_name_mapping('references')                        
        # print(references.keys())   
        for r_i in references:
            self.assertFalse( r_i in aspects, msg = "{}, {}".format(r_i,references[r_i]) )

        # scales will refer to a reference which can be cross-checked
        scales = dict() 
        type_dir = os.path.join(json_files,'scales')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # In each dict there should be a 'uid' element
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if name in scales:
                        msg = "{} is used for {}".format(UUID,scales[name])
                        self.fail(msg)
                    else:
                        scales[name] = UUID   

                    # Cross check
                    ref = i['reference']
                    self.assertTrue( str(ref[0]) in references, msg=ref )
           
        for s_i in scales:
            self.assertFalse( s_i in aspects, msg = "{}, {}".format(s_i,scales[s_i]) )
            self.assertFalse( s_i in references, msg = "{}, {}".format(s_i,scales[s_i]) )

        # conversion and casting can be cross checked
        type_dir = os.path.join(json_files,'conversion_casting')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'ScalesForAspect':
                        a = i['aspect']
                        self.assertTrue( str(a[0]) in aspects )
                        
                        s_lst = i['scales']
                        for s in s_lst:
                            msg = "{} in {}".format(s[0],f_json)
                            self.assertTrue( str(s[0]) in scales, msg=msg )
                            
                    elif i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[0]) in scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[0]) in scales, msg=s )
                    elif i['__entry__'] == 'Cast':
                        # aspects follow scales in the JSON files 
                        x = i['src']
                        self.assertTrue( str(x[0][0]) in scales, msg=x )
                        self.assertTrue( str(x[1][0]) in aspects, msg=x )
                        
                        x = i['dst']
                        self.assertTrue( str(x[0][0]) in scales, msg=x )
                        self.assertTrue( str(x[1][0]) in aspects, msg=x )
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)        
#============================================================================
if __name__ == '__main__':
    unittest.main()
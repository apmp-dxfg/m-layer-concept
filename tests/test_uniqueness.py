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

        # conversion can be cross checked
        type_dir = os.path.join(json_files,'conversion')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                            
                    if i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[1]) in scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[1]) in scales, msg=s )

                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)


        # aspect-scales can be cross checked
        type_dir = os.path.join(json_files,'scales_for')
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
                                                    
                        s = i['src']
                        msg = "{} in {}".format(s[0],f_json)
                        self.assertTrue( str(s[1]) in scales, msg=msg )

                        d = i['dst']
                        msg = "{} in {}".format(d[0],f_json)
                        self.assertTrue( str(d[1]) in scales, msg=msg )

                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)

        # casting can be cross checked
        type_dir = os.path.join(json_files,'casting')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'Cast':
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
        In a particular aspect/scale/reference directory defined by `ml_type`,
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

        # conversion can be cross checked
        type_dir = os.path.join(json_files,'conversion')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                            
                    if i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[0]) in scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[0]) in scales, msg=s )
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)        

        # aspect-scales can be cross checked
        type_dir = os.path.join(json_files,'scales_for')
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
                        self.assertTrue( str(a[0]) in aspects,
                            msg="{!r} not found".format(a[0])
                        )
                        
                        s = i['src']
                        msg = "{} in {}".format(s[0],f_json)
                        self.assertTrue( str(s[0]) in scales, msg=msg )

                        d = i['dst']
                        msg = "{} in {}".format(d[0],f_json)
                        self.assertTrue( str(d[0]) in scales, msg=msg )
                            
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)  
                        
        # casting can be cross checked
        type_dir = os.path.join(json_files,'casting')
        self.assertTrue(os.path.isdir(type_dir))
        files = os.path.join(type_dir,r'*.json')
        # print(files)
        for f_json in glob.glob( files ):
            # print(f_json)
            with open(f_json,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'Cast':
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
 
    # def test_systematic_scale_uniqueness(self):
        # """
        # The name of a ratio scale with a reference belonging to a unit  
        # system may be a product of powers of base unit names in that system. 
        # We call such a scale "systematic". A scale name may also be special 
        # in some way (i.e., non-systematic, like "V.m-1")

        # The M-layer dimension of any non-systematic scale must map to 
        # just one systematic scale (the client may then need to cast
        # to the desired scale).
        
        # """
        # from m_layer.context import global_context as cxt 
        # from m_layer.lib import _sys_to_dimension
        # from m_layer.uid import UID
        
        # for src_scale_uid in cxt.scale_reg._objects.keys(): 
            
            # json_scale = cxt.scale_reg[src_scale_uid]  
            # ref_uid = UID( json_scale['reference'] )
            # json_ref = cxt.reference_reg[ ref_uid ]

            # if "system" in json_ref: 
            
                # json_sys = json_ref["system"]
                # dim = _sys_to_dimension( json_sys )  
                
                # if 'systematic' in json_sys:
                
                    # self.assertTrue(
                        # json_scale["scale_type"] == "ratio",
                        # msg="{}".format(src_scale_uid)
                    # )
                    # self.assertTrue( 
                        # cxt.dimension_conversion_reg[dim] == src_scale_uid,
                        # msg="{} from {}".format(src_scale_uid,dim)
                    # )
                    
                # elif json_scale["scale_type"] == "ratio":
                    # # For every name of a ratio scale with a reference belonging 
                    # # to a unit system that is not systematic, there should 
                    # # be a systematic scale entry with the same dimensions in the 
                    # # `dimension_conversion_reg`. 
                    # # This systematic scale provides a basis for casting.
                    # # This test reports any missing cases.
                    # with self.subTest(
                        # msg = "no mapping from {!r} to {!r}".format(
                            # src_scale_uid,dim
                        # )
                    # ):
                        # self.assertTrue( dim in cxt.dimension_conversion_reg )
                        
                    # with self.subTest(
                        # msg = "{} is not systematic".format(
                            # cxt.dimension_conversion_reg[dim]
                        # )
                    # ):
                        # s_uid = cxt.dimension_conversion_reg[dim]
                        # s_json = cxt.scale_reg[ s_uid ]
                        # r_uid = UID( s_json['reference'] )
                        # json_r = cxt.reference_reg[ ref_uid ]
                        # self.assertTrue( "systematic" in json_r["system"] )
                # else:
                    # pass
      
            

#============================================================================
if __name__ == '__main__':
    unittest.main()
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

    # -----------------------------------------------------------------------                
    def _make_UUID_mapping(self,ml_type):
        # `ml_type` will be 'aspects', 'scales', etc 
        
        self.assertTrue( os.path.isdir(json_files),msg=os.getcwd() )
        
        UUID_mapping = dict() 
        type_dir = os.path.join(json_files,ml_type)
        self.assertTrue( os.path.isdir(type_dir) )
        
        # Look for JSON files in type_dir and subdirectories
        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
            
                data = json.load(f)  
                
                # Expect a list of dicts 
                # In each dict there is a 'uid' element
                for i in data:
                    name = i['uid'][0]
                    UUID = str( i['uid'][1] )
                    
                    if UUID in UUID_mapping:
                        msg = "file {}, the UUID in [{},{}] is already used for {}".format( 
                            f_i,name,UUID,UUID_mapping[UUID]
                        )
                        self.fail(msg)
                    else:
                        UUID_mapping[UUID] = (name,f_i)  
                        
        return UUID_mapping 
        
    # -----------------------------------------------------------------------                
    def test_UUIDs(self):
        """
        In a particular aspects, scales, or references directory,
        make sure that each UUID is indeed different from all the others.
        
        """
        
        UUID_aspects = self._make_UUID_mapping('aspects')                        
        # print(aspects.values())                
                                
        UUID_references = self._make_UUID_mapping('references')                        
        # print(references.values()) 
        
        # No UUIDS in common between aspects and references
        for r_i in UUID_references:
            self.assertFalse( 
                r_i in UUID_aspects, 
                msg = "{}, {}".format(r_i,UUID_references[r_i]
            ) 
        )

        UUID_scales = dict() 
        type_dir = os.path.join(json_files,'scales')
        self.assertTrue(os.path.isdir(type_dir))

        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # In each dict has a 'uid' element
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if UUID in UUID_scales:
                        msg = "file {}, the UUID in [{},{}] is already used for {}".format( 
                            f_i,name,UUID,UUID_mapping[UUID]
                        )
                        msg = "{} is used for {}".format(name,UUID_scales[UUID])
                        self.fail(msg)
                    else:
                        UUID_scales[UUID] = (name,f_i)     

                    # scales refer to a reference which can be cross checked here
                    ref = i['reference']
                    self.assertTrue( str(ref[1]) in UUID_references, msg=ref )
        
        # Check the uniqueness of UUIDs against aspects and references
        for s_i in UUID_scales:
            self.assertFalse( s_i in UUID_aspects, msg = "{}, {}".format(s_i,UUID_scales[s_i]) )
            self.assertFalse( s_i in UUID_references, msg = "{}, {}".format(s_i,UUID_scales[s_i]) )

        # ------------------------------------------------------------------
        # scale conversion can be cross checked
        type_dir = os.path.join(json_files,'conversion')
        self.assertTrue(os.path.isdir(type_dir))
        
        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)

            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                            
                    if i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[1]) in UUID_scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[1]) in UUID_scales, msg=s )

                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)


        # ------------------------------------------------------------------
        # aspect-scales can be cross checked
        type_dir = os.path.join(json_files,'scales_for')
        self.assertTrue(os.path.isdir(type_dir))

        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)

            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'ScalesForAspect':
                        a = i['aspect']
                        self.assertTrue( 
                            str(a[1]) in UUID_aspects, 
                            msg="{!r} not fount in aspects".format(a[1]) 
                        )
                                                    
                        s = i['src']
                        msg = "{} in {}".format(s[0],f_json)
                        self.assertTrue( str(s[1]) in UUID_scales, msg=msg )

                        d = i['dst']
                        msg = "{} in {}".format(d[0],f_json)
                        self.assertTrue( str(d[1]) in UUID_scales, msg=msg )

                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)

        # ------------------------------------------------------------------
        # casting can be cross checked
        type_dir = os.path.join(json_files,'casting')
        self.assertTrue(os.path.isdir(type_dir))

        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)

            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                for i in data:
                    if i['__entry__'] == 'Cast':
                        # aspects follow scales in the JSON files 
                        x = i['src']
                        self.assertTrue( str(x[0][1]) in UUID_scales, msg=x )
                        self.assertTrue( str(x[1][1]) in UUID_aspects, msg=x )
                        
                        x = i['dst']
                        self.assertTrue( str(x[0][1]) in UUID_scales, msg=x )
                        self.assertTrue( str(x[1][1]) in UUID_aspects, msg=x )
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)
                    
    # -----------------------------------------------------------------------                
    def _make_name_mapping(self,ml_type):
        self.assertTrue(os.path.isdir(json_files),msg=os.getcwd())
        
        name_mapping = dict() 
        type_dir = os.path.join(json_files,ml_type)
        self.assertTrue(os.path.isdir(type_dir))
        
        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                # Expect a list of dicts 
                # Each dict should has a 'uid' element
                # which has two components: a `name` and a UUID
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    if name in name_mapping:
                        msg = "file {},\nthe name in [{},{}] is already used for\n{}".format( 
                            f_i,name,UUID,name_mapping[name]
                        )
                        self.fail(msg)
                    else:
                        name_mapping[name] = (UUID, f_i)
                        
        return name_mapping 
        
    # -----------------------------------------------------------------------                
    def test_names(self):
        """
        In the aspect, scales, and references directories,
        make sure that each name is different from all the others.
        
        This is not really a strict requirement for the M-layer, but for the 
        proof of concept it is desirable to keep things tidy. 
        
        """
        
        named_aspects = self._make_name_mapping('aspects')                        
        # print(named_aspects.keys())                
                                
        named_references = self._make_name_mapping('references')                        
        # print(named_references.keys())   
        
        # Check that reference and aspect names are different
        for r_i in named_references:
            self.assertFalse( 
                r_i in named_aspects, 
                msg = "repeated:{}, {}".format(r_i,named_references[r_i]) 
            )

        named_scales = dict() 
        type_dir = os.path.join(json_files,'scales')
        self.assertTrue( os.path.isdir(type_dir) )
        
        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
            
                data = json.load(f)  
                # Expect a list of dicts 
                # Each dict has a 'uid' element
                # take the name from there
                for i in data:
                    name = i['uid'][0]
                    UUID = str(i['uid'][1])
                    
                    # Is the scale name a duplicate?
                    if name in named_scales:
                        msg = "file {}, [{},{}] is used for {}".format(f_i,name,UUID,named_scales[name])
                        self.fail(msg)
                    else:
                        named_scales[name] = (UUID,f_i)   

                    # scales refer to a reference. This can be cross-checked
                    ref_name = str(i['reference'][0])
                    self.assertTrue( 
                        ref_name in named_references, 
                        msg="{} is not a registered reference".format(i['reference']) 
                    )
           
        # Check that names are different from aspects and references
        for s_i in named_scales:
            self.assertFalse( 
                s_i in named_aspects, 
                msg = "{}, {}".format(s_i,named_scales[s_i]) 
            )
            self.assertFalse(   
                s_i in named_references, 
                msg = "{}, {}".format(s_i,named_scales[s_i]) 
            )

        # ------------------------------------------------------------------
        # conversion can be cross checked
        type_dir = os.path.join(json_files,'conversion')
        self.assertTrue(os.path.isdir(type_dir))

        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)

            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  
                for i in data:
                            
                    if i['__entry__'] == 'Conversion':
                        s = i['src']
                        self.assertTrue( str(s[0]) in named_scales, msg=s )
                        s = i['dst']
                        self.assertTrue( str(s[0]) in named_scales, msg=s )
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)        

        # ------------------------------------------------------------------
        # aspect-scales can be cross checked
        type_dir = os.path.join(json_files,'scales_for')
        self.assertTrue(os.path.isdir(type_dir))
        
        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  

                for i in data:
                    if i['__entry__'] == 'ScalesForAspect':
                        a = i['aspect']
                        self.assertTrue( str(a[0]) in named_aspects,
                            msg="{!r} not found".format(a[0])
                        )
                        
                        s = i['src']
                        msg = "{} in {}".format(s[0],f_json)
                        self.assertTrue( str(s[0]) in named_scales, msg=msg )

                        d = i['dst']
                        msg = "{} in {}".format(d[0],f_json)
                        self.assertTrue( str(d[0]) in named_scales, msg=msg )
                            
                    else:
                        msg = "unknown type: {} in {}".format(i['__entry__'],f_json)
                        self.fail(msg)  
                        
        # ------------------------------------------------------------------
        # casting can be cross checked
        type_dir = os.path.join(json_files,'casting')
        self.assertTrue(os.path.isdir(type_dir))

        for f_json in glob.glob( '**/*.json',root_dir=type_dir,recursive=True ):
            # print(f_json)
            f_i = os.path.join(type_dir,f_json)
            with open(f_i,'r') as f:
                data = json.load(f)  

                for i in data:
                    if i['__entry__'] == 'Cast':
                        x = i['src']
                        self.assertTrue( str(x[0][0]) in named_scales, msg=x )
                        self.assertTrue( str(x[1][0]) in named_aspects, msg=x )
                        
                        x = i['dst']
                        self.assertTrue( str(x[0][0]) in named_scales, msg=x )
                        self.assertTrue( str(x[1][0]) in named_aspects, msg=x )
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
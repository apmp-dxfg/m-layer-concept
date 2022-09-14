import unittest
import os
import glob
import json
import sys

from m_layer import * 
from m_layer.context import global_context as cxt 

# The set elements are tuples of allowed (src,dst) scale types
conversion_rules = {
    ('ratio','ratio'),
    ('interval','interval'),
    ('bounded','bounded'),
    ('ordinal','ordinal'),
    ('nominal','nominal'),    
    ('bounded','ratio'),
    ('interval','ratio'),
    ('ordinal','ratio'),
    ('nominal','ratio'),
    ('ordinal','interval'),
    ('nominal','interval'),   
    ('nominal','ordinal'),
}

#----------------------------------------------------------------------------
class TestConversion(unittest.TestCase):

    """
    Tests that make sure registered conversions obey rules 
    associated with scale-type:

        i) conversion that does not change the type, or 
        ii) conversion to a scale type which has all the invariant 
            properties of the source scale type.
    """
        
    def test_conversions(self):
        """
        The rules associated with scale-type:

        i) conversion that does not change the type, or 
        ii) conversion to a scale type which has all the invariant 
            properties of the source scale type.  
            
        """
        # i) Step through all registered conversions 
        # ii) Find the src and dst scales 
        # iii) check that any changes of scale type are legal 
        
        for uid_pair in cxt.conversion_reg._table.keys():
            src_scale_uid, dst_scale_uid = uid_pair

        # The M-Layer reference identifies the type of scale
        _scales = cxt.scale_reg
        src_type = _scales[ src_scale_uid ]['scale_type']
        dst_type = _scales[ dst_scale_uid ]['scale_type']
        
        self.assertTrue( (src_type,dst_type) in conversion_rules )
            


#============================================================================
if __name__ == '__main__':
    unittest.main()
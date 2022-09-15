import unittest

from m_layer import * 
from m_layer.context import global_context as cxt 

# The set elements are tuples of allowed (src,dst) scale types
# 
conversion_rules = {
    # No change 
    ('ratio','ratio'),
    ('interval','interval'),
    ('bounded','bounded'),
    ('ordinal','ordinal'),
    ('nominal','nominal'), 
    # Promotion to the ratio scale
    ('bounded','ratio'),
    ('interval','ratio'),
    ('ordinal','ratio'),
    ('nominal','ratio'),
    # Promotion to the interval scale 
    ('ordinal','interval'),
    ('nominal','interval'),  
    # Promotion to the ordinal scale
    ('nominal','ordinal'),
}

#----------------------------------------------------------------------------
class TestConversion(unittest.TestCase):

    """
    Make sure registered conversions obey rules
    """
        
    def test_conversions(self):
        """
        i) Step through all registered conversions 
        ii) Find the src and dst scales 
        iii) check that any changes of scale type are legal 
            
        """      
        for uid_pair in cxt.conversion_reg._table.keys():
            src_scale_uid, dst_scale_uid = uid_pair

        src_type = cxt.scale_reg[ src_scale_uid ]['scale_type']
        dst_type = cxt.scale_reg[ dst_scale_uid ]['scale_type']
        
        self.assertTrue( (src_type,dst_type) in conversion_rules )

#============================================================================
if __name__ == '__main__':
    unittest.main()
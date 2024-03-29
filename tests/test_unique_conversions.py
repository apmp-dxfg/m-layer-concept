import unittest
import os
import glob
import json
import sys

from m_layer import * 
from m_layer.context import global_context as cxt

#----------------------------------------------------------------------------
class TestUniqueConversion(unittest.TestCase):

    """
        There are rules about the structure of conversion tables:
          1) conversions that do not change the scale type do not need aspect 
          2) conversion between ratio and interval scales may be 
            allowed if the aspect is declared
          3) conversion between the same type of scale may be restricted 
            to a certain aspect

        We must check that instances of 1) do not overshadow 3)      
    """
    
    # Note, the implementation in Context has been modified so that 
    # it will be possible for aspect-specific and aspect-free conversion
    # definitions to coexist, with aspect-specific ones given precedence.
    # This probably isn't a good idea, so the test case will flag it as 
    # an error. However, we may wish to revisit that policy down the track.
    
    def test_unique_conversion(self):
        
        # A table of conversions indexed by a pair of scale IDs
        conversions = cxt.conversion_reg._table
        
        # for scale_pair in conversions.keys(): print( scale_pair )
        # print()
        
        # A mapping from aspect ID to a table of conversions 
        # indexed by a pair of scale IDs
        aspect_conversions = cxt.scales_for_aspect_reg._table        
        aspect_keys = list(aspect_conversions.keys())
        
        # For each table that is restricted to a certain aspect 
        # check that the same pair of scales is not in the 
        # aspect-free conversion table
        for a_i in aspect_keys: 
            # print( a_i )
            
            _conversions = aspect_conversions[a_i]
            
            for scale_pair in _conversions.keys(): 
                self.assertTrue( scale_pair in _conversions )
                self.assertFalse( scale_pair in conversions ) 
                
                # print( scale_pair )
            # print()
            
        # print()


#============================================================================
if __name__ == '__main__':
    unittest.main()
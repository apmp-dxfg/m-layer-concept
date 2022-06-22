# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import json

"""
"""
# Numerical terms in JSON strings are converted to numbers using `eval()`. 
import math

from m_layer import si_constants as si 
from m_layer.conversion_register import _set_conversion_fn

# ---------------------------------------------------------------------------
class ScalesForAspectRegister(object):
    """
    """
    
    def __init__(self,context):
        self._context = context 
        
        # Table indexed by aspect with entries that are 
        # mapping scale-pairs to conversion functions
        # (same format as conversion_register entries)
        
        self._table = {}
 
    # These mapping methods just act on the aspect table
    def __contains__(self,aspect):
        return aspect in self._table 

    def __getitem__(self,aspect):
        return self._table[ aspect ]
 
    def get(self,aspect,default):
        return self._table.get( aspect, default )

    # This method goes down to the second level 
    def get_fn(self,aspect,scale_uid_pair,default=None):
        """
        Return a conversion function 
        """        
        return self._table.get( aspect, {} ).get( scale_uid_pair, default ) 
                
    def set(self,entry):
        # keys: aspect, src, dst, factors
        uid_aspect = tuple( entry['aspect'] )

        if uid_aspect not in self._table:
            self._table[uid_aspect] = {}
                    
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        scale_uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        _set_conversion_fn(self,entry,self._table[uid_aspect],scale_uid_pair)
       
            
        
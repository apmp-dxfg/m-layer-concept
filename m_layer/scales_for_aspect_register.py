# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import json

"""
Declared conversions must be enabled for each aspect.
This register holds a sequence of M-layer scales for each aspect. 
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
        # Table indexed by aspect to entries that are 
        # mapped by scale-pairs to a conversion function
        # (same format as conversion_register entries)
        
        self._table = {}
                
        
    def set(self,entry):
        # keys: aspect, src, dst, factors
        uid = tuple( entry['aspect'] )

        if uid not in self._table:
            self._table[uid] = {}
                    
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        _set_conversion_fn(self,entry,self._table[uid],uid_pair)
       
            
        
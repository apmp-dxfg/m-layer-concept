# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import json

# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math, we can include defined constants, like math.pi.
import math

# ---------------------------------------------------------------------------
class CastingRegister(object):
    
    """
    A `CastingRegister` holds a mapping of scale pairs 
    to information about how to convert between scales. 
    Casting involves a change in the type of scalee.
    """
    
    def __init__(self,context):
        self._context = context 
        self._table = {}
                
    def __contains__(self,item):
        return item in self._table 
        
    def __getitem__(self,uid_pair):
        return self._table[ uid_pair ]
        
    def get(self,uid_pair,default=None):
        """
        Return a conversion function 
        """
        # `uid` may be a list from json
        return self._table.get( uid_pair, default ) 
        
    # Extract a uid pair for the entry and then a function
    # to cast from one M-layer reference to the other.
    def set(self,entry):
        """
        Create an entry for a conversion function
        The type of the source and destination scales
        determines the form of the conversion function
        and the function parameters are elements in `entry`.
        
        """
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        if uid_pair in self._table:
            raise RuntimeError(
                "existing casting entry: {}".format(uid_pair)
            )
        else:
            # The M-Layer reference identifies the type of scale
            _scales = self._context.scale_reg
            src_type = _scales[uid_ml_ref_src]['scale_type']
            dst_type = _scales[uid_ml_ref_dst]['scale_type']
                                      
        # Casting function parameter values are in a sequence 
        # they are stored as strings to allow fractions 
        factors = tuple(  eval(x_i) for x_i in entry['factors'] )
        
        # Set the conversion function
        if (
            (src_type,dst_type) == ('interval-scale','ratio-scale')  
        or  (src_type,dst_type) == ('ratio-scale','interval-scale') 
        ):
            # `factors[0]` is the scale divisions conversion factor 
            # `factors[1]` is the offset
            self._table[uid_pair] = lambda x: factors[0]*x + factors[1]
        else:
            raise RuntimeError(
                "unrecognised case: {}".format((src_type,dst_type))
            )

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import json

# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math, we can include defined constants, like math.pi.
import math

# ---------------------------------------------------------------------------
class ConversionRegister(object):
    
    """
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
        """
        # `uid` may be a list from json
        return self._table.get( uid_pair, default) 
        
    # Extract a uid pair for the entry and then a conversion function
    # from one M-layer reference to the other.
    def set(self,entry):
        """
        """
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        if uid_pair in self._table:
            raise RuntimeError(
                "existing conversion entry: {}".format(uid_pair)
            )
        else:
            # The M-layer reference identifies the type of scale
            _scales = self._context.scale_reg
            src_type = _scales[uid_ml_ref_src]['scale_type']
            dst_type = _scales[uid_ml_ref_dst]['scale_type']
                                      
        # Conversion function parameter values are in a sequence 
        # they are stored as strings to allow fractions 
        factors = tuple(  eval(x_i) for x_i in entry['factors'] )
        
        # Set the conversion function
        if (src_type,dst_type) == ('ratio-scale','ratio-scale'):
            self._table[uid_pair] = lambda x: factors[0]*x 
        elif (
            (src_type,dst_type) == ('interval-scale','interval-scale') or 
            (src_type,dst_type) == ('ratio-scale','interval-scale') or
            (src_type,dst_type) == ('interval-scale','ratio-scale')
        ):
            # `factors[0]` is the scale divisions conversion factor 
            # `factors[1]` is the offset
            self._table[uid_pair] = lambda x: factors[0]*x + factors[1]
        elif (
            (src_type,dst_type) == ('bounded-interval-scale','bounded-interval-scale')
        ):
            # `factors[0]` is the scale divisions conversion factor 
            # `factors[1]` is the lower bound of the dst scale 
            # `factors[2]` is the range of values in the dst scale
            self._table[uid_pair] = lambda x: \
                (factors[0]*x - + factors[1]) % factors[2] + factors[1]
        else:
            raise RuntimeError(
                "unrecognised case: {}".format((src_type,dst_type))
            )

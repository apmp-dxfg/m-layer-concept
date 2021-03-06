"""
Conversion changes the scale of an expression but leaves the type of scale and aspect unchanged. 

Legitimate conversions are recorded in a :class:`~.conversion_register.ConversionRegister`, which is an attribute of the :class:`~context.Context` object.

"""
import json

# Numerical terms in JSON strings are converted to numbers using `eval()`. 
import math
from m_layer import si_constants as si 

# ---------------------------------------------------------------------------
def _set_conversion_fn(self,entry,_tbl, uid_pair):
    """
    Utility function to take one JSON entry for conversion between scales 
    and enter it into a mapping, indexed by the pair of ML scale uids
    
    """

    if uid_pair in _tbl:
        raise RuntimeError(
            "existing conversion entry: {}".format(uid_pair)
        )
        
    # The M-Layer reference identifies the type of scale
    _scales = self._context.scale_reg
    src_type = _scales[ uid_pair[0] ]['scale_type']
    dst_type = _scales[ uid_pair[1] ]['scale_type']

    if src_type != dst_type:
        raise RuntimeError(
            "scale types must be the same: {} and {}".format(
            src_type,dst_type)
        )
                              
    # Conversion function parameter values are in a sequence 
    # they are stored as strings to allow fractions 
    factors = tuple(  eval(x_i) for x_i in entry['factors'] )
    
    # Set the conversion function
    if (src_type,dst_type) == ('ratio','ratio'):
        _tbl[uid_pair] = lambda x: factors[0]*x 
    elif (
        (src_type,dst_type) == ('interval','interval')  
    ):
        # `factors[0]` is the scale divisions conversion factor 
        # `factors[1]` is the offset
        _tbl[uid_pair] = lambda x: factors[0]*x + factors[1]
    elif (
        (src_type,dst_type) == ('bounded','bounded')
    ):
        # `factors[0]` is the scale divisions conversion factor 
        # `factors[1]` is the lower bound of the dst scale 
        # `factors[2]` is the range of values in the dst scale
        _tbl[uid_pair] = lambda x: \
            (factors[0]*x - + factors[1]) % factors[2] + factors[1]
    else:
        raise RuntimeError(
            "unrecognised case: {}".format((src_type,dst_type))
        )
 
# ---------------------------------------------------------------------------
class ConversionRegister(object):
    
    """
    A ``ConversionRegister`` maps scale pairs 
    to a function that will convert tokens between scales. 
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
        
        Args:
            uid_pair: a pair of M-layer scale uids
            
        """
        # `uid` may be a list from json
        
        return self._table.get( uid_pair, default ) 
        
    # Extract a uid pair for the entry and then a conversion function
    # from one M-layer reference to the other.
    def set(self,entry):
        """
        Create an entry for a conversion function
        The type of the source and destination scales
        determines the form of the conversion function
        and the function parameters are elements in `entry`.
        
        Args:
            entry: the M-layer record for a conversion
        
        """
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        
        _set_conversion_fn(self,entry,self._table,uid_pair)

            
"""
Conversions can be declared for specific aspects. The 
:class:`~scales_for_aspect_register.ScalesForAspectRegister` is used to hold 
these records.

"""
import json

from m_layer.ml_eval import ml_eval 

# from m_layer.conversion_register import _set_conversion_fn
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

    # if src_type != dst_type:
        # raise RuntimeError(
            # "scale types must be the same: {} and {}".format(
            # src_type,dst_type)
        # )
                              
    # Conversion function parameter values are in a sequence 
    # they are stored as strings to allow fractions 
    factors = tuple(  ml_eval(x_i) for x_i in entry['factors'] )
    
    # Set the conversion function
    if (src_type,dst_type) == ('ratio','ratio'):
        _tbl[uid_pair] = lambda x: factors[0]*x 
    elif (
        (src_type,dst_type) == ('interval','interval') 
    or  (src_type,dst_type) == ('ratio','interval')
    or  (src_type,dst_type) == ('interval','ratio')
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
            (factors[0]*x - factors[1]) % factors[2] + factors[1]
    elif (
        (src_type,dst_type) == ('bounded','ratio')
    ):
        # This is just removal of the cyclic bounds 
        # `factors[0]`  is the scale divisions conversion factor 
        _tbl[uid_pair] = lambda x: factors[0]*x
    else:
        raise RuntimeError(
            "unrecognised case: {}".format((src_type,dst_type))
        )
 
# ---------------------------------------------------------------------------
class ScalesForAspectRegister(object):

    """
    A ``ScalesForAspectRegister`` maps an aspect to a mapping 
    of scale pairs, which, in turn, index conversion functions. 
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
        """
        Return a mapping of scale-pairs to conversion functions
        (same format as conversion_register entries)
        
        Args:
            aspect (:class:`~aspect.Aspect`)
            
        """
        return self._table.get( aspect, default )

    # This method goes down to the second level 
    def get_fn(self,aspect,scale_uid_pair,default=None):
        """
        Return a conversion function 
        
        Args:
            aspect (:class:`~aspect.Aspect`)
            scale_uid_pair: a pair of M-layer scale uids
            
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
       
            
        
"""
Conversions can be declared for specific aspects. The 
:class:`~scales_for_aspect_register.ScalesForAspectRegister` is used to hold 
these records.

"""
from m_layer.ml_eval import ml_eval 
from m_layer.uid import UID

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
            aspect (:class:`~lib.Aspect`)
            
        """
        return self._table.get( aspect, default )

    # This method goes down to the second level 
    def get_fn(self,aspect,scale_uid_pair,default=None):
        """
        Return a conversion function 
        
        Args:
            aspect (:class:`~lib.Aspect`)
            scale_uid_pair: a pair of M-layer scale uids
            
        """        
        return self._table.get( aspect, {} ).get( scale_uid_pair, default ) 
                
    def set(self,entry):
        # keys: aspect, src, dst, factors
        uid_aspect = UID( entry['aspect'] )

        if uid_aspect not in self._table:
            self._table[uid_aspect] = {}
                    
        uid_ml_ref_src = UID( entry['src'] )        
        uid_ml_ref_dst = UID( entry['dst'] )
            
        scale_uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        self._set_conversion_fn(
            entry,
            self._table[uid_aspect],
            scale_uid_pair
        )
       
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

        # Parameter values are stored as strings in a dictionary
        # E.g., { "a": "1", "b": "+273.15" }
        # They may take the form of arithmetic expressions
        # E.g., { "c": "si.h*si.c/si.e/si.nano" }
        parameters_dict = { 
            k : ml_eval(v) 
                for (k,v) in entry['parameters'].items() 
        }
                
        # Set the casting function
        _tbl[uid_pair] = ml_eval(entry['function'],parameters_dict)
                                   
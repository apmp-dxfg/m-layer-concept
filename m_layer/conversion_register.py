"""
Conversion changes the scale of an expression but leaves the type of scale and aspect unchanged. 

Legitimate conversions are recorded in a :class:`ConversionRegister`

"""
from m_layer.ml_eval import ml_eval

from m_layer import ml_math        
from m_layer.uid import UID
 
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
        uid_ml_ref_src = UID( entry['src'] )        
        uid_ml_ref_dst = UID( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        
        self._set_conversion_fn(entry,self._table,uid_pair)

    # ---------------------------------------------------------------------------
    def _set_conversion_fn(self,entry,_tbl, uid_pair):
        """
        
        """
        if uid_pair in _tbl:
            raise RuntimeError(
                "existing conversion entry: {}".format(uid_pair)
            )

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
        self._table[uid_pair] = ml_eval(entry['function'],parameters_dict)
 
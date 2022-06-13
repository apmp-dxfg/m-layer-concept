# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import json

# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math, we can include defined constants, like math.pi.
import math

# e = 1.602176634E-19 coulomb
# c = 2.99792458E8 meter per second
# h = 6.62607015E-34 joule second

# ---------------------------------------------------------------------------
class CastingRegister(object):
    
    """
    A `CastingRegister` holds a mapping of aspect-scale pairs 
    to information about how to cast between expressions. 
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
        Create an entry for a casting function
        The aspect and type of the source and destination scales
        are used to identify the function
        
        """
        # TODO: aspect-scale required for src & dst 
        # This function needs finishing !
        
        uid_ml_ref_src = tuple( entry['src'] )        
        uid_ml_ref_dst = tuple( entry['dst'] )
            
        uid_pair = (uid_ml_ref_src,uid_ml_ref_dst)
        if uid_pair in self._table:
            raise RuntimeError(
                "existing cast entry: {}".format(uid_pair)
            )
        else:
            # The M-Layer reference identifies the type of scale
            _scales = self._context.scale_reg
            src_type = _scales[uid_ml_ref_src]['scale_type']
            dst_type = _scales[uid_ml_ref_dst]['scale_type']
                                      
        # Parameter values are stored as strings in a dictionary
        parameters_dict = entry['parameters'] 
        
        # Safe mode, but too restrictive
        fn = eval(entry['function'],{"__builtins__": None},parameters_dict)
        
        # Set the casting function
        if (
            (src_type,dst_type) == ('interval-scale','ratio-scale')  
        or  (src_type,dst_type) == ('ratio-scale','interval-scale') 
        ):
            self._table[uid_pair] = eval(entry['function'],parameters_dict)
        else:
            raise RuntimeError(
                "unrecognised case: {}".format((src_type,dst_type))
            )

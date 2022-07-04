"""
Casting can change the scale and aspect of an expression. 

Legitimate castings are recorded in a :class:`~.casting_register.CastingRegister`, which is an attribute of the :class:`~context.Context` object.

"""
import json

# Terms in JSON strings for numerical factors are converted to numbers using 
# `eval()`. By importing math, we can include defined constants, like math.pi.

import math

from m_layer import si_constants as si 

# ---------------------------------------------------------------------------
def _to_tuple(lst):
    """
    Convert nested lists to nested tuples
    """
    return tuple(
        _to_tuple(i) if isinstance(i, list) else i for i in lst
    )
    
# ---------------------------------------------------------------------------
class CastingRegister(object):
    
    """
    A ``CastingRegister`` maps scale-aspect pairs 
    to a function that will convert tokens between expressions
    in different scale-aspects. 
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
            uid_pair: a pair of M-layer scale-aspect uids
            
        """
        return self._table.get( uid_pair, default ) 
        
    # Extract an scale-aspect pair for the entry and then a function
    # to cast from one value to the another for the expression.
    def set(self,entry):
        """
        Create an entry for a casting function
        
        Args:
            entry: the M-layer record for a casting
        
        """
        uid_src = _to_tuple( entry['src'] )        
        uid_dst = _to_tuple( entry['dst'] )
            
        uid_pair = (uid_src,uid_dst)

        if uid_pair in self._table:
            raise RuntimeError(
                "existing cast entry: {}".format(uid_pair)
            )            
                                       
        # Parameter values are stored as strings in a dictionary
        parameters_dict = { 
            k : eval(v) 
                for (k,v) in entry['parameters'].items() 
        }
                
        # Set the casting function
        self._table[uid_pair] = eval(entry['function'],parameters_dict)

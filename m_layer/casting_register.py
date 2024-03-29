"""
Casting can change the type of scale and aspect of an expression. 

Legitimate castings are recorded in a :class:`~.casting_register.CastingRegister`.

"""
from m_layer.ml_eval import ml_eval   
from m_layer.uid import UID
    
# ---------------------------------------------------------------------------
class CastingRegister(object):
    
    """
    A ``CastingRegister`` maps scale-aspect pairs 
    to a function that will convert tokens. 
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
        # The JSON format is an array containing a 
        # pair of uids (also arrays).
        # _to_tuple = lambda l: tuple(
            # _to_tuple(i) if isinstance(i, list) else i 
                # for i in l
        # )
        _to_tuple = lambda lst: tuple( UID(i) for i in lst )
        
        uid_src = _to_tuple( entry['src'] )        
        uid_dst = _to_tuple( entry['dst'] )
            
        uid_pair = (uid_src,uid_dst)

        if uid_pair in self._table:
            raise RuntimeError(
                "existing cast entry: {}".format(uid_pair)
            )            
                                       
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

"""
Casting can change the type of scale and aspect of an expression. 

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
        
    def __getitem__(self,dim_sa):
        return self._table[ dim_sa ]
        
    def get(self,dim_sa,default=None):
        """
        Return a conversion function 
        
        Args:
            dim_sa: a dimension and a scale-aspect uid
            
        """
        return self._table.get( dim_sa, default ) 
        
    # Extract an scale-aspect pair for the entry and then a function
    # to cast from one value to the another for the expression.
    def set(self,k_i,v_i):
        """
        Create an entry for a casting function
                
        """
        self._table[k_i] = v_i

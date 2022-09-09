"""
Casting can change the type of scale and aspect of an expression. 

"""

# ---------------------------------------------------------------------------
class DimensionRegister(object):
    
    """
    """
    
    def __init__(self,context):
        self._context = context 
        self._table = {}
                
    def __contains__(self,item):
        return item in self._table 
        
    def __getitem__(self,dim_sa):
        return self._table[ dim_sa ]
        
    def get(self,key,default=None):
        """
            
        """
        return self._table.get( dim_sa, default ) 
        
    # Extract an scale-aspect pair for the entry and then a function
    # to cast from one value to the another for the expression.
    def set(self,k_i,v_i):
        """
        Create an entry for a casting function
                
        """

        if k_i in self._table:
            raise RuntimeError(
                "existing register entry: {} = {}".format(k_i,v_i)
            )
        else:
            self._table[k_i] = v_i

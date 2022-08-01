"""
"""
__all__ = (
    'Stack',
)


# ---------------------------------------------------------------------------
class Stack(object):

    """
    """
    
    # Contains two lists: one of object references
    # the other of applied operations
    
    def __init__(self,obj):
        self._obj = [obj]
        self._opn = []
  
    def copy(self):
        return Stack(
            list( self._obj ),
            list( self._opn )
        )
     
    def rmul(self,x):       
        opn = 'rmul'
        if isinstance(x,Stack):
            return self._extend(x,opn)
        else:   
            return self._append(x,opn)
        
    # These operations can be called with a Stack
    # argument or a single object
    # When a stack is passed, this object should 
    # be extended with the stack contents 
    
    def _extend(self,stack,opn):
        rtn = self + stack
        return Stack(
            rtn._obj,
            rtn._opn + [opn]
        )

    def _append(self,obj,opn):
        return Stack(
            self._obj + [obj],
            self._opn + [opn]
        )
    
    def mul(self,y):
        opn = 'mul'
        if isinstance(y,Stack):
            return self._extend(y,opn)
        else:   
            return self._append(y,opn)
 
    def div(self,y):
        opn = 'div'
        if isinstance(y,Stack):
            return self._extend(y,opn)
        else:   
            return self._append(y,opn)
            
    def pow(self,y):
        opn = 'pow'
        if isinstance(y,Stack):
            return self._extend(y,opn)
        else:   
            return self._append(y,opn)
 
    def __len__(self):
        return len(self._obj)
        
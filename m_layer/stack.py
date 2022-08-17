"""
"""

__all__ = (
    'Stack',
)

# ---------------------------------------------------------------------------
stack = list    # Alias

# ---------------------------------------------------------------------------
class Stack(object):

    """
    A Stack holds numbers and tokens for simple arithmetic operations.
    Operations like `mul, `div`, etc., return a new Stack object.
    
    """
    
    def __init__(self,obj=stack()):  
        if isinstance(obj,stack):
            self._obj = obj
        else:
            assert False
              
    def copy(self):
        return Stack( self._obj.copy() )

    def _render_str(self):

        stk = []
        
        for o_i in self._obj:
        
            # Stack objects unless they are recognised operations
            if o_i not in ('mul','div','rmul','pow'):
                stk.append( o_i )
                
            else:
                if o_i == 'mul':
                    x,y = stk.pop(), stk.pop()
                    stk.append( "{!s}.{!s}".format( y,x ) )
                                    
                elif o_i == 'rmul':
                    # `x` must be an integer
                    x,y = stk.pop(), stk.pop()
                    stk.append( "{:d}.{!s}".format( x,y ) )
                                    
                elif o_i == 'div':
                    x,y = stk.pop(), stk.pop()
                    # Numerator brackets could be added
                    stk.append( "{!s}/({!s})".format( y,x ) )
                                    
                elif o_i == 'pow':
                    # `x` must be an integer
                    x,y = stk.pop(), stk.pop()
                    # Brackets around the term `y` could be added
                    stk.append( "{!s}^{:d}".format( y,x ) )
                    
                else:
                    raise RuntimeError(opn)
        
        assert len(stk) == 1,\
            "residual stack elements: {!r}".format(stk)
        
        return stk.pop() 

    def __len__(self):
        return len(self._obj)
        
    def __getitem__(self,i):
        return self._obj[i]
        
    def __str__(self):
        return self._render_str()
        
    def __repr__(self):
        return "Stack({!r})".format(self._obj)

    def _append(self,obj):
        return Stack(self._obj + stack(obj))
        
    def push(self,x):
        """
        Args:
            x (:class:`Stack` or single object):
            
        When a :class:`Stack` is received the contents 
        are used to extend the current stack. 
        
        """
        if isinstance(x,Stack):
            return self._append( x._obj )
        elif hasattr(x,'stack'):
            return self._append( x.stack._obj )
        else:
            return self._append([x])
        
    def rmul(self):       
        return self._append(['rmul'])
        
    def mul(self):
        return self._append(['mul'])
 
    def div(self):
        return self._append(['div'])
            
    def pow(self):
        return self._append(['pow'])
 
  
# ===========================================================================
if __name__ == '__main__':

    s = Stack().push("l")
    s2 = Stack().push("km").push(100).rmul()
    s = s.push(s2).div()
    print(s)
    print(repr(s))
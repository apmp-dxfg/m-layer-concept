"""
"""
stack = list    # Alias

__all__ = (
    'Stack',
)

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
        """
        
        """
        exec_stack = []
        
        _N = len(self._obj)
        _base = 0
        
        while _base < _N:
            # Push objects to the execution stack unless they 
            # are recognised operations
            if self._obj[_base] not in ('mul','div','rmul','pow'): 
                exec_stack.append( self._obj[_base] )
                _base += 1
                
            else:
                opn = self._obj[_base]
                _base += 1
                
                if opn == 'mul':
                    x = exec_stack.pop()
                    y = exec_stack.pop()
                    exec_stack.append( "{!s}.{!s}".format( y,x ) )
                                    
                elif opn == 'rmul':
                    # `x` must be an integer
                    x = exec_stack.pop()
                    y = exec_stack.pop()
                    exec_stack.append( "{:d}.{!s}".format( x,y ) )
                                    
                elif opn == 'div':
                    x = exec_stack.pop()
                    y = exec_stack.pop()
                    # Numerator brackets could be added
                    exec_stack.append( "{!s}/({!s})".format( y,x ) )
                                    
                elif opn == 'pow':
                    # `y` must be an integer
                    x = exec_stack.pop()
                    y = exec_stack.pop()
                    # Brackets around the term `y` could be added
                    exec_stack.append( "{!s}^{:d}".format( y,x ) )
                    
                else:
                    raise RuntimeError(opn)
        
        assert len(exec_stack) == 1,\
            "residual stack elements: {!r}".format(exec_stack)
        
        return exec_stack.pop() 

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
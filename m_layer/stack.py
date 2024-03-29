"""
"""
import numbers
from fractions import Fraction 

from collections import ChainMap
from collections import abc

# ---------------------------------------------------------------------------
__all__ = (
    'Stack',
    'ProductOfPowers',
    'normal_form',
)
                                                   
# ---------------------------------------------------------------------------
class ProductOfPowers(object):

    """
    :class:`ProductOfPowers` represents an expression of products of 
    powers of objects, and includes a numerical a prefactor.  
    
    The ``factors`` attribute is a mapping of Python objects to powers 
    The ``prefactor`` attribute is a floating point number. 
    
    This can be used as a dimensional vector, where the factor keys
    refer to base objects.
    
    """
    # Note that the powers-of-products form is insensitive to the 
    # order of multiplication and division in the initial expression;
    # it allows arithmetically equivalent forms to be seen 
    # as equal. However, sometimes there are factors embedded in the original
    # expression. For instance, [litres per 100 kilometres] could 
    # become {'litres':1,'kilometres':-1,'prefactor':0.01}, in which
    # the numerical factor of 1/100 is retained but not as might be expected. 

    # Also, something like [10 litres per 100 kilometres] would combine
    # the two factors, giving {'litres':1,'kilometres':-1,'prefactor':0.1}.
    
    # Note the rmul factors may apply to combinations of objects, not 
    # just single objects, so a more complete representation is complicated. 
    
    __slots__ = ('prefactor','factors')
    
    def __init__(self,factors,prefactor=1):
        # Hoping that the Fraction class will handle integer factors
        # in the numerator and denominator without approximation
        # Arithmetic operations on the class will result in float 
        # when the operation cannot be exactly represented as a fraction.
        self.prefactor = Fraction( *prefactor ) if isinstance(
            prefactor,abc.Iterable) else Fraction( prefactor )
        self.factors = factors
 
    def __str__(self):
        if self.prefactor == 1:
            return "{!s}".format(self.prefactor)
        else:
            return "{!s}:{!s}".format(
                self.prefactor,
                self.factors
            )
        
    def __repr__(self):
        if self.prefactor == 1:
            return "ProductOfPowers({!s})".format(
                self.factors
            )
        else:
            return "ProductOfPowers({!s},prefactor={!s})".format(
                self.factors,
                self.prefactor
            )
         
    def __eq__(self,other):
        return (
            isinstance(other,self.__class__)
        and
            # Mappings are equal if they have the same 
            # key-value pairs regardless of ordering
            self.factors == other.factors
        and
            self.prefactor == other.prefactor
        )
 
    def __mul__(self,rhs):
        return self.__class__(
            { 
                i: self.factors.get(i,0) + rhs.factors.get(i,0)
                    for i in ChainMap(self.factors,rhs.factors) 
            },
            self.prefactor*rhs.prefactor
        )  
        
    def __rmul__(self,lhs):
        assert isinstance(lhs,numbers.Integral), repr(lhs)
        return self.__class__(
            self.factors,
            lhs*self.prefactor
        )    
    
    def __truediv__(self,rhs):
        return self.__class__(
            { 
                i: self.factors.get(i,0) - rhs.factors.get(i,0)
                    for i in ChainMap(self.factors,rhs.factors) 
            },
            self.prefactor/rhs.prefactor
        )    
    
    def __pow__(self,x):
        assert isinstance(x,numbers.Integral), repr(x)
        return self.__class__(
            { 
                i: x*v for i,v in self.factors.items() 
            },
            self.prefactor**x
        )    
    
# ---------------------------------------------------------------------------
def normal_form(rpn):
    """
    Return a :class:`ProductOfPowers` for the RPN expression as
    a product of powers of objects, and including a scaling prefactor. 
    
    Args:
        rpn (:class:`Stack`)
        
    Returns:
        :class:`ProductOfPowers`
        
    """
    assert isinstance(rpn,Stack), repr(rpn)
        
    stk = []    
    for o_i in rpn._obj:

        if o_i not in ('mul','div','rmul','pow'):   
            if isinstance(o_i, numbers.Integral):
                stk.append( o_i )
            else:
                stk.append( 
                    ProductOfPowers({o_i:1}) 
                )
        else:
            if o_i == 'mul':
                x,y = stk.pop(), stk.pop()
                stk.append( y * x )
                                
            elif o_i == 'rmul':               
                x,y = stk.pop(), stk.pop()
                stk.append( x * y )
                                
            elif o_i == 'div':
                x,y = stk.pop(), stk.pop()
                stk.append( y / x )
                                
            elif o_i == 'pow':
                x,y = stk.pop(), stk.pop()
                stk.append( y**x )
                
            else:
                raise RuntimeError(opn)
        
    assert len(stk) == 1,\
        "residual stack elements: {!r}".format(stk)
    
    return stk.pop() 
        
# ---------------------------------------------------------------------------
class Stack(object):

    """
    A Stack holds numbers and tokens for simple arithmetic operations.
    Operations like `mul, `div`, etc., return a new Stack object.
    
    """
    
    def __init__(self,obj=list()):  
        if isinstance(obj,list):
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
                    
                    den = str(y)
                    if den[0] == '(' and den[-1] == ')':
                        stk.append( "{!s}/{!s}".format( y,x ) )
                    else:
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
        return Stack(self._obj + list(obj))
        
    def push(self,x):
        """
        Args:
            x (:class:`Stack` or single object)
            
        When ``x`` is a :class:`Stack` the contents 
        are used to extend the current stack. 
        
        """
        
        if hasattr(x,'stack'):
            return self._append( x.stack._obj )     
            
        elif isinstance(x,Stack):
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
    print( ( normal_form(s) ) ) 
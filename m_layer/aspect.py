"""
The M-layer introduces the notion of a kind of quantity as an explicit component 
in the expression of measured data. The term 'aspect' broader in meaning
than 'kind of quantity'. 

"""
import numbers

from m_layer.context import default_context as cxt
from m_layer.stack import Stack

# ---------------------------------------------------------------------------
__all__ = (
    'Aspect',
    'no_aspect'
)
# ---------------------------------------------------------------------------
class ComposedAspect(object):

    __slots__ = (
        '_aspect_stack', '_uid'
    )

    def __init__(self,aspect_stack):
    
        assert isinstance(aspect_stack,Stack)      
        self._aspect_stack = aspect_stack

    @property 
    def aspect(self):
        return self._aspect_stack
  
    @property
    def uid(self):
        """
        A pair of RPN sequences containing Scale and Aspect uids, 
        arithmetic operations 'mul', 'rmul', 'div', 'pow', and integers.
        
        """
        try:
            return self._uid
        except AttributeError:
            self._uid = tuple(
                o.uid if isinstance(o,Aspect) else o
                    for o in self.aspect
            )            
            return self._uid
  
    def __mul__(self,y):
        return ComposedAspect(
            self.aspect.push(y.aspect).mul()
        )

    def __truediv__(self,y):
        return ComposedAspect(
            self.aspect.push(y.aspect).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedAspect(
            self.aspect.push(y).pow()
        )

    def __str__(self):
        return "{!s}".format( self.aspect )
        
    def __repr__(self):
        return "ComposedAspect({!r})".format( self.aspect ) 
        

# ---------------------------------------------------------------------------
class Aspect(object):

    """
    Aspect objects provide a lightweight wrapper around the 
    unique identifier for an M-layer aspect.  
    """

    __slots__ = (
        '_aspect_uid',
    )
    
    def __init__(self,aspect_uid):    
        self._aspect_uid = aspect_uid

    def _from_json(self,locale=None,short=False):
        aspect_json = cxt.aspect_reg[self._aspect_uid] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return aspect_json['locale'][locale][locale_key]

    @property 
    def aspect(self):
        return self 
        
    @property 
    def uid(self):
        "The M-layer identifier for this aspect"
        return self._aspect_uid
        
    def __eq__(self,other):
        """
        True when both objects have the same uid
        An aspect with uid ``None`` is never equal 
        to another aspect.
        """
        if self._aspect_uid is not None and hasattr(other,'uid'):
            return self.uid[1] == other.uid[1] 
        else:
            return False

    def __mul__(self,y):
        return ComposedAspect(
            Stack().push(self.aspect).push(y.aspect).mul()
        )

    def __truediv__(self,y):
        return ComposedAspect(
            Stack().push(self.aspect).push(y.aspect).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedAspect(
            Stack().push(self.aspect).push(y).pow()
        )
        
    def __str__(self):
        if self.uid is None:
            return ""
        else:
            return str( self._from_json() )
        
    def __repr__(self):
        if self.uid is None:
            return ""
        else:
            return "Aspect{!r}".format( self.uid )

# ---------------------------------------------------------------------------
no_aspect = Aspect(None)    

# ===========================================================================
if __name__ == '__main__':

    M = Aspect( ('ml_mass', 321881801928222308627062904049725548287) )
    L = Aspect( ('ml_length', 993853592179723568440264076369400241) )
    T = Aspect( ('ml_time', 59007067547744628223483093626372886675) )
    
    print(M**2*L/T)
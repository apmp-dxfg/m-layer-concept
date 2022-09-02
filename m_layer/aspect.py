"""
The M-layer includes the notion of kind of quantity as a component 
called *aspect* in expressions of measured data. 
The term 'aspect' is broader in meaning than 'kind of quantity'. 

"""
import numbers

from m_layer.context import default_context as cxt
from m_layer.stack import Stack, normal_form

# ---------------------------------------------------------------------------
__all__ = (
    'Aspect',
    'ComposedAspect',
    'no_aspect'
)

# ---------------------------------------------------------------------------
class ComposedAspect(object):

    """
    A :class:`ComposedAspect` holds an :class:`Aspect` expression
    """

    __slots__ = (
        '_stack', '_uid'
    )

    def __init__(self,aspect_stack):
    
        assert isinstance(aspect_stack,Stack)      
        self._stack = aspect_stack

    @property 
    def stack(self):
        return self._stack
  
    @property
    def uid(self):
        """
        
        
        """
        try:
            return self._uid
        except AttributeError:
            # Reduce to a product of powers
            pops = normal_form(self.stack)
            self._uid = dict({
                i.uid : v 
                    for i,v in pops.factors.items()
            })
                                                   
            return self._uid
  
    def __mul__(self,y):
        return ComposedAspect(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return ComposedAspect(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedAspect(
            self.stack.push(y).pow()
        )

    def __str__(self):
        return "{!s}".format( self.stack )
        
    def __repr__(self):
        return "{!s}({!r})".format( self.__class__,self.stack ) 
        

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
    def uid(self):
        "The M-layer identifier for this aspect"
        return self._aspect_uid
        
    def __hash__(self):
        return id(self)
        
    def __eq__(self,other):
        """
        True when both objects have the same uid

        """
        return isinstance(other,Aspect) and self.uid == other.uid 

    def __mul__(self,y):
        return ComposedAspect(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        return ComposedAspect(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedAspect(
            Stack().push(self).push(y).pow()
        )
        
    def __str__(self):
        if self.uid == no_aspect.uid:
            return ""
        else:
            return str( self._from_json() )
        
    def __repr__(self):
        if self.uid == no_aspect.uid:
            return ""
        else:
            return "Aspect{!r}".format( self.uid )

# ---------------------------------------------------------------------------
no_aspect = Aspect((
    "ml_no_aspect",
    295504637700214937127120941173285352815
))    
"""An object representing no assigned aspect"""

# ===========================================================================
if __name__ == '__main__':

    M = Aspect( ('ml_mass', 321881801928222308627062904049725548287) )
    L = Aspect( ('ml_length', 993853592179723568440264076369400241) )
    T = Aspect( ('ml_time', 59007067547744628223483093626372886675) )
    
    print( (M*L/T).uid )
    

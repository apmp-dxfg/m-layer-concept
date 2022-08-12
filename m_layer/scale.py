"""

"""
import numbers

from m_layer.context import default_context as cxt
from m_layer.aspect import Aspect, no_aspect
from m_layer.composition import Stack
from m_layer.system import System
from m_layer.dimension import Dimension

__all__ = (
    'Scale',
    'ScaleAspect',
)

# ---------------------------------------------------------------------------
class ComposedScaleAspect(object):

    """
    For expressions of ScaleAspects
    """

    __slots__ = ("_scale_stack","_aspect_stack","_uid")

    def __init__(self,scale,aspect):
    
        assert isinstance(scale,Stack)
        assert isinstance(aspect,Stack)
        
        self._scale_stack = scale
        self._aspect_stack = aspect

    @property 
    def composable(self): return True
 
    @property
    def scale(self):
        "The scale stack"
        return self._scale_stack 
 
    @property 
    def aspect(self):
        "The aspect stack"
        return self._aspect_stack
            
    # Alias
    kind_of_quantity = aspect 

    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        return ComposedScaleAspect(
            self.scale.push(x).rmul(),
            self.aspect.copy()
        )
        
    def __mul__(self,y):
        return ComposedScaleAspect(
            self.scale.push(y.scale).mul(),
            self.aspect.push(y.aspect).mul()
        )

    def __truediv__(self,y):
        return ComposedScaleAspect(
            self.scale.push(y.scale).div(),
            self.aspect.push(y.aspect).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedScaleAspect(
            self.scale.push(y.scale).pow(),
            self.aspect.push(y.aspect).pow()
        )
    
    # There is no `uid` in the central register for composed objects.
    # However, a `uid` is needed for records.
    # One possibility is to provide uid expressions in RPN.
    # Such a stack is easy to operate on to produce other forms
    # and allows numeric pre-factors, like 100.km.
    # An alternative would be a dict-like mapping between 
    # objects and exponents, but this cannot handle pre-factors.
    # Perhaps these can be combined: initially reduce to 
    # a 'normal' form and then express that in RPN
    # (with pre-factors bound to their scale, like (100.km)^2). 
    
    @property
    def uid(self):
        """
        A pair of RPN sequences containing Scale and Aspect uids, 
        arithmetic operations 'mul', 'rmul', 'div', 'pow', and integers.
        
        """
        try:
            return self._uid
        except AttributeError:
            # Construct a uid from the scale and attribute stacks
            scale = tuple(
                o.uid if isinstance(o,Scale) else o
                    for o in self.scale
            )
                    
            aspect = tuple(
                o.uid if isinstance(o,Aspect) else o
                    for o in self.aspect
            )
                    
            self._uid = scale, aspect
            
            return self._uid
            
    # Equality (`==` method) could be based on the equivalence of expressions
    # without simplification (indifferent to ordering of terms).
    # Explicit function names like `commensurate` might be better. 
            
    def __str__(self):
        return "({!s}, {!s})".format( self.scale, self.aspect )
        
    def __repr__(self):
        return "ComposedScaleAspect({!r},{!r})".format( self.scale, self.aspect ) 
        
# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale-aspect pair
    Objects are immutable.
    """

    __slots__ = ("_scale","_aspect")

    def __init__(self,scale,aspect=no_aspect):
        self._scale = scale
        self._aspect = aspect

    @property
    def scale(self):
        "The scale"
        return self._scale 
        
    @property 
    def aspect(self):
        "The aspect or kind of quantity"
        return self._aspect
            
    # Alias
    kind_of_quantity = aspect 

    @property 
    def uid(self):
        "A pair of M-layer identifiers for scale and aspect"
        return (self.scale.uid,self.aspect.uid)

    @property 
    def composable(self):
        return self._scale.scale_type == "ratio"
        
    # These arithmetic operations must match operations in ComposedScaleAspect
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        assert self.composable
        
        return ComposedScaleAspect(
            Stack().push(self.scale).push(x).rmul(),
            Stack().push(self.aspect) 
        )
        
    def __mul__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            Stack().push(self.scale).push(y.scale).mul(),
            Stack().push(self.aspect).push(y.aspect).mul()
        )

    def __truediv__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            Stack().push(self.scale).push(y.scale).div(),
            Stack().push(self.aspect).push(y.aspect).div()
        )
 
    def __pow__(self,x):
        assert isinstance(x,numbers.Integral)
        assert self.composable

        return ComposedScaleAspect(
            Stack().push(self.scale).push(x).pow(),
            Stack().push(self.aspect).push(x).pow()
        )
        
    def __eq__(self,other):
        "True when the M-layer identifiers of both objects match"
        return (
            isinstance(other,ScaleAspect)
        and self.scale == other.scale
        and self.aspect == other.aspect
        )
        
    def __str__(self):
        return "({!s}, {!s})".format(self.scale,self.aspect)
        
    def __repr__(self):
        return "ScaleAspect({!r},{!r})".format( self.scale,self.aspect ) 
                 
# ---------------------------------------------------------------------------
class Scale(object):

    """
    Scale objects provide a lightweight wrapper around the 
    unique identifier for an M-layer scale.  
    """

    __slots__ = (
        '_scale_uid','_scale_type', '_system', '_dimensions'
    )
    
    def __init__(self,scale_uid):    
        self._scale_uid = scale_uid

    def _from_json(self):
        return cxt.scale_reg[self._scale_uid] 

    def _json_scale_to_ref(self,locale=None,short=False):
    
        scale_json = self._from_json()
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return ref_uid['locale'][locale][locale_key]
        
    @property 
    def uid(self):
        "The M-layer identifier for this aspect"
        return self._scale_uid
        
    @property 
    def scale_type(self):
        try:
            return self._scale_type
        except AttributeError:
            scale_json = self._from_json()
            self._scale_type = scale_json['scale_type']
            return self._scale_type

    @property 
    def system(self):
        try:
            return self._system
        except AttributeError:
            # Look at the reference 
            # to see if a system is identified 
            scale_json = self._from_json()
            ref_json = cxt.reference_reg[ tuple(scale_json['reference']) ] 
            if 'system' in ref_json:
                self._system = System( tuple(ref_json['system']['uid']) )
            else:
                self._system = None
                
            return self._system
 
    @property 
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            system = self.system
            if system is None: 
                self._dimension = None
            else:
                scale_json = self._from_json()
                ref_json = cxt.reference_reg[ tuple(scale_json['reference']) ] 
                self._dimensions = Dimension( 
                    system,
                    tuple( ref_json['system']['dimensions'])
                )
                
            return self._dimensions 
            
    def __eq__(self,other):
        "True when both objects have the same uids"
        return isinstance(other,Scale) and self.uid[1] == other.uid[1] 
        
    def __str__(self):
        return self._json_scale_to_ref(short=True)
        
    def __repr__(self):
        return "Scale({!r})".format( self.uid )

    def to_scale_aspect(self,aspect=no_aspect):
        """
        Return a :class:`~scale_aspect.ScaleAspect` object 
        combining this scale and ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 
         
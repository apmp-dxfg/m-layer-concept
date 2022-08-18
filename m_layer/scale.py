"""

"""
import numbers

from m_layer.context import default_context as cxt
from m_layer.aspect import Aspect, ComposedAspect, no_aspect
from m_layer.stack import Stack, normal_form, ProductOfPowers
from m_layer.system import System
from m_layer.dimension import Dimension

__all__ = (
    'Scale',
    'ScaleAspect',
)

# ---------------------------------------------------------------------------
class ComposedScaleAspect(object):

    __slots__ = ("_scale","_aspect","_uid","_dimension")

    def __init__(self,scale_xp,aspect_xp):
    
        assert isinstance(scale_xp,ComposedScale), repr(scale_xp)
        assert isinstance(aspect_xp,ComposedAspect), repr(aspect_xp)
        
        self._scale = scale_xp
        self._aspect = aspect_xp

    @property 
    def composable(self): return True
 
    @property
    def scale(self):
        return self._scale 
 
    @property 
    def aspect(self):
        return self._aspect
            
    # Alias
    kind_of_quantity = aspect 

    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        return ComposedScaleAspect(
            x*self.scale,
            x*self.aspect
        )
        
    def __mul__(self,y):
        return ComposedScaleAspect(
            self.scale*y.scale,
            self.aspect*y.aspect
        )

    def __truediv__(self,y):
        return ComposedScaleAspect(
            self.scale/y.scale,
            self.aspect/y.aspect
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedScaleAspect(
            self.scale**y.scale,
            self.aspect**y.aspect
        )
    
    @property
    def dimension(self):
        return self.scale.dimension
 
    # There is no `uid` in the central register for composed objects.
 
    @property
    def uid(self):
        """
        A pair of RPN sequences containing Scale and Aspect uids, 
        arithmetic operations 'mul', 'rmul', 'div', 'pow', and integers.
        
        """
        try:
            return self._uid
        except AttributeError:
            # Construct a uid from the scale and attribute RPN stacks
            pops = normal_form(self.scale.stack)
            scale = ProductOfPowers(
                {
                    i.uid : v 
                        for i,v in pops.factors.items()
                },
                prefactor=pops.prefactor
            )
                    
            pops = normal_form(self.aspect.stack)
            aspect = ProductOfPowers(
                {
                    i.uid : v 
                        for i,v in pops.factors.items()
                },
                prefactor=pops.prefactor
            )
                    
            self._uid = scale, aspect
            
            return self._uid
            
    # Equality (`==` method) could be based on the equivalence of expressions
    # without simplification (indifferent to ordering of terms).
    # Explicit function names like `commensurate` might be better. 
      
    def __str__(self):
        return "({!s}, {!s})".format( self.scale, self.aspect )
        
    def __repr__(self):
        return "{!s}({!r},{!r})".format( 
            self.__class__,self.scale, self.aspect 
        ) 
        
# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale-aspect pair
    Objects are immutable.
    """

    __slots__ = ("_scale","_aspect")

    def __init__(self,scale,aspect=no_aspect):
        assert isinstance(scale,Scale)
        assert isinstance(aspect,Aspect)
        
        self._scale = scale
        self._aspect = aspect

    @property
    def scale(self):
        return self._scale 
        
    @property 
    def aspect(self):
        return self._aspect
            
    # Alias
    kind_of_quantity = aspect 

    @property 
    def uid(self):
        "A pair of M-layer identifiers for scale and aspect"
        return (self.scale.uid,self.aspect.uid)

    @property 
    def composable(self):
        return self.scale.composable
        
    # These arithmetic operations must match operations in ComposedScaleAspect
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        assert self.composable
        
        return ComposedScaleAspect(
            ComposedScale( Stack().push(self.scale).push(x).rmul() ),
            ComposedAspect( Stack().push(self.aspect) )
        )
        
    def __mul__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            ComposedScale( Stack().push(self.scale).push(y.scale).mul() ),
            ComposedAspect( Stack().push(self.aspect).push(y.aspect).mul() )
        )

    def __truediv__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            ComposedScale( Stack().push(self.scale).push(y.scale).div() ),
            ComposedAspect( Stack().push(self.aspect).push(y.aspect).div() )
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        assert self.composable

        return ComposedScaleAspect(
            ComposedScale( Stack().push(self.scale).push(y).pow() ),
            ComposedAspect( Stack().push(self.aspect).push(y).pow() )
        )
        
    def __eq__(self,other):
        "True when the M-layer identifiers of both objects match"
        return (
            isinstance(other,ScaleAspect)
        and self.scale == other.scale
        and self.aspect == other.aspect
        )
        
    def __hash__(self):
        return id(self)
        
    def __str__(self):
        return "({!s}, {!s})".format(self.scale,self.aspect)
        
    def __repr__(self):
        return "{!s}({!r},{!r})".format( 
            self.__class__,self.scale,self.aspect
        ) 
  
# ---------------------------------------------------------------------------
class ComposedScale(object):
 
    __slots__ = (
        '_uid', '_stack', '_dimension'
    )
 
    def __init__(self,scale_stack):

        assert isinstance(scale_stack,Stack)
        self._stack = scale_stack

    @property 
    def uid(self):
        try:
            return self._uid
        except AttributeError:
            assert False
        
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            # 
            stack = []
            ptr_it = iter(self.stack)
            ptr = next(ptr_it)
            
            while True:
                try: 
                    if isinstance(ptr,Scale):
                        stack.append(ptr.dimension)
                        ptr = next(ptr_it)
                        
                    elif ptr == 'mul':
                        x,y = stack.pop(),stack.pop()
                        stack.append( y*x ) 
                        ptr = next(ptr_it)
                        
                    elif ptr == 'div':
                        x,y = stack.pop(),stack.pop()
                        stack.append( y/x ) 
                        ptr = next(ptr_it)
                        
                    elif ptr == 'pow':
                        x,y = stack.pop(),stack.pop()
                        stack.append( y**x ) 
                        ptr = next(ptr_it)

                    if isinstance(ptr,numbers.Integral):  
                        stack.append( ptr )
                        ptr = next(ptr_it)
                        
                        # Deal with 'rmul' case immediately
                        # Otherwise the number is an exponent 
                        if ptr == 'rmul':
                            x,y = stack.pop(),stack.pop()
                            stack.append( x*y )
                            ptr = next(ptr_it)
                     
                except StopIteration:
                    break
                
            assert len(stack) == 1, repr(stack)
            self._dimension = stack.pop()
            return self._dimension
            
    @property
    def stack(self):
        return self._stack 
 
    @property 
    def scale_type(self):
        return "ratio"
  
    @property 
    def composable(self):
        return True
 
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)      
        return ComposedScale(
            self.stack.push(x).rmul()
        )

    def __mul__(self,y):
        return ComposedScale(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return ComposedScale(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedScale(
            self.stack.push(y).pow()
        )

    def __str__(self):
        return "{!s}".format( self.stack )
        
    def __repr__(self):
        return "{!s}({!r})".format( self.__class__,self.stack )  
        
# ---------------------------------------------------------------------------
class Scale(object):

    """
    Scale objects provide a lightweight wrapper around the 
    unique identifier for an M-layer scale.  
    """

    __slots__ = (
        '_scale_uid','_scale_type', '_dimension'
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
    def composable(self):
        return self.scale_type == "ratio"
        
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
    def dimension(self):
        """
        Return a :class:`~dimension.Dimension` when a scale is associated  
        with a reference in a coherent system of units, like the SI.
        Otherwise return ``None``.
        
        """
        try:
            return self._dimension
        except AttributeError:
            scale_json = self._from_json()
            ref_json = cxt.reference_reg[ tuple(scale_json['reference']) ] 
            if 'system' in ref_json:
                self._dimension = Dimension( 
                    System( tuple(ref_json['system']['uid']) ),
                    tuple( ref_json['system']['dimensions']),
                    float( ref_json['system']['prefix'] )
                )
            else:
                self._dimension = None
                
            return self._dimension 
            
    def __eq__(self,other):
        "True when both objects have the same uids"
        return isinstance(other,Scale) and self.uid[1] == other.uid[1] 
 
    def __hash__(self):
        return id(self)
        
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        assert self.composable       
        return ComposedScale(
            Stack().push(self).push(x).rmul()
        )

    def __mul__(self,y):
        assert self.composable
        return ComposedScale(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        assert self.composable
        return ComposedScale(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        assert self.composable
        return ComposedScale(
            Stack().push(self).push(y).pow()
        )    
        
    def __str__(self):
        return self._json_scale_to_ref(short=True)
        
    def __repr__(self):
        return "{!s}({!r})".format( self.__class__,self.uid )

    def to_scale_aspect(self,aspect=no_aspect):
        """
        Return a :class:`~scale.ScaleAspect` 
        combining this scale and ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 

# ===========================================================================
if __name__ == '__main__':

    M = Scale( ('ml_imp_pound_ratio', 188380796861507506602975683857494523991) )
    L = Scale( ('ml_foot_ratio', 150280610960339969789551668292960104920) )
    T = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )
    
    print(100*M*L/T) 
   

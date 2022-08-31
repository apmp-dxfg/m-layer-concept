"""

"""
import numbers

from m_layer.context import default_context as cxt
from m_layer.aspect import Aspect, ComposedAspect, no_aspect
from m_layer.stack import Stack, product_of_powers
from m_layer.system import System
from m_layer.dimension import Dimension

__all__ = (
    'Scale',
    'ComposedScale',
    'ScaleAspect',
    'ComposedScaleAspect'
)

# ---------------------------------------------------------------------------
class ComposedScaleAspect(object):

    """
    A :class:`ComposedScaleAspect` holds a :class:`ScaleAspect` expression
    """
    
    __slots__ = ( "_stack","_uid", "_dimension" )

    def __init__(self,scale_aspect_stack):
    
        assert isinstance(scale_aspect_stack,Stack), repr(scale_aspect_stack)       
        self._stack = scale_aspect_stack

    @property 
    def composable(self): return True
 
    @property
    def stack(self):
        return self._stack 
 
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        return ComposedScaleAspect( self.stack.push(x).rmul() )
        
    def __mul__(self,y):
        return ComposedScaleAspect(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return ComposedScaleAspect(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return ComposedScaleAspect(
            self.stack.push(y).pow()
        )
    
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            self._dimension = product_of_powers(
                self.stack,
                lambda i: i.scale.dimension 
            )
            return self._dimension

    @property
    def uid(self):
        """
        A product of powers for Scale-Aspect uid pairs.
        
        """
        # There is no `uid` in the central register for composed objects.
        try:
            return self._uid
        except AttributeError:
            self._uid = product_of_powers(
                self.stack,
                lambda i: i.uid 
            )                                                   
            return self._uid
            
    # Equality (`==` method) could be based on the equivalence of expressions
    # without simplification (indifferent to ordering of terms).
    # Explicit function names like `commensurate` might be better. 
      
    def __str__(self):
        return "({!s})".format( self.stack )
        
    def __repr__(self):
        return "ComposedScaleAspect({!r})".format(self.stack) 
        
# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale and aspect pair.
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
            Stack().push(self).push(x).rmul() 
        )
        
    def __mul__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        assert self.composable
        assert y.composable

        return ComposedScaleAspect(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        assert self.composable

        return ComposedScaleAspect(
            Stack().push(self).push(y).pow()
        )
        
    def __eq__(self,other):
        "True when the M-layer identifiers of both objects match"
        return (
            isinstance(other,self.__class__)
        and 
            self.scale == other.scale
        and 
            self.aspect == other.aspect
        )
        
    def __hash__(self):
        return id(self)
        
    def __str__(self):
        return "({!s}, {!s})".format(self.scale,self.aspect)
        
    def __repr__(self):
        return "ScaleAspect({!r},{!r})".format( 
            self.scale,self.aspect
        ) 
  
# ---------------------------------------------------------------------------
class ComposedScale(object):
 
    """
    A :class:`ComposedScale` holds a :class:`Scale` expression
    """
    
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
            self._uid = product_of_powers(
                self.stack,
                lambda i: i.uid 
            )
            return self._uid
        
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            self._dimension = product_of_powers(
                self.stack,
                lambda i: i.scale.dimension 
            )
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
        return "ComposedScale({!r})".format( self.stack )  
  
    def to_composed_scale_aspect(self,composed_scale_aspect):
        """
        Return a :class:`~scale.ComposedScaleAspect` 
        by copying the aspects in ``composed_scale_aspect``.
        
        Args:
            composed_scale_aspect (:class:`~scale.ComposedScaleAspect`)
        
        .. warning:
        
            This function will fail if the encoded expression is 
            not in exactly the same form as the expression in ``composed_scale_aspect``.
            
            For example, reversing the order of terms in a 
            multiplication will lead to failure.            
            
        """
        # This seems risky. Unless we really need to do this,
        # it should probably be removed.
        
        sa_stack = composed_scale_aspect.stack 
        assert len(sa_stack) == len(self.stack)
        
        stk = []
        for i,o_i in enumerate(sa_stack):
            if o_i not in ('mul','div','rmul','pow'):
            
                # At this point the ability to 
                # convert later can be checked:
                # if src scale and aspect don't convert 
                # to the dst scale, then something is wrong.
                
                src_scale_uid, src_aspect_uid = sa_stack[i].uid       
                dst_scale_uid = self.stack[i].uid 
                cxt.convertible(
                    src_scale_uid, src_aspect_uid,                   
                    dst_scale_uid
                )    
                
                stk.append( 
                    self.stack[i].to_scale_aspect( 
                        sa_stack[i].aspect 
                    ) 
                )
            else:
                stk.append( o_i )                
                           
        return ComposedScaleAspect( Stack(stk) )
  
# ---------------------------------------------------------------------------
class Scale(object):

    """
    A Scale encapsulates a unique identifier for an M-layer scale.  
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
                return self._dimension 
                
            else:
                raise RuntimeError("No dimension for {!r}".format(self))
                
            
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
        return "Scale({!r})".format( self.uid )

    def to_scale_aspect(self,aspect=no_aspect):
        """
        Return a :class:`~scale.ScaleAspect` 
        combining this scale and ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 

# ===========================================================================
if __name__ == '__main__':

    # M = Scale( ('ml_si_kilogram_ratio', 12782167041499057092439851237297548539) )
    # L = Scale( ('ml_si_metre_ratio', 17771593641054934856197983478245767638) )
    # T = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )

    M = Scale( ('ml_imp_pound_ratio', 188380796861507506602975683857494523991) )
    L = Scale( ('ml_foot_ratio', 150280610960339969789551668292960104920) )
    T = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )
    
    print((100*M*L/T).uid) 
   

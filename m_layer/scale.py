"""

"""
import numbers
import json 

from ast import literal_eval

from m_layer.context import default_context as cxt
from m_layer.aspect import Aspect, ComposedAspect, no_aspect
from m_layer.reference import Reference
from m_layer.stack import Stack
from m_layer.system import System
from m_layer.dimension import Dimension, ComposedDimension
from m_layer.uid import UID, ComposedUID 

# ---------------------------------------------------------------------------
__all__ = (
    'Scale',
    'ComposedScale',
    'ScaleAspect',
    'ComposedScaleAspect'
)
# ---------------------------------------------------------------------------
def to_str(o):
    "JSON objects can't have tuple keys"
    if isinstance(o,tuple):
        return "[{0[0]!r}, {0[1]}]".format(o)
    else:
        return o
                    

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
            self._dimension = ComposedDimension(self.stack)
            return self._dimension

    @property
    def json(self):
        uid = self.uid 
        factors = {
            str(k) : list(v) 
                for k,v in uid.factors.items()
        }
        obj = dict(
            __type__ = "ComposedScaleAspect",
            prefactor = uid.prefactor,
            factors = factors
        )
        return json.dumps(obj)

    @property
    def uid(self):
        """
        A product of powers for Scale-Aspect uid pairs.
        
        """
        try:
            return self._uid
        except AttributeError:
            self._uid = ComposedUID(self.stack)
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

    __slots__ = ("_scale","_aspect","_dimension")

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
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            # If there are no defined dimensions a RuntimeError  
            # is raised here. Allow it to propagate.
            self._dimension = self.scale.dimension
            return self._dimension

    @property
    def json(self):
        obj = dict(
            __type__ = "ScaleAspect",
            scale = to_str( self.scale.uid ),
            aspect = to_str( self.aspect.uid )
        )
        return json.dumps(obj)

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
            self._uid = ComposedUID(self.stack)
            return self._uid
        
    @property
    def json(self):
        uid = self.uid 
        factors = {
            str(k) : list(v) 
                for k,v in uid.factors.items()
        }

        obj = dict(
            __type__ = "ComposedScale",
            factors = factors,
            prefactor = uid.prefactor
        )
        return json.dumps(obj)

    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            self._dimension = ComposedDimension(self.stack)
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
        # This seems risky. 
        
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
        '_scale_uid','_scale_type', '_reference'
    )
    
    def __init__(self,scale_uid):    
        self._scale_uid = UID(scale_uid)
        self._scale_type = cxt.scale_reg[self._scale_uid]['scale_type']
        self._reference = Reference(
            cxt.scale_reg[self._scale_uid]['reference']
        ) 
        
    @property
    def json(self):
        obj = dict(
            __type__ = "Scale",
            uid = str( self._scale_uid.uid ) 
        )
        return json.dumps(obj)

    @property 
    def composable(self):
        return self.scale_type == "ratio"
        
    @property 
    def uid(self):
        return self._scale_uid
        
    @property 
    def scale_type(self):
        return self._scale_type
     
    @property 
    def dimension(self):
        """
        Return a :class:`~dimension.Dimension` when a scale is associated  
        with a reference in a coherent system of units, like the SI.
        Otherwise return ``None``.
        
        """
        return self._reference.dimension
            
    def __eq__(self,other):
        "True when both objects have the same uids"
        return isinstance(other,Scale) and self.uid == other.uid 
 
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
        return "{}".format(self._reference)
        # return self._json_scale_to_ref(short=True)
        
    def __repr__(self):
        return "Scale( {!s} )".format( self.uid )

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
    T2 = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )
    
    # print( (100*M*L/T).json ) 
    # print(T is T2)
    print( (T2/T).json )
   

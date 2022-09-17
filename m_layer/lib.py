import numbers

from m_layer.context import global_context as cxt

from m_layer.dimension import Dimension, CompoundDimension
from m_layer.stack import Stack
from m_layer.uid import UID, CompoundUID 

__all__ = (
    'Reference',
    'Scale',
    'CompoundScale',
    'ScaleAspect',
    'CompoundScaleAspect',
    'Aspect',
    'CompoundAspect',
    'no_aspect',
    'System',
)

# ---------------------------------------------------------------------------
class CompoundAspect(object):

    """
    A CompoundAspect holds an :class:`Aspect` expression
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
            self._uid = CompoundUID(self.stack)
            return self._uid
 
    @property
    def no_aspect(self):
        """
        ``True`` if ``no_aspect`` is anywhere in the expression.
        
        """
        return no_aspect.uid in self.uid
        
    def __mul__(self,y):
        return CompoundAspect(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return CompoundAspect(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundAspect(
            self.stack.push(y).pow()
        )

    def __str__(self):
        return "{!s}".format( self.stack )
        
    def __repr__(self):
        return "CompoundAspect({!r})".format( self.stack )       

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
        self._aspect_uid = UID(aspect_uid)

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
        return CompoundAspect(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        return CompoundAspect(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundAspect(
            Stack().push(self).push(y).pow()
        )
        
    def __str__(self):
        if self.uid == no_aspect.uid:
            return ""
        else:
            return self._from_json()
        
    def __repr__(self):
        if self.uid == no_aspect.uid:
            return ""
        else:
            return "Aspect( {!s} )".format( self.uid )

# --------------------------------------------------------------------------- 
no_aspect = Aspect( cxt.no_aspect_uid )    
"An object to represent the absence of an assigned aspect"

# ---------------------------------------------------------------------------
from collections import namedtuple 

class System(object):

    __slots__ = (
        '_uid',
        '_name',
        '_basis'
    )

    def __init__(self,uid):
    
        self._uid = uid = UID( uid )  
        
        self._name = cxt.system_reg[uid]['name']
        
        # The basis is a sequence of M-layer reference uids
        basis = [ UID( tuple(s_i) ) for s_i in cxt.system_reg[uid]['basis'] ] 
        names = [ cxt.reference_reg[ uid_i ]['locale']['default']['symbol'] 
            for uid_i in basis
        ]
        # A namedtuple keeps the order of base units and allows 
        # the reference uids to be indexed or accessed by attribute  
        # using the reference symbol
        self._basis = namedtuple(self._name,names)._make(basis)
                    
    @property
    def uid(self):
        return self._uid
        
    @property 
    def name(self):
        return self._name 
        
    @property 
    def basis(self):
        return self._basis 
        
    def __repr__(self):
        return "System( {} )".format(self.uid)
   
    def __str__(self):
        return "{}".format(self.name)
   
    def __eq__(self,other):
        return (
            isinstance(other,System)
        and
            self.uid == other.uid
        )
   
    def __hash__(self):
        return hash(self._uid)
        
# ---------------------------------------------------------------------------
from ast import literal_eval

def _sys_to_dimension(json_sys):
    """
    """
    # The JSON prefix is a pair of string-formatted
    # integers for the numerator and denominator
    to_prefix_tuple = lambda x: tuple( 
        int( literal_eval(i) ) for i in x 
    )

    to_dim_tuple = lambda x: tuple( literal_eval(x) )
    
    return Dimension( 
        System( UID( json_sys['uid'] ) ),
        to_dim_tuple( json_sys['dimensions'] ),
        to_prefix_tuple( json_sys['prefix'] )
    )       
        
# ---------------------------------------------------------------------------
class Reference(object):

    """
    A Reference encapsulates access to an M-layer entry for a
    unit of measurement or other type of reference.  

    """

    slots = ( '_uid', '_json_entry', '_dimension'  )
    
    def __init__(self,json_uid):
    
        self._uid = UID(json_uid)
        self._json_entry = cxt.reference_reg[self.uid]


    def __hash__(self):
        return hash(self.uid)
    
    def __repr__(self):
        return "Reference({})".format(self.uid)
    
    def __str__(self):    
        return "{}".format(
            self._json_entry['locale']['default']['symbol'] 
        )
        
    @property
    def uid(self): 
        return self._uid 
    
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            if "system" in self._json_entry:
                self._dimension = _sys_to_dimension(self._json_entry["system"])
            else:
                raise RuntimeError("no unit system for {!r}".format(
                        UID( self._json_entry["uid"] )
                    )
                )
                
            return self._dimension
            
# ---------------------------------------------------------------------------
class CompoundScaleAspect(object):

    """
    A :class:`CompoundScaleAspect` holds a :class:`ScaleAspect` expression
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
        return CompoundScaleAspect( self.stack.push(x).rmul() )
        
    def __mul__(self,y):
        return CompoundScaleAspect(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return CompoundScaleAspect(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundScaleAspect(
            self.stack.push(y).pow()
        )
    
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            self._dimension = CompoundDimension(self.stack)
            return self._dimension

    @property
    def uid(self):
        """
        A product of powers for Scale-Aspect uid pairs.
        
        """
        try:
            return self._uid
        except AttributeError:
            self._uid = CompoundUID(self.stack)
            return self._uid
            
    # Equality (`==` method) could be based on the equivalence of expressions
    # without simplification (indifferent to ordering of terms).
    # Explicit function names like `commensurate` might be better. 

    def to_compound_scales_and_aspects(self):
        """
        Return a :class:`CompoundScale`-:class:`CompoundAspect` pair 
        
        Args:
            `compound_scale_aspect` (:class:`CompoundScaleAspect`):
        
        """
        scale_stk = Stack([
            o_i.scale if isinstance(o_i,ScaleAspect) else o_i
                for o_i in self._stack
        ])
        aspect_stk = Stack([
            o_i.aspect if isinstance(o_i,ScaleAspect) else o_i
                for o_i in self._stack
        ])
                    
        return ( 
            CompoundScale( scale_stk ), 
            CompoundAspect( aspect_stk ) 
        )
              
    def __str__(self):
        return "({!s})".format( self.stack )
        
    def __repr__(self):
        return "CompoundScaleAspect({!r})".format(self.stack) 
        
# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale and aspect pair.
    """

    __slots__ = ("_scale","_aspect","_dimension")

    def __init__(self,scale,aspect=no_aspect):
        assert isinstance(scale,Scale), repr(scale)
        assert isinstance(aspect,Aspect), repr(aspect)
        
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
    def uid(self):
        "A pair of M-layer identifiers for scale and aspect"
        return (self.scale.uid,self.aspect.uid)

    @property 
    def composable(self):
        return self.scale.composable
        
    # These arithmetic operations must match operations in CompoundScaleAspect
    def __rmul__(self,x):
        # a numerical scale factor on the left 
        assert isinstance(x,numbers.Integral)
        assert self.composable
        
        return CompoundScaleAspect(
            Stack().push(self).push(x).rmul() 
        )
        
    def __mul__(self,y):
        assert self.composable
        assert y.composable

        return CompoundScaleAspect(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        assert self.composable
        assert y.composable

        return CompoundScaleAspect(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        assert self.composable

        return CompoundScaleAspect(
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
        if self.aspect is no_aspect:
            return str(self.scale)
        else:
            return "({}, {})".format(self.scale,self.aspect)
        
    def __repr__(self):
        if self.aspect is no_aspect:
            return "ScaleAspect({!r})".format( 
                self.scale
            ) 
        else:
            return "ScaleAspect({!r},{!r})".format( 
                self.scale,self.aspect
            ) 
         
# ---------------------------------------------------------------------------
class CompoundScale(object):
 
    """
    A :class:`CompoundScale` holds a :class:`Scale` expression
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
            self._uid = CompoundUID(self.stack)
            return self._uid

    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            self._dimension = CompoundDimension(self.stack)
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
        return CompoundScale(
            self.stack.push(x).rmul()
        )

    def __mul__(self,y):
        return CompoundScale(
            self.stack.push(y).mul()
        )

    def __truediv__(self,y):
        return CompoundScale(
            self.stack.push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundScale(
            self.stack.push(y).pow()
        )

    def __str__(self):
        return "{}".format( self.stack )
        
    def __repr__(self):
        return "CompoundScale({!r})".format( self.stack )  
  
    def to_compound_scale_aspect(self,src=no_aspect):
        """
        Return a :class:`CompoundScaleAspect` 
        taking aspects from ``src``.
        
        Args:
            src (:class:`CompoundScaleAspect` or 
            :class:`CompoundScale` or 
            :class:`CompoundAspect`)
        
        .. warning:
        
            This function will fail if the encoded expression is 
            not in exactly the same form as the expression in ``src``.
            
            For example, simply reversing the order of terms in a 
            multiplication will lead to failure.            
            
        """
        assert len(src.stack) == len(self.stack)       
        
        stk = []
        for i,o_i in enumerate(src.stack):
            if (
                o_i not in ('mul','div','rmul','pow') 
            and
                not isinstance(o_i,numbers.Integral)
            ):
                # At this point the ability to 
                # convert later can be checked:
                # if src scale and aspect don't convert,
                # then something is wrong.
                
                dst_scale_uid = self.stack[i].uid 
                
                if isinstance(src,CompoundScaleAspect):
                    src_scale_uid, src_aspect_uid = src.stack[i].uid
                elif isinstance(src,CompoundAspect):
                    src_scale_uid = dst_scale_uid
                    src_aspect_uid = src.stack[i].uid
                elif src is no_aspect:
                    src_scale_uid = dst_scale_uid
                    src_aspect_uid = no_aspect.uid
                else:
                    assert False, repr(src)
                    
                # Raise an exception if conversion is not going to be possible.
                cxt.convertible(
                    src_scale_uid, src_aspect_uid,                   
                    dst_scale_uid
                )    
                
                if isinstance(src,CompoundScaleAspect):
                    stk.append( 
                        self.stack[i].to_scale_aspect( src.stack[i].aspect ) 
                    )
                elif isinstance(src,CompoundAspect):
                    stk.append( 
                        self.stack[i].to_scale_aspect( src.stack[i] ) 
                    )
                elif src is no_aspect:
                    stk.append( 
                        self.stack[i].to_scale_aspect( no_aspect ) 
                    )
                else:
                    assert False

            else:
                stk.append( o_i )                
                           
        return CompoundScaleAspect( Stack(stk) )
  
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
        return CompoundScale(
            Stack().push(self).push(x).rmul()
        )

    def __mul__(self,y):
        assert self.composable
        return CompoundScale(
            Stack().push(self).push(y).mul()
        )

    def __truediv__(self,y):
        assert self.composable
        return CompoundScale(
            Stack().push(self).push(y).div()
        )
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        assert self.composable
        return CompoundScale(
            Stack().push(self).push(y).pow()
        )    
        
    def __str__(self):
        return str(self._reference)
        
    def __repr__(self):
        return "Scale( {!s} )".format( self.uid )

    def to_scale_aspect(self,aspect=no_aspect):
        """
        Return a :class:`ScaleAspect` 
        combining this scale and ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 
        
# ===========================================================================
# Further configuration of `cxt` requiring some classes defined above.
# 
# Map the M-layer dimensions of systematically named scales to 
# their scale UID.
#
for src_scale_uid in cxt.scale_reg._objects.keys(): 

    json_scale = cxt.scale_reg[src_scale_uid]   
    
    if "systematic" in json_scale:   
    
        ref_uid = UID( json_scale['reference'] )
        json_ref = cxt.reference_reg[ ref_uid ]
        
        dim = _sys_to_dimension( json_ref["system"] )
        
        if dim not in cxt.dimension_conversion_reg:
            assert isinstance(src_scale_uid,UID), type(src_scale_uid)
            cxt.dimension_conversion_reg[dim] = src_scale_uid
            
        assert cxt.dimension_conversion_reg[dim] == src_scale_uid,\
            "systematic scales: {} and {} both refer to {}".format(
                src_scale_uid,
                cxt.dimension_conversion_reg[dim],
                json_ref["uid"]
            )
             

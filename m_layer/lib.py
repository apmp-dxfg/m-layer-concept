import numbers

from collections import defaultdict
from fractions import Fraction

from m_layer.context import global_context as cxt

from m_layer.systematic import Systematic, CompoundSystematic
from m_layer.prefixed import Prefixed
from m_layer.stack import Stack, normal_form
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
        if len(self.uid):
            return all(
                no_aspect.uid == f_i
                    for f_i in self.uid.factors.keys() 
            )
        else:
            return True
        
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
        return "{}".format( self.stack )
        
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
    
    def __init__(self,aspect_uid=cxt.no_aspect_uid):  
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
            return "Aspect()"
        else:
            return "Aspect( {} )".format( self.uid )

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

def _sys_to_systematic(json_sys):
    """
    """
    # The JSON prefix is a pair of string-formatted
    # integers for the numerator and denominator
    to_prefix_tuple = lambda x: tuple( 
        int( literal_eval(i) ) for i in x 
    )

    to_dim_tuple = lambda x: tuple( literal_eval(x) )
    
    prefixed = "prefixed" in json_sys
    
    if prefixed:
        return Systematic( 
            System( UID( json_sys['uid'] ) ),
            to_dim_tuple( json_sys['dimensions'] ),
            to_prefix_tuple( json_sys['prefixed']['prefix'] )
        )   
    else:
        return Systematic( 
            System( UID( json_sys['uid'] ) ),
            to_dim_tuple( json_sys['dimensions'] )
        )   
 
def _sys_to_prefix(json_sys):
    """
    Return a ``Prefixed`` object 
    
    """
    # The JSON prefix is a pair of string-formatted
    # integers for the numerator and denominator
    to_prefix_tuple = lambda x: tuple( 
        int( literal_eval(i) ) for i in x 
    )

    to_dim_tuple = lambda x: tuple( literal_eval(x) )
    
    assert "prefixed" in json_sys, "unexpected"
    
    return Prefixed( 
        UID( json_sys['prefixed']['uid'] ),
        to_prefix_tuple( json_sys['prefixed']['prefix'] )
    )

# ---------------------------------------------------------------------------
class Reference(object):

    """
    A Reference encapsulates an M-layer register entry for a
    unit of measurement or other type of reference.  

    """

    slots = ( 
        '_uid', 
        '_json_entry', 
        '_systematic', '_is_systematic',
        '_prefixed', '_is_prefixed',
    )
    
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
        "The unique identifier of the reference"
        return self._uid 
    
    @property
    def systematic(self):
        "A :class:`~systematic.Systematic` object representing the unit"
        try:
            return self._systematic
        except AttributeError:
            if self.is_systematic:
                self._systematic = _sys_to_systematic(self._json_entry["system"])
            else:
                raise RuntimeError("no unit system for {!r}".format(
                        UID( self._json_entry["uid"] )
                    )
                )
                
            return self._systematic
 
    @property
    def is_systematic(self):
        """
        ``True`` if the reference is a systematic unit in its unit system
        
        A systematic unit has a name composed of products of powers of base 
        unit names (or symbols).
        
        """
        try:
            return self._is_systematic
        except AttributeError:
            if "system" in self._json_entry :
                self._is_systematic = "systematic" in self._json_entry["system"]
            else:    
                self._is_systematic = False
                
            return self._is_systematic
            
    @property
    def is_prefixed(self):
        """
        ``True`` if the reference is a prefixed in the unit system
                
        """
        try:
            return self._is_prefixed
        except AttributeError:
            if "system" in self._json_entry :
                self._is_prefixed = "prefixed" in self._json_entry["system"]
            else:    
                self._is_prefixed = False
                
            return self._is_prefixed
 
    @property
    def prefixed(self):
        """
        """
        try:
            return self._prefixed
        except AttributeError:
            if self.is_prefixed:
                self._prefixed = _sys_to_prefix(self._json_entry["system"])
            else:
                raise RuntimeError("no prefix for {!r}".format(
                        UID( self._json_entry["uid"] )
                    )
                )
                
            return self._prefixed
        
# ---------------------------------------------------------------------------
class CompoundScaleAspect(object):

    """
    A :class:`CompoundScaleAspect` holds a :class:`ScaleAspect` expression
    """
    
    __slots__ = ( 
    "_stack","_uid", "_systematic", "_pops", "_is_systematic",
    # "_str", 
    )

    def __init__(self,scale_aspect_stack):
    
        assert isinstance(scale_aspect_stack,Stack), repr(scale_aspect_stack)       
        self._stack = scale_aspect_stack
        
        # self._str = self._pop_to_str(scale_aspect_stack)

    def _pop(self):
        # The keys in pops.factors are Scale objects.
        try:
            return self._pops
        except AttributeError:
            self._pops = normal_form(self._stack)
        return self._pops
        
    def _pop_to_str(self):
        
        # There may be different objects with the same M-layer UID,
        # but each object instance is recorded once.     

        setter = lambda factors,i,v: (
            # `str(i)` should not be ambiguous in the expression!
            factors[ str(i) ].add(v) if v != 0 else None
        )
        
        factors = defaultdict(set)
        for k,v in self._pop().factors.items():
            setter(factors,k,v)
          
        s = ""
        for k,v in factors.items():
            for i in v:
                if i == 1:
                    s += "{}.".format(k)
                else:
                    s += "{}{}.".format(k,i) 
                    
        return s[:-1] if s[-1] == "." else s
        
    @property 
    def composable(self): return True
 
    @property
    def stack(self):
        return self._stack 
 
    def __rmul__(self,x):
         
        if isinstance(x,numbers.Integral):
            # a numerical scale factor on the left
            return CompoundScaleAspect( self.stack.push(x).rmul() )
        else:
            assert False, repr(x)
            
    def __mul__(self,y):
        return CompoundScaleAspect(
            self.stack.push(y).mul()
        ) if isinstance( 
            y,(ScaleAspect,CompoundScaleAspect) 
          ) else NotImplemented

    def __truediv__(self,y):
        return CompoundScaleAspect(
            self.stack.push(y).div()
        ) if isinstance( 
            y,(ScaleAspect,CompoundScaleAspect) 
          ) else NotImplemented
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundScaleAspect(
            self.stack.push(y).pow()
        )
    
    @property 
    def is_systematic(self):
        """A :class:`CompoundScaleAspect` is systematic when all scales are systematic 
        
        """
        try: 
            return self._is_systematic
        except AttributeError:
            self._is_systematic = all(
                k.is_systematic 
                    for k in self._pop().factors.keys()
            )
            return self._is_systematic

    @property
    def systematic(self):
        try:
            return self._systematic
        except AttributeError:
            self._systematic = CompoundSystematic(self.stack)
            return self._systematic

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
        return "{}".format( self.stack )
        
    def __repr__(self):
        return "CompoundScaleAspect({!r})".format(self.stack) 
        
# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale and aspect pair.
    """

    __slots__ = ("_scale","_aspect", )

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
    def is_systematic(self):
        return self.scale.is_systematic

    @property
    def systematic(self):
        if self.is_systematic: 
            return self.scale.systematic
        else:
            return None

    @property 
    def is_prefixed(self):
        return self.scale.is_prefixed

    @property
    def prefixed(self):
        if self.is_prefixed: 
            return self.scale.prefixed
        else:
            return None

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
        ) if isinstance( 
            y,(ScaleAspect,CompoundScaleAspect) 
          ) else NotImplemented
            
    def __truediv__(self,y):
        assert self.composable
        assert y.composable

        return CompoundScaleAspect(
            Stack().push(self).push(y).div()
        ) if isinstance( 
            y,(ScaleAspect,CompoundScaleAspect) 
          ) else NotImplemented
 
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
        '_uid', '_stack', '_systematic', '_is_systematic', '_pops',
        # '_str'
    )
 
    def __init__(self,scale_stack):

        assert isinstance(scale_stack,Stack)
        self._stack = scale_stack
        
        # self._str = self._pop_to_str()

    def _pop(self):
        # The keys in pops.factors are Scale objects.
        try:
            return self._pops
        except AttributeError:
            self._pops = normal_form(self._stack)
            return self._pops
        
    def _pop_to_str(self):
        
        # There may be different Scale objects with the same M-layer UID,
        # but each object instance is recorded once.     

        setter = lambda factors,i,v: (
            # `str(i)` should not be ambiguous in the expression!
            factors[ str(i) ].add(v) if v != 0 else None
        )
        
        factors = defaultdict(set)
        for k,v in self._pop().factors.items():
            setter(factors,k,v)
          
        s = ""
        for k,v in factors.items():
            for i in v:
                if i == 1:
                    s += "{}.".format(k)
                else:
                    s += "{}{}.".format(k,i) 
                    
        return s[:-1] if s[-1] == "." else s
            
    
    def __str__(self):
        return "{}".format( self.stack )
        
    def __repr__(self):
        return "CompoundScale({!r})".format( self.stack )  
  
    @property 
    def uid(self):
        "The UIDs of the component scales"
        try:
            return self._uid
        except AttributeError:
            self._uid = CompoundUID(self.stack)
            return self._uid

    @property 
    def is_systematic(self):
        """A :class:`CompoundScale` is systematic when all scales are systematic 
        
        """
        try: 
            return self._is_systematic
        except AttributeError:
            self._is_systematic = all(
                k.is_systematic 
                    for k in self._pop().factors.keys()
            )
            return self._is_systematic
            
    @property
    def systematic(self):
        "The dimensions of the component scales"
        try:
            return self._systematic
        except AttributeError:
            self._systematic = CompoundSystematic(self.stack)
            return self._systematic
 
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
        ) if isinstance( y,(Scale,CompoundScale) ) else NotImplemented

    def __truediv__(self,y):
        return CompoundScale(
            self.stack.push(y).div()
        ) if isinstance( y,(Scale,CompoundScale) ) else NotImplemented
 
    def __pow__(self,y):
        assert isinstance(y,numbers.Integral)
        return CompoundScale(
            self.stack.push(y).pow()
        )

    def _to_compound_scale_aspect(self,src=no_aspect):
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
        if src is not no_aspect:
            assert len(src.stack) == len(self.stack)       
        
        stk = []
        for i,o_i in enumerate(self.stack):
            if (
                o_i not in ('mul','div','rmul','pow') 
            and
                not isinstance(o_i,numbers.Integral)
            ):
                assert isinstance(o_i,Scale) , repr(o_i)
                
                dst_scale_uid = o_i.uid 
                
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
                        ScaleAspect( self.stack[i], src.stack[i].aspect ) 
                    )
                elif isinstance(src,CompoundAspect):
                    stk.append( 
                        ScaleAspect( self.stack[i], src.stack[i] ) 
                    )
                elif src is no_aspect:
                    stk.append( 
                        ScaleAspect( self.stack[i], no_aspect ) 
                    )
                else:
                    assert False, repr(src)

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
    def reference(self):
        return self._reference

    @property 
    def is_systematic(self):
        return (
            self.scale_type == 'ratio'
        and
            self._reference.is_systematic
        )
 
    @property 
    def systematic(self):
        """
        Return a :class:`~systematic.Systematic` when a ratio scale
        is associated with a reference in a coherent system of 
        units, like the SI. Otherwise return ``None``.
        
        """
        if self.is_systematic:
            return self._reference.systematic
        else:
            return None

    @property 
    def is_prefixed(self):
        return (
            self.scale_type == 'ratio'
        and
            self._reference.is_prefixed
        )
 
    @property 
    def prefixed(self):
        """
        Return a :class:`~prefixed.Prefixed` when a ratio scale
        is associated with a reference in a coherent system of 
        units, like the SI. Otherwise return ``None``.
        
        """
        if self.is_prefixed:
            return self._reference.prefixed
        else:
            return None
            
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
        ) if isinstance( y,(Scale,CompoundScale) ) else NotImplemented

    def __truediv__(self,y):
        assert self.composable
        return CompoundScale(
            Stack().push(self).push(y).div()
        ) if isinstance( y,(Scale,CompoundScale) ) else NotImplemented
 
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
    
# ===========================================================================
# Further configuration of `cxt`, which requires classes defined above,
# so it cannot be part of context.py (circular import issues).
#
#------------------------------------------------------------------------    
def build_systematic_conversion_registers(cxt):
    """
    Build the context registers needed to handle 
    systematic conversions when one or both 
    of the scales is systematic
    
    """
    if not hasattr(cxt, 'dim_dim_conversion_reg'):
        cxt.dim_dim_conversion_reg = defaultdict(set)
    if not hasattr(cxt, 'src_dim_conversion_reg'):
        cxt.src_dim_conversion_reg = defaultdict(set)
    if not hasattr(cxt, 'dim_dst_conversion_reg'):
        cxt.dim_dst_conversion_reg = defaultdict(set)
        
    for pair_uid in cxt.conversion_reg._table.keys():  

        src_scale_uid, dst_scale_uid = pair_uid
        
        src_scale = Scale( src_scale_uid )  
        dst_scale = Scale( dst_scale_uid ) 
        
        if src_scale.is_systematic and dst_scale.is_systematic:
        
            src_system = src_scale.systematic.system 
            src_dimensions = src_scale.systematic.dimensions 
            dst_system = dst_scale.systematic.system 
            dst_dimensions = dst_scale.systematic.dimensions 

            cxt.dim_dim_conversion_reg[(
                (src_system,src_dimensions),
                (dst_system,dst_dimensions)
            )].add(pair_uid)
            
        elif dst_scale.is_systematic:
            dst_system = dst_scale.systematic.system 
            dst_dimensions = dst_scale.systematic.dimensions 

            cxt.src_dim_conversion_reg[(
                src_scale_uid,
                (dst_system,dst_dimensions)
            )].add(pair_uid)
        
        elif src_scale.is_systematic:
            src_system = src_scale.systematic.system 
            src_dimensions = src_scale.systematic.dimensions 
            cxt.dim_dst_conversion_reg[(
                (src_system,src_dimensions),
                dst_scale_uid
            )].add(pair_uid)
            
        else:
            pass

    #----------------------------------------------------------------------------
    if not hasattr(cxt, 'dim_dim_for_aspect_reg'):
        cxt.dim_dim_for_aspect_reg = dict() 
     
    if not hasattr(cxt, 'dim_dst_for_aspect_reg'):
        cxt.dim_dst_for_aspect_reg = dict() 

    if not hasattr(cxt, 'src_dim_for_aspect_reg'):
        cxt.src_dim_for_aspect_reg = dict() 
     
    for a_uid in cxt.scales_for_aspect_reg._table:

        conversion_reg = cxt.scales_for_aspect_reg[a_uid]
        
        for pair_uid in conversion_reg:

            src_scale_uid, dst_scale_uid = pair_uid
            
            src_scale = Scale( src_scale_uid )  
            dst_scale = Scale( dst_scale_uid ) 
            
            if src_scale.is_systematic and dst_scale.is_systematic:
            
                src_system = src_scale.systematic.system 
                src_dimensions = src_scale.systematic.dimensions 
                
                dst_system = dst_scale.systematic.system 
                dst_dimensions = dst_scale.systematic.dimensions 
                    
                _conversion_reg = cxt.dim_dim_for_aspect_reg.setdefault( 
                    a_uid,defaultdict(set) 
                )
                
                _conversion_reg[(
                    (src_system,src_dimensions),
                    (dst_system,dst_dimensions)
                )].add(pair_uid)
            
            if dst_scale.is_systematic:
            
                dst_system = dst_scale.systematic.system 
                dst_dimensions = dst_scale.systematic.dimensions 
                    
                _conversion_reg = cxt.src_dim_for_aspect_reg.setdefault( 
                    a_uid,defaultdict(set) 
                )
                
                _conversion_reg[(
                    src_scale_uid,
                    (dst_system,dst_dimensions)
                )].add(pair_uid)

            if src_scale.is_systematic:
            
                src_system = src_scale.systematic.system 
                src_dimensions = src_scale.systematic.dimensions 
                    
                    
                _conversion_reg = cxt.dim_dst_for_aspect_reg.setdefault( 
                    a_uid,defaultdict(set) 
                )
                
                _conversion_reg[(
                    (src_system,src_dimensions),
                    dst_scale_uid
                )].add(pair_uid)
        
#------------------------------------------------------------------------    
def build_systematic_casting_registers(cxt):
    """
    Build the context registers needed to handle 
    systematic casting when one or both 
    of the scales is systematic
    
    """
    if not hasattr(cxt, 'dim_dim_cast_reg'):
        cxt.dim_dim_cast_reg = defaultdict(set)
    if not hasattr(cxt, 'src_dim_cast_reg'):
        cxt.src_dim_cast_reg = defaultdict(set)
    if not hasattr(cxt, 'dim_dst_cast_reg'):
        cxt.dim_dst_cast_reg = defaultdict(set)

    for scale_aspect_pair_uid in cxt.casting_reg._table.keys(): 
        src_uid, dst_uid = scale_aspect_pair_uid
        
        src_scale = Scale( src_uid[0] )
        src_aspect = Aspect( src_uid[1] )
        dst_scale = Scale( dst_uid[0] )
        dst_aspect = Aspect( dst_uid[1] )

        if src_scale.is_systematic and dst_scale.is_systematic:
        
            src_system = src_scale.systematic.system 
            src_dimensions = src_scale.systematic.dimensions 
            dst_system = dst_scale.systematic.system 
            dst_dimensions = dst_scale.systematic.dimensions 

            cxt.dim_dim_cast_reg[(
                ((src_system,src_dimensions),src_aspect.uid),
                ((dst_system,dst_dimensions),dst_aspect.uid)
            )].add( (src_scale.uid,dst_scale.uid) )
            
        elif dst_scale.is_systematic:
            dst_system = dst_scale.systematic.system 
            dst_dimensions = dst_scale.systematic.dimensions 

            cxt.src_dim_cast_reg[(
                src_uid,
                ((dst_system,dst_dimensions),dst_aspect.uid)
            )].add( (src_scale.uid,dst_scale.uid) )
        
        elif src_scale.is_systematic:
            src_system = src_scale.systematic.system 
            src_dimensions = src_scale.systematic.dimensions 

            cxt.dim_dst_cast_reg[(
                ((src_system,src_dimensions),src_aspect.uid),
                dst_uid
            )].add( (src_scale.uid,dst_scale.uid) )
            
        else:
            pass 
     
#----------------------------------------------------------------------------
build_systematic_conversion_registers(cxt) 
build_systematic_casting_registers(cxt)

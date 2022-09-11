import json
from collections import defaultdict
from fractions import Fraction

from m_layer.stack import normal_form

__all__ = (
    'UID',
    'CompoundUID'
)

# ---------------------------------------------------------------------------
# The uid key for a ScaleAspect is a tuple of UIDs, 
# so str(k) calls the __repr__ UID method on the elements.
#
fmt_key = lambda k: "[{0[0]}, {0[1]}]".format(k)

# ---------------------------------------------------------------------------
# Encapsulate the format of M-layer UIDs
# So this becomes a point of adaptation.
#
class UID(object):

    __slots__ = ('_m_layer_uuid',)
    
    """
    M = UID( [
        'ml_imp_pound_ratio', 
        188380796861507506602975683857494523991
    ] )
    """
    
    def __init__(self,uid):
        if isinstance(uid,self.__class__):
            self._m_layer_uuid = uid._m_layer_uuid
        elif isinstance(uid,tuple):
            self._m_layer_uuid = uid
        elif isinstance(uid,list):
            self._m_layer_uuid = tuple(uid)
        else:
            assert False, repr(uid)

    def __hash__(self):
        return hash( self._m_layer_uuid )
        
    def __eq__(self,other):
        return (
            isinstance(other,self.__class__)
        and
            self._m_layer_uuid == other._m_layer_uuid
        )
        
    @property 
    def name(self):
        return self._m_layer_uuid[0]
        
    @property 
    def uuid(self):
        return self._m_layer_uuid[1]
        
    @property 
    def uid(self):
        "The M-layer identifier"
        return self._m_layer_uuid
        
    def json(self,**kwargs):
        obj = dict(
            __type__ = "UID",
            uid = str( list(self._m_layer_uuid) ) 
        )
        return json.dumps(obj,**kwargs)
        
    def __str__(self):
        return str(list(self._m_layer_uuid))
        
    def __repr__(self):
        return "UID( {} )".format(list(self._m_layer_uuid))
  
# ---------------------------------------------------------------------------
class CompoundUID(object):

    __slots__ = ('prefactor','factors')

    def __init__(self,stack):
    
        pops = normal_form(stack)

        # The keys in  pop.factors are Python objects.
        # Some may be distinct objects with the same M-layer UID.
        # In that case, each object occurs only once.    
        # The CompoundUID representation uses the M-layer UID as key 
        # and a forzenset of exponents as value. 
        
        setter = lambda factors,i,v: factors[ i.uid ].add(v)
        
        factors = defaultdict(set)
        for k,v in pops.factors.items():
            setter(factors,k,v)

        self.prefactor = pops.prefactor
        
        self.factors = {
            k : frozenset(v) 
                for k,v in factors.items()
        }

    def __contains__(self,item):
        return item in self.factors 
        
    def __eq__(self,other):
        return (
            isinstance(other,self.__class__)
        and
            # Mappings are equal if they have the same 
            # key-value pairs regardless of ordering
            # The frozenset values compare equal 
            # by membership, not ordering of elements.
            self.factors == other.factors
        and
            self.prefactor == other.prefactor
        )

    def __hash__(self):
        return hash( (
            tuple( self.factors.items() ),
            self.prefactor
        ) )
 
    def __str__(self):
        factors = ", ".join(
                "{} : {}".format(k if isinstance(k,UID) else fmt_key(k), list(v) 
            ) for k,v in self.factors.items() 
        ) 
        
        if self.prefactor != 1:
            return "{{ {} ,prefactor={}) }}".format(
                factors,
                self.prefactor
            )
        else:
            return "{{ {} }}".format(factors)
            
    def __repr__(self):
        factors = ", ".join(
                "{} : {}".format(k if isinstance(k,UID) else fmt_key(k), list(v) 
            ) for k,v in self.factors.items() 
        ) 
        
        if self.prefactor != 1:
            return "CompoundUID({{ {} }},prefactor={})".format(
                factors,
                self.prefactor
            )
        else:
            return "CompoundUID({})".format(factors)
        
        
    def json(self,**kwargs):
        """
        Return a JSON record for the CompoundUID
        
        Args:
            kwargs: will be passed directly to json.dumps
            
        """
        factors = {
            str(k) if isinstance(k,UID) else fmt_key(k) : list(v) 
                    for k,v in self.factors.items()
        }

        if self.prefactor != 1:
            if isinstance(self.prefactor,Fraction):
                prefactor = list( self.prefactor.as_integer_ratio() )
            else:
                prefactor = [ str(self.prefactor), "1" ]

            obj = dict(
                __type__ = "CompoundUID",
                factors = factors,
                prefactor = prefactor
            )
        else:
            obj = dict(
                __type__ = "CompoundUID",
                factors = factors
            )

        return json.dumps(obj,**kwargs)

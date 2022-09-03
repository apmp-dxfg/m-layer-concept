"""
A reference (unit) belonging to a coherent unit system has a dimensional  
signature that can be represented as a sequence of exponents referred to a 
corresponding sequence of base units. 

Multiplication and division of such units 
may be accompanied by addition (respectively subtraction) of the 
corresponding dimensional exponents, with raising to an integer power
understood as repeated multiplication or division. 

Coherent unit systems also have (incoherent) units that are multiples or 
submultiples of coherent units. So, given a system, the combination of a  
dimensional vector and a prefix is enough to identify a unit expressed as a 
product of powers of system base units.

"""
import numbers
import json
from collections import defaultdict

from m_layer.stack import normal_form

# ---------------------------------------------------------------------------
class ComposedDimension(object):

    __slots__ = ('prefactor','factors')

    def __init__(self,stack):
        pops = normal_form(stack)

        # The keys in pop.factors are Python objects.
        # Some may be distinct objects with the same M-layer UID.
        # In that case, each object occurs only once.    
        # The ComposedDimension representation uses the dimension as key 
        # and a frozenset of exponents as value. 
        
        setter = lambda factors,i,v: factors[ i.dimension ].add(v)
        
        factors = defaultdict(set)
        for k,v in pops.factors.items():
            setter(factors,k,v)

        self.prefactor = pops.prefactor
        
        self.factors = {
            k : frozenset(v) 
                for k,v in factors.items()
        }

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
        return hash( 
            tuple( self.factors.items() )
        +   ( self.prefactor, )
        )
 
    def __str__(self):
        factors = ", ".join(
            "{} : {}".format(k,list(v) )
                for k,v in self.factors.items()
        )
        return "{{ factors = {{ {} }}, prefactor = {} }}".format(
            factors,
            self.prefactor
        )

    def __repr__(self):
        factors = ", ".join(
            "{} : {}".format(k,list(v) )
                for k,v in self.factors.items()
        )
        return "ComposedDimension({{ {} }},prefactor={})".format(
            factors,
            self.prefactor
        )
        
    @property
    def json(self):
        factors = ", ".join(
            "{} : {}".format(k,list(v) )
                for k,v in self.factors.items()
        )
        obj = dict(
            __type__ = "ComposedDimension",
            factors = factors,
            prefactor = self.prefactor
        )
        return json.dumps(obj)
        
# ---------------------------------------------------------------------------
class Dimension(object):

    """
    Dimension(system,dim,prefix=1)
    """
    
    __slots__ = (
        '_system', '_dim', '_prefix'
    )
    
    def __init__(self,system,dim,prefix=1):
    
        self._system = system 
        self._dim = tuple(dim)
        self._prefix = prefix
        
    @property 
    def system(self):
        "The unit system"
        return self._system

    @property 
    def dim(self):
        return self._dim
        
    @property 
    def prefix(self):
        return self._prefix

    def __hash__(self):
        return hash( (
            self._system, 
            self._dim, 
            self._prefix
        ) )
        
    def __eq__(self,other):
        return (
            self.commensurate(other)
        and
            self.prefix == other.prefix
        )
 
    def commensurate(self,other):
        """
        ``True`` when this object and ``other`` 
        belong to the same system and have the 
        same dimensional exponents.
        
        """
        return (
            isinstance(other,Dimension)
        and
            self.system == other.system
        and 
            self.dim == other.dim
        )
      
    def __repr__(self):
        return "Dimension( {}, {}, prefix={} )".format(
            self.system,
            self.dim,
            self.prefix
        )
 
    def __str__(self):
        if self.prefix == 1:
            return "{}{}".format(
                self.system,
                self.dim
            )
        else:
            return "{}*{}{}".format(
                self.prefix,
                self.system,
                self.dim
            )
 
    def __rmul__(self,x):
        # a numerical scale factor 
        assert isinstance(x,numbers.Integral)
        return Dimension(
            self.system,
            self.dim,
            self.prefix * x
        )
        
    def __mul__(self,rhs):
            
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i + j for (i,j) in zip(self.dim,rhs.dim) ),
            self.prefix * rhs.prefix
        )
            
    
    def __truediv__(self,rhs):
    
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i - j for (i,j) in zip(self.dim,rhs.dim) ),
            self.prefix / rhs.prefix
        )
    
    def __pow__(self,n):
        if not isinstance(n,numbers.Integral):
            raise RuntimeError(
                "integer required '{!r}'".format(n)
            )
        return Dimension(
            self.system,
            tuple( n*i for i in self.dim ),
            self.prefix**n
        )
    
# ===========================================================================
if __name__ == '__main__':

    from m_layer import *
    from m_layer.system import System 
    
    si = System( ('si_system', 88156805987886421108624908988601219537) )
    d1 = Dimension(si,[1,2,3])
    d2 = Dimension(si,[1,-1,0])
    print(d1)

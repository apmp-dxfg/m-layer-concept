"""
A reference (unit) belonging to a coherent unit system has a dimensional  
signature that can be represented as a sequence of exponents referred 
to base units. 

Multiplication and division of scales may be recorded by addition (respectively  
subtraction) of the corresponding dimensional exponents, with raising to an 
integer power understood as repeated multiplication or division. 

Coherent unit systems also have (incoherent) units, which are multiples or 
submultiples of the coherent units. So, given a system, the combination of a  
dimensional vector and a prefix is enough to identify a unit expressed as a 
product of powers of system base units.

"""
import numbers

from collections import defaultdict
from collections import abc
from fractions import Fraction

from m_layer.stack import normal_form

# ---------------------------------------------------------------------------
class CompoundDimension(object):

    """
    A :class:`CompoundDimension` holds an expression 
    of :class:`Dimension` objects
    """

    __slots__ = ('prefactor','factors','_stack')

    def __init__(self,stack):
    
        self._stack = stack
        
        pops = normal_form(stack)

        # The keys in pop.factors are Python objects.
        # Some may be distinct objects with the same M-layer UID.
        # In that case, each object occurs only once.    
        # The CompoundDimension representation uses the dimension as key 
        # and a frozenset of exponents as value. 
        
        setter = lambda factors,i,v: (
            factors[ i.dimension ].add(v) if v != 0 else None
        )
        
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
        return hash( (
            self.factors.items(),
            self.prefactor
        ) )
 
    def __str__(self):
        factors = ", ".join(
            "{} : {}".format(k,list(v) )
                for k,v in self.factors.items()
        )
        if self.prefactor == 1:
            return "{{ {} }}".format(
                factors
            )
        else:
            return "{{ factors = {{ {} }}, prefactor = {} }}".format(
                factors,
                self.c
            )
        
    def __repr__(self):
        return "CompoundDimension({!r})".format(self._stack)
        
    @property
    def simplify(self):
        """
        Return the combination of the exponentiated factors
        
        """
        x = 1
        for k,v in self.factors.items():
            x *= k**sum(v)
            
        return x
 
    def commensurate(self,other):
        if isinstance(other,CompoundDimension):
            return self.simplify.commensurate(other.simplify)
        elif isinstance(other,Dimension):
            return self.simplify.commensurate(other)
        else:
            return NotImplementedError( repr(other) )
 
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
        self._prefix = Fraction( *prefix ) if isinstance(
            prefix,abc.Iterable) else Fraction( prefix )
        
    @property 
    def system(self):
        "The unit system"
        return self._system

    @property 
    def dim(self):
        "The tuple of dimensions"
        return self._dim
        
    @property 
    def prefix(self):
        "The numerical unit prefix"
        return self._prefix

    def __hash__(self):
        return hash( (
            self._system, 
            self._dim, 
            # Fraction(1,10) <=> Fraction(10,100), etc.
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
        if self.prefix == 1:
            return "Dimension( {}, {} )".format(
                self.system,
                self.dim
            )
        else:
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
            if self.prefix.numerator > 1E3 :
                prefix = "{:.0E}".format( float(self.prefix) )
            elif self.prefix.denominator > 1E3:
                prefix = "{:.0E}".format( float(self.prefix) )
            else:
                prefix = str(self.prefix)
                
            return "{}*{}{}".format(
                prefix,
                self.system,
                self.dim
            )
 
    def __rmul__(self,x):
        # a numerical scale factor 
        assert isinstance(x,numbers.Integral)
        return Dimension(
            self.system,
            self.dim,
            self.prefix
        )
        
    def __mul__(self,rhs):
            
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i + j for (i,j) in zip(self.dim,rhs.dim) ),
            self.prefix*rhs.prefix
        )
            
    
    def __truediv__(self,rhs):
    
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i - j for (i,j) in zip(self.dim,rhs.dim) ),
            self.prefix/rhs.prefix
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
    from m_layer.lib import System 
    
    si = System( ('si_system', 88156805987886421108624908988601219537) )
    d1 = Dimension(si,[1,2,3],prefix=[100,10])
    d2 = Dimension(si,[1,-1,0])
    print(d1)

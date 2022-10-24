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
class CompoundSystematic(object):

    """
    A :class:`CompoundSystematic` holds an expression 
    of :class:`Systematic` objects
    """

    __slots__ = ('prefactor','factors','_stack')

    def __init__(self,stack):
    
        self._stack = stack
        
        pops = normal_form(stack)

        # The keys in pop.factors are Python objects.
        # Some may be distinct objects with the same M-layer UID.
        # In that case, each object occurs only once.    
        # The CompoundSystematic representation uses the systematic as key 
        # and a frozenset of exponents as value. 
        
        setter = lambda factors,i,v: (
            factors[ i.systematic ].add(v) if v != 0 else None
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
        return "CompoundSystematic({!r})".format(self._stack)
        
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
        if isinstance(other,CompoundSystematic):
            return self.simplify.commensurate(other.simplify)
        elif isinstance(other,Systematic):
            return self.simplify.commensurate(other)
        else:
            return NotImplementedError( repr(other) )
 
# ---------------------------------------------------------------------------
# Systematic units in a unit system are products of powers of base units. 
# They encode the scaling represented by units,
# but do not identify a dimension (quantity). You can multiply 
# and divide systematic units to obtain other systematic units and 
# you can arithmetically simplify the results of such calculations. 
# Systematic units may be numeric multiples of submultiples of other
# systematic units.
#
# Different systematic units can be equivalent in terms of scaling. 
# For instance, kg/m <=> g/mm. 
# This class captures the unique scaling properties of a systematic unit.
# (So, it would not distinguish between kg/m and g/mm.)
#
# We can use the "system" and "dimensions" attributes of this class to 
# index an M-layer scale for the corresponding COHERENT systematic unit.
# We must restrict ourselves to a single M-layer ratio scale for
# each coherent unit expressed systematically, like m.s-2, kg.m2.s-2, etc. 
#
# This constraint can be checked in the registry because the JSON 
# record for a coherent unit has a "systematic" name (but no "prefix" data). 
#
# Note that the SI allows for different expressions of ONE coherent unit, 
# but it considers these to refer all to the same unit (SI9 p140). 
# This is difficult to make sense of. It seems that they consider only 
# scaling. Do they mean that when N.m is used for torque (a derived unit)  
# it is coherent and when it is used for energy (as a compound unit)
# it is not? You need to know the aspect to make that distinction.
# Of course, N.m doesn't take a prefix in either case, nor would 
# other permutations of the unit names. So, in terms of scaling 
# they are all equivalent.
# 
# In this project, the joule is distinct from an (arbitrary)  
# compound unit N.m. There is also a reference si_N.m,
# which can be used to represent torque. 
#
class Systematic(object):

    """
    Systematic(system,dim,prefix=1)
    """
    
    __slots__ = (
        '_system', '_dim', '_prefix'
    )
    
    def __init__(self,system,dim,prefix=None):
    
        self._system = system 
        self._dim = tuple(dim)
        
        if prefix is None:
            self._prefix = 1
        elif isinstance(prefix,abc.Iterable):
            self._prefix = Fraction( *prefix )
        else:
            self._prefix = Fraction( prefix )
        
    @property 
    def system(self):
        "The unit system"
        return self._system

    @property
    def simplify(self):
        return self

    @property 
    def dimensions(self):
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
            isinstance(other,Systematic)
        and
            self.system == other.system
        and 
            self.dimensions == other.dimensions
        )
      
    def __repr__(self):
        if self.prefix == 1:
            return "Systematic( {}, {} )".format(
                self.system,
                self.dimensions
            )
        else:
            return "Systematic( {}, {}, prefix={} )".format(
                self.system,
                self.dimensions,
                self.prefix
            )
 
    def __str__(self):
        if self.prefix == 1:
            return "{}{}".format(
                self.system,
                self.dimensions
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
                self.dimensions
            )
 
    def __rmul__(self,x):
        # a numerical scale factor 
        assert isinstance(x,numbers.Integral)
        return Systematic(
            self.system,
            self.dimensions,
            self.prefix
        )
        
    def __mul__(self,rhs):
            
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Systematic(
            self.system,
            tuple( i + j for (i,j) in zip(
                self.dimensions,rhs.dimensions) ),
            self.prefix*rhs.prefix
        )
            
    
    def __truediv__(self,rhs):
    
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Systematic(
            self.system,
            tuple( i - j for (i,j) in zip(
                self.dimensions,rhs.dimensions) ),
            self.prefix/rhs.prefix
        )
    
    def __pow__(self,n):
        if not isinstance(n,numbers.Integral):
            raise RuntimeError(
                "integer required '{!r}'".format(n)
            )
        return Systematic(
            self.system,
            tuple( n*i for i in self.dimensions ),
            self.prefix**n
        )
    
# ===========================================================================
if __name__ == '__main__':

    from m_layer import *
    from m_layer.lib import System 
    
    si = System( ('si_system', 88156805987886421108624908988601219537) )
    d1 = Systematic(si,[1,2,3],prefix=[100,10])
    d2 = Systematic(si,[1,-1,0])
    print(d1)

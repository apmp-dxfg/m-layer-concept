"""
A reference (unit) that belongs to a coherent unit system has a dimensional  
signature which can be represented as a sequence of exponents referred to a 
corresponding sequence of base units. 

Multiplication and division of quantities expressed in such units 
may be accompanied by addition (respectively subtraction) of the 
corresponding dimensional exponents, with raising to an integer power
understood as repeated multiplication or division. 

Coherent units systems also have (incoherent) units that are multiples or 
submultiples of coherent units. So, the combination of a dimensional 
vector and a prefix is enough to identify a unit expressed as a product
of powers of system base units.

"""
import numbers

class Dimension(object):

    """
    Dimension(system,dim,prefix=1)
    """
    
    __slots__ = (
        '_system', '_dim', '_prefix'
    )
    
    def __init__(self,system,dim,prefix=1):
    
        self._system = system 
        self._dim = tuple( dim )
        self._prefix = prefix
        
    @property 
    def system(self):
        return self._system

    @property 
    def dim(self):
        return self._dim
        
    @property 
    def prefix(self):
        return self._prefix

    def __eq__(self,other):
        return (
            self.commensurate(other)
        and
            self.prefix == other.prefix
        )
 
    def commensurate(self,other):
        """
        Return ``True`` when this object and ``other`` have the 
        same system and dimensions.
        
        """
        return (
            isinstance(other,Dimension)
        and
            self.system == other.system
        and 
            self.dim == other.dim
        )
      
    def __repr__(self):
        return "Dimension( {!s}, {!s}, prefix={!s} )".format(
            self.system,
            self.dim,
            self.prefix
        )
 
    def __str__(self):
        if self.prefix == 1:
            return "{!s}{!s}".format(
                self.system,
                self.dim
            )
        else:
            return "{!s}*{!s}{!s}".format(
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
    
    si = System( ('si-system', 88156805987886421108624908988601219537) )
    d1 = Dimension(si,[1,2,3])
    d2 = Dimension(si,[1,-1,0])
    print(d1**4.7)

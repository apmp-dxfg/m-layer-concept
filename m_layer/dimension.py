"""
A reference (unit) that belongs to a unit system has a dimensional signature 
that can be represented as a sequence of exponents referred to a 
corresponding sequence of base units. 

Multiplication and division of quantities expressed in such units 
is accompanied by addition ()respectively subtraction) of the 
corresponding dimensional exponents, with raising to an ingeger power
understood as repeated multiplication or division. 

"""
import numbers

class Dimension(object):

    __slots__ = (
        '_system', '_dim'
    )
    
    def __init__(self,system,dim):
    
        self._system = system 
        self._dim = tuple( dim )
        
    @property 
    def system(self):
        return self._system

    @property 
    def dim(self):
        return self._dim
        
    def __eq__(self,other):
        return (
            isinstance(other,Dimension)
        and
            self.system == other.system
        and 
            self.dim == other.dim
        )
        
    def __repr__(self):
        return "Dimension( {!s}{!s} )".format(
            self.system,
            self.dim
        )
 
    def __str__(self):
        return "{!s}{!s}".format(
            self.system,
            self.dim
        )
 
    def __mul__(self,rhs):
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i + j for (i,j) in zip(self.dim,rhs.dim) )
        )
    
    def __truediv__(self,rhs):
        assert self.system == rhs.system,\
            "different systems: '{}', '{}'".format(self.system, rhs.system)
            
        return Dimension(
            self.system,
            tuple( i - j for (i,j) in zip(self.dim,rhs.dim) )
        )
    
    def __pow__(self,n):
        if not isinstance(n,numbers.Integral):
            raise RuntimeError(
                "integer required '{!r}'".format(n)
            )
        return Dimension(
            self.system,
            tuple( n*i for i in self.dim )
        )
    
# ===========================================================================
if __name__ == '__main__':

    from m_layer import *
    from m_layer.system import System 
    
    si = System( ('si-system', 88156805987886421108624908988601219537) )
    d1 = Dimension(si,[1,2,3])
    d2 = Dimension(si,[1,-1,0])
    print(d1**4.7)

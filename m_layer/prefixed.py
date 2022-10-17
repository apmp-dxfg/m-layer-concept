"""


"""
import numbers

from collections import defaultdict
from collections import abc
from fractions import Fraction

from m_layer.stack import normal_form

# ---------------------------------------------------------------------------
class Prefixed(object):

    """
    Prefixed(reference,prefix)
    """
    
    __slots__ = (
        '_reference', ''_prefix'
    )
    
    def __init__(self,reference,prefix):
    
        self._reference = reference 
        
        if isinstance(prefix,abc.Iterable):
            self._prefix = Fraction( *prefix )
        else:
            self._prefix = Fraction( prefix )
                
    @property 
    def prefix(self):
        "The numerical unit prefix"
        return self._prefix

    def __hash__(self):
        return hash( (
            self._reference, 
            self._prefix   
        ) )
        
    def __eq__(self,other):
        return (
            isinstance(other,Prefixed)
        and
            self._reference == other._reference
        and
            self.prefix == other.prefix
        )
 
    def __repr__(self):
        return "Prefixed( {}, {} )".format(
            self._reference,
            self.prefix
        )
 
    def __str__(self):
        if self.prefix.numerator > 1E3 :
            prefix = "{:.0E}".format( float(self.prefix) )
        elif self.prefix.denominator > 1E3:
            prefix = "{:.0E}".format( float(self.prefix) )
        else:
            prefix = str(self.prefix)
            
        return "{}*{}".format(
            prefix,
            self._reference
        )
 
    
# ===========================================================================
if __name__ == '__main__':

    from m_layer import *

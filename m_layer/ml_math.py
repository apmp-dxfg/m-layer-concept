"""
The functions exported from this module are used during parsing of JSON strings that define mathematical transformations. 
 
"""
__all__ = (
    'bounded_convert',
    'interval_convert',
    'ratio_convert',
    'Fraction',
)
from fractions import Fraction

# This will import uncertain-number math functions when they are available in the system
# otherwise the regular math library is imported
try: 
    import GTC as math
    
    # TODO: when GTC gets an implementation of fmod, use that 
    import math as py_math    
    def fmod(x,y):
        value = math.value(x)
        return py_math.fmod(value,y) + (x - value)
        
    math.fmod = fmod 
    
except ImportError:
    import math

# ---------------------------------------------------------------------------
def bounded_convert(x,a,y_lb,y_ub):
    """
    Convert ``x`` to a bounded interval scale
    
    Args:
        x : the value to be converted 
        a : the scaling factor for divisions 
        y_lb : the lower limit of the destination scale
        y_ub : the upper limit of the destination scale
        
    Returns:
        A value corresponding to ``x`` on the destination scale 
        
    .. Note: 
    
        Untested assumptions are that ``y_ub - y_lb > 0`` and ``a > 0``
    
    """
    z = math.fmod(a*x - y_lb, y_ub - y_lb) 
    return z + y_ub if z < 0.0 else z + y_lb  
 
# ---------------------------------------------------------------------------
def interval_convert(x,a,b):
    """
    Convert ``x`` to an interval scale

    Args:
        x : the value to be converted 
        a : the scaling factor for divisions 
        b : the scale offset
        
    Returns:
        A value corresponding to ``x`` on the destination scale 
        
    .. Note: 
    
        An untested assumption is that ``a > 0``

    """
    return a*x + b
   
# ---------------------------------------------------------------------------
def ratio_convert(x,a):
    """
    Convert ``x`` to an ratio scale

    Args:
        x : the value to be converted 
        a : the scaling factor for divisions 
        
    Returns:
        A value corresponding to ``x`` on the destination scale 
        
    .. Note: 
    
        An untested assumption is that ``a > 0``

    """
    return a*x
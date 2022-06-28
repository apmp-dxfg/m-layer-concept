# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import default_context as cxt

__all__ = (
    'Expression', 'XP'
)
  
# ---------------------------------------------------------------------------
class Expression(object):
    
    """
    An `Expression` is defined by a value, a scale and an aspect. 
    """
    
    __slots__ = ("_value","_scale","_aspect")
    
    def __init__(self,value,scale,aspect=None):
        self._value = value 
        self._scale = scale
        self._aspect = aspect
        
    def __str__(self):
        short=True
        locale=cxt.locale       
        
        return "{} {}".format( 
            self.value(), 
            self._scale._json_scale_to_ref(locale,short) 
        )
        
    def __repr__(self):
        locale=cxt.locale
        short=False
        
        v = "{}".format( self.value() )
        r = "{}".format( self._scale._json_scale_to_ref(locale,short) )
        
        if self._aspect is None:
            return "Expression({},{})".format(v,r)
        else:
            a = "{}".format( self._aspect._from_json(locale,short) )
            return "Expression({},{},{})".format(v,r,a)
        
    def value(self):
        """
        Return the value 
        
        """
        return cxt.value_fmt.format(self._value)


    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """
        Return a new `Expression` in terms of the scale provided
        
        """
        fn = cxt.conversion_fn( self, dst_scale )
 
        return Expression(
            fn( self._value ),
            dst_scale,
            self._aspect
        )

    # ---------------------------------------------------------------------------
    def cast(self,dst_scale,dst_aspect=None):
        """
        Return a new `Expression` in terms of the aspect and scale provided

        If the argument `dst_aspect` is not specified it
        will default to be the same aspect as `self`.
                
        """
        if self._aspect is None:
            raise RuntimeError(
                "{!r} has no declared aspect, so it cannot be cast".format(self)
            )

        # No destination aspect => reuse the object's aspect
        if dst_aspect is None: 
            dst_aspect = self._aspect
        
        fn = cxt.casting_fn(self, (dst_scale, dst_aspect) )
        
        return Expression(
            fn( self._value ),
            dst_scale,
            dst_aspect
        )

XP = Expression


# ===========================================================================
if __name__ == '__main__':
    
    pass

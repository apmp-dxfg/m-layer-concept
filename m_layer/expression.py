# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import context

cxt = context.default_context

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
        return "{} {}".format( 
            self.value(), 
            self.ref(locale=cxt.locale) 
        )
        
    def __repr__(self):
        v = "{}".format( self.value() )
        r = "{}".format( self.ref(locale=cxt.locale,short=False) )
        
        if self._aspect is None:
            return "Expression({},{})".format(v,r)
        else:
            a = "{}".format( self.aspect(locale=cxt.locale), short=False )
            return "Expression({},{},{})".format(v,r,a)
        
    def value(self):
        """
        Return the value 
        
        """
        return cxt.value_fmt.format(self._value)
       
    def ref(self,locale=None,short=True):
        """
        Return the unit (or reference) as a string 
        
        """
        scale_json = cxt.scale_reg[self._scale] 
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 
        
        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 

        return ref_uid['locale'][locale][locale_key]

    def aspect(self,locale=None,short=False):
        """
        Return the aspect as a string 
        
        """
        if self._aspect is not None:
            aspect_json = cxt.aspect_reg[self._aspect] 

            locale_key = 'symbol' if short else 'name'
            if locale is None: locale = cxt.locale 
                
            return aspect_json['locale'][locale][locale_key]
        else:
            return ""


    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """
        Return a new `Expression` in terms of the scale provided
        
        """
        fn = cxt.conversion_fn(self,dst_scale) 
 
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

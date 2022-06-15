# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import context

cxt = context.default_context

__all__ = (
    'Expression', 'XP'
)

# ---------------------------------------------------------------------------
class Expression(object):
    
    """
    An `Expression` is defined by an aspect, a value and a scale. 
    """
    
    # Notation distinguishes between an M-Layer reference ('ml_ref'), which 
    # includes information about the scale type, and a conventional reference.
    __slots__ = ("_value","_ml_ref","_aspect")
    
    def __init__(self,aspect,value,ref):
        self._value = value 
        self._aspect = aspect
        self._ml_ref = ref
        
    def __str__(self):
        return "{} {}".format( 
            self.value(), 
            self.ref(locale=cxt.locale) 
        )
        
    def __repr__(self):
        a = "{}".format( self.aspect(locale=cxt.locale), short=False )
        v = "{}".format( self.value() )
        r = "{}".format( self.ref(locale=cxt.locale,short=False) )
        
        return "Expression({},{},{})".format(a,v,r)
        
    def value(self):
        """
        Return the value 
        
        """
        return cxt.value_fmt.format(self._value)
       
    def ref(self,locale=None,short=True):
        """
        Return the unit (or reference) as a string 
        
        """
        scale_json = cxt.scale_reg[self._ml_ref] 
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 
        
        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 

        return ref_uid['locale'][locale][locale_key]

    def aspect(self,locale=None,short=False):
        """
        Return the aspect as a string 
        
        """
        aspect_json = cxt.aspect_reg[self._aspect] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return aspect_json['locale'][locale][locale_key]


    # ---------------------------------------------------------------------------
    def convert(self,ml_ref):
        """
        Return a new `Expression` in terms of the scale provided
        
        Conversion does not change the aspect or the type of scale
        
        """
        if ml_ref in cxt.scales_for_aspect_reg[self._aspect]:
            
            fn = cxt.conversion_fn(self,ml_ref)
            return Expression(
                self._aspect,
                fn( self._value ),
                ml_ref
            )
        else: 
            raise RuntimeError(
                "cannot convert {!r} to {!r}".format(self._ml_ref,ml_ref)
            )

    # ---------------------------------------------------------------------------
    def cast(self,aspect_dst,scale_dst):
        """
        Return a new `Expression` in terms of the aspect and scale provided
        
        """
        dst = (aspect_dst,scale_dst) 
        
        fn = cxt.casting_fn(self,dst)
        
        return Expression(
            aspect_dst,
            fn( self._value ),
            scale_dst
        )

XP = Expression


# ===========================================================================
if __name__ == '__main__':
    
    pass

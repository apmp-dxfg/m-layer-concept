# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import context

cxt = context.default_context

__all__ = (
    'AspectValue', 'AV'
)

# ---------------------------------------------------------------------------
class AspectValue(object):
    
    """
    An `AspectValue` combines an aspect, a value and an M-Layer scale. 
    Only UIDs for the aspect and scale are stored. Corresponding details
    are accessed in a `Context` using these UIDs.
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
        
        return "AspectValue({},{},{})".format(a,v,r)
        
    # These methods render information 
    def value(self):
        return cxt.value_fmt.format(self._value)
       
    def ref(self,locale=None,short=True):
        scale_json = cxt.scale_reg[self._ml_ref] 
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 
        
        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 

        return ref_uid['locale'][locale][locale_key]

    def aspect(self,locale=None,short=False):
        aspect_json = cxt.aspect_reg[self._aspect] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return aspect_json['locale'][locale][locale_key]


    # ---------------------------------------------------------------------------
    def convert(self,ml_ref):
        """
        Convert `av` to an expression in terms of `ml_ref`
        """
        # `ml_ref` is the ID for an M-Layer extended scale 
        
        if ml_ref in cxt.scales_for_aspect_reg[self._aspect]:
            
            fn = cxt.conversion_fn(self,ml_ref)
            return AV(
                self._aspect,
                fn( self._value ),
                ml_ref
            )
        else: 
            raise RuntimeError(
                "cannot convert {} to {}".format(self._ml_ref,ml_ref)
            )

AV = AspectValue


# ===========================================================================
if __name__ == '__main__':
    
    pass

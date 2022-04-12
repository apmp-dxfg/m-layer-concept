# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import context

cxt = context.default_context

__all__ = (
    'AspectValue', 'AV', 'convert'
)

# ---------------------------------------------------------------------------
class AspectValue(object):
    """
    """
    # Notation distinguishes between an M-layer reference ('ml_ref'), which 
    # includes information about the scale type, and a conventional reference.
    __slots__ = ("_value","_ml_ref","_aspect")
    
    def __init__(self,aspect,value,ref):
        self._value = value 
        self._aspect = aspect
        self._ml_ref = ref
        
    def __str__(self):
        return "{} {}".format( 
            self.value, 
            self.ref(locale=cxt.locale) 
        )
        
    def __repr__(self):
        a = "{}".format( self.aspect(locale=cxt.locale),short=False )
        v = "{}".format( self.value )
        r = "{}".format( self.ref(locale=cxt.locale,short=False) )
        
        return "AspectValue({},{},{})".format(a,v,r)
        
    # These methods render information 
    @property
    def value(self):
        return self._value 
       
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

AV = AspectValue

# ---------------------------------------------------------------------------
def convert(av,ml_ref):
    """
    Convert `av` to an expression in terms of `ml_ref`
    """
    # `ml_ref` is the ID for an M-Layer extended scale 
    fn = cxt.conversion_fn(av,ml_ref)
    return AV(
        av._aspect,
        fn(av.value),
        ml_ref
    )
    

# ===========================================================================
if __name__ == '__main__':
    
    pass

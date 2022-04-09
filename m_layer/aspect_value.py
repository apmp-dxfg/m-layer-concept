# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import context
import m_layer

cxt = context.default_context

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
        return "{} {}".format( self.value, self.ref() )
        
    # These methods render information about the aspect value.
    @property
    def value(self):
        return self._value 
       
    def ref(self,locale=None,short=True):
        scale_json = cxt.scale_reg[self._ml_ref] 
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 
        
        if short:
            return ref_uid['locale'][cxt.locale]['symbol']
        else:
            return ref_uid['locale'][cxt.locale]['name']

    def aspect(self,locale=None,short=False):
        aspect_json = cxt.aspect_reg[self._aspect] 

        if short:
            return aspect_json['locale'][cxt.locale]['symbol']
        else:
            return aspect_json['locale'][cxt.locale]['name']

AV = AspectValue

# ---------------------------------------------------------------------------
def convert(src_av,dst_ml_ref_id):
    """
    """
    fn = cxt.conversion_fn(src_av,dst_ml_ref_id)
    return AV(src_av._aspect,fn(src_av.value),dst_ml_ref_id)
    
# ===========================================================================
if __name__ == '__main__':
    
    from m_layer import aspect
    from m_layer import si_unit 
    from m_layer import imperial_unit 
    
    x = AV(aspect.mass,12,si_unit.kg)
    print(x)
    print( "{}: {} {}".format( x.aspect(), x.value, x.ref() ) )

    y = convert(x,imperial_unit.lb)
    print( "{}: {} {}".format( y.aspect(), y.value, y.ref() ) )
    


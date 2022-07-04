from m_layer.context import default_context as cxt
from m_layer.scale_aspect import ScaleAspect

__all__ = ('Scale','to_scale_aspect',)

# ---------------------------------------------------------------------------
class Scale(object):

    """
    Lightweight wrapper around the unique identifier for 
    an M-layer scale.  
    """

    __slots__ = (
        '_scale_uid',
    )
    
    def __init__(self,scale_uid):    
        self._scale_uid = scale_uid

    def _from_json(self):
        return cxt.scale_reg[self._scale_uid] 

    def _json_scale_to_ref(self,locale=None,short=False):
    
        scale_json = self._from_json()
        ref_uid = cxt.reference_reg[ tuple(scale_json['reference']) ] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return ref_uid['locale'][locale][locale_key]
        
    @property 
    def uid(self):
        "The M-layer identifier for this aspect"
        return self._scale_uid
        
    def __eq__(self,other):
        "True when both objects have the same uids"
        return self.uid[1] == other.uid[1] 
        
    def __str__(self):
        return str( self._from_json() )
        
    def __repr__(self):
        return "Scale({!r})".format( self.uid )

    def to_scale_aspect(self,aspect=None):
        """Return a :class:`~scale_aspect.ScaleAspect` object 
        with the same scale and aspect ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 
         
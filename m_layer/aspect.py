from m_layer.context import default_context as cxt

# ---------------------------------------------------------------------------
class Aspect(object):

    """
    Lightweight wrapper around the unique identifier for 
    an M-layer aspect.  
    """

    __slots__ = (
        '_aspect_uid',
    )
    
    def __init__(self,aspect_uid):    
        self._aspect_uid = aspect_uid

    def _from_json(self,locale=None,short=False):
        aspect_json = cxt.aspect_reg[self._aspect_uid] 

        locale_key = 'symbol' if short else 'name'
        if locale is None: locale = cxt.locale 
            
        return aspect_json['locale'][locale][locale_key]

    @property 
    def uid(self):
        "The M-layer identifier for this aspect"
        return self._aspect_uid
        
    def __eq__(self,other):
        "True when both objects have the same uids"
        return self.uid[1] == other.uid[1] 
        
    def __str__(self):
        return str( self._from_json() )
        
    def __repr__(self):
        if self.uid is None:
            return ""
        else:
            return "Aspect{!r}".format( self.uid )

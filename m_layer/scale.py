"""

"""
from m_layer.context import default_context as cxt
from m_layer.aspect import no_aspect

__all__ = (
    'Scale',
    'ScaleAspect',
)

# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A wrapper around a scale-aspect pair
    Objects are immutable.
    """

    __slots__ = ("_scale","_aspect")

    def __init__(self,scale,aspect=no_aspect):
        self._scale = scale
        self._aspect = aspect

    @property
    def scale(self):
        "The scale"
        return self._scale 
        
    @property 
    def aspect(self):
        "The aspect or kind of quantity"
        return self._aspect
            
    # Alias
    kind_of_quantity = aspect 

    @property 
    def uid(self):
        "A pair of M-layer identifiers for scale and aspect"
        return (self.scale.uid,self.aspect.uid)
        
    def __eq__(self,other):
        "True when the M-layer identifiers of both objects match"
        return (
            self.scale == other.scale
        and self.aspect == other.aspect
        )
        
    def __str__(self):
        return "({!s}, {!s})".format(self.scale,self.aspect)
        
    def __repr__(self):
        return "ScaleAspect({!r},{!r})".format( self.scale,self.aspect ) 
         
    # def to_scale_aspect(self,aspect):
        # """
        # This matches a method in :class:`Scale`, which 
        # creates ``ScaleAspect`` objects. It will have no effect, 
        # unless there is an attempt to change the aspect.

        # """ 
        # if self._aspect != aspect:
            # raise RuntimeError(
                # "cannot change the aspect of a ScaleAspect"
            # )
            
        # return self
        
# ---------------------------------------------------------------------------
class Scale(object):

    """
    Scale objects provide a lightweight wrapper around the 
    unique identifier for an M-layer scale.  
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

    def to_scale_aspect(self,aspect=no_aspect):
        """
        Return a :class:`~scale_aspect.ScaleAspect` object 
        combining this scale and ``aspect``.
        
        """
        return ScaleAspect(self,aspect) 
         
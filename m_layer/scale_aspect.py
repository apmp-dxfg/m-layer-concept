__all__ = (
    'ScaleAspect', 
) 

# ---------------------------------------------------------------------------
class ScaleAspect(object):

    """
    A scale-aspect pair 
    """

    __slots__ = ("_scale","_aspect")

    def __init__(self,scale,aspect=None):
        self._scale = scale
        self._aspect = aspect

    @property
    def scale(self):
        return self._scale 
        
    @property 
    def aspect(self):
        return self._aspect
            
    # Alias
    kind_of_quantity = aspect 

    @property 
    def uid(self):
        return (self.scale.uid,self.aspect.uid)
        
    def __eq__(self,other):
        return (
            self.scale == other.scale
        and self.aspect == other.aspect
        )
        
    def __str__(self):
        return "({!s}, {!s})".format(self.scale,self.aspect)
        
    def __repr__(self):
        return "ScaleAspect({!r},{!r})".format( self.scale,self.aspect ) 
         
    def to_scale_aspect(self):
        return self
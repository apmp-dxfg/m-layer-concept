# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import default_context as cxt

__all__ = (
    'Expression', 
    'token', 'value',
    'convert', 
    'cast',
    'aspect', 'kind_of_quantity',
    'scale',
    'scale_aspect',
)


# ---------------------------------------------------------------------------
class Expression(object):
    
    """
    An ``Expression`` is defined by a token and a scale. 
    A third component called aspect may also be specified.
    """
    
    __slots__ = ("_token","_scale_aspect")
    
    def __init__(self,token,scale_aspect):
        self._token = token 
        self._scale_aspect = scale_aspect
         
    @staticmethod
    def from_scale(token,scale):
        return Expression( 
            token,
            scale.to_scale_aspect(None) 
        ) 
 
    @staticmethod
    def from_scale_aspect(token,scale,aspect):
        return Expression(
            token,
            scale.to_scale_aspect(aspect)
        ) 
 
    def __str__(self):
        short=True
        locale=cxt.locale       
        
        return "{} {}".format( 
            self._token, 
            self._scale_aspect.scale._json_scale_to_ref(locale,short) 
        )
        
    def __repr__(self):
        locale=cxt.locale
        short=False
        
        v = "{}".format( self.token )
        r = "{}".format( self._scale_aspect.scale._json_scale_to_ref(locale,short) )
        
        if self.aspect is None:
            return "Expression({},{})".format(v,r)
        else:
            a = "{}".format( self.aspect._from_json(locale,short) )
            return "Expression({},{},{})".format(v,r,a)
            
    @property
    def token(self):
        return self._token

    # Alias
    # In future it may be sensible to define a subclass of Expression 
    # for (the majority of) cases where the tokens are real numbers 
    value = token 
 
    @property 
    def scale(self):
        return self._scale_aspect.scale 
 
    @property 
    def aspect(self):
        return self._scale_aspect.aspect 
        
    # Alias
    # See also the comment for ``value`` above     
    kind_of_quantity = aspect 
 
    @property 
    def scale_aspect(self):
        return self._scale_aspect
        
 
    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """
        Return a new ``Expression`` in terms of the scale provided
        
        """
        if hasattr(dst_scale,'aspect'):
            # treat as a ScaleAspect 
            dst_scale = dst_scale.scale 
            
        dst_scale_aspect = dst_scale.to_scale_aspect()
        
        fn = cxt.conversion_fn( self, dst_scale )
 
        return Expression(
            fn( self._token ),
            dst_scale.to_scale_aspect(self._scale_aspect.aspect)
        )

    # ---------------------------------------------------------------------------
    def cast(self,dst_scale_aspect):
        """
        Return a new ``Expression`` in terms of the aspect and scale provided

        If the argument ``dst_aspect`` is not specified the aspect of the 
        new expression will be the same as ``self``.
                
        """
        # `dst_scale_aspect` could be a Scale or a ScaleAspect
        dst_scale_aspect = dst_scale_aspect.to_scale_aspect()
        
        if self._scale_aspect.aspect is None:
            raise RuntimeError(
                "{!r} has no declared aspect, so it cannot be cast".format(self)
            )

        # No destination aspect => reuse the object's aspect
        if dst_scale_aspect.aspect is None: 
            dst_scale_aspect = dst_scale_aspect.scale.to_scale_aspect(
                self._scale_aspect.aspect
            )

        fn = cxt.casting_fn(self, dst_scale_aspect )
        
        return Expression(
            fn( self._token ),
            dst_scale_aspect
        )

XP = Expression

# ---------------------------------------------------------------------------
# Unbound functions and aliases corresponding to ``Expression`` operations
#
def token(xp):
    return xp.token

value = token

def convert(xp,dst_scale):
    return xp.convert(dst_scale)
    
def cast(xp,dst_scale_aspect):
    return xp.cast(dst_scale_aspect)
    
def aspect(xp):
    return xp.aspect 
    
kind_of_quantity = aspect
    
def scale(xp):
    return xp.scale 

def scale_aspect(xp):
    return xp.scale_aspect 
   
def expression():
    """
    """
# ===========================================================================
if __name__ == '__main__':
    
    pass

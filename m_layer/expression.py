# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer import default_context as cxt

__all__ = (
    'Expression', 'XP',
    'token', 'value',
    'convert', 
    'cast',
    'aspect', 'kind_of_quantity',
    'scale',
)
  
# ---------------------------------------------------------------------------
class Expression(object):
    
    """
    An ``Expression`` is defined by a token and a scale. 
    A third component called aspect may also be specified.
    """
    
    __slots__ = ("_token","_scale","_aspect")
    
    def __init__(self,token,scale,aspect=None):
        self._token = token 
        self._scale = scale
        self._aspect = aspect
        
    def __str__(self):
        short=True
        locale=cxt.locale       
        
        return "{} {}".format( 
            self._token, 
            self._scale._json_scale_to_ref(locale,short) 
        )
        
    def __repr__(self):
        locale=cxt.locale
        short=False
        
        v = "{}".format( self.token )
        r = "{}".format( self._scale._json_scale_to_ref(locale,short) )
        
        if self._aspect is None:
            return "Expression({},{})".format(v,r)
        else:
            a = "{}".format( self._aspect._from_json(locale,short) )
            return "Expression({},{},{})".format(v,r,a)
    @property
    def token(self):
        return self._token

    @property
    def scale(self):
        return self._scale 
        
    @property 
    def aspect(self):
        return self._aspect

    # Alias
    # In future it may be sensible to define a subclass of Expression 
    # for (the majority of) cases where the tokens are real numbers 
    value = token 
 
    @property 
    def scale(self):
        return self._scale 
 
    @property 
    def aspect(self):
        return self._aspect 
        
    # Alias
    # See also the comment for ``value`` above     
    kind_of_quantity = aspect 
    
    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """
        Return a new ``Expression`` in terms of the scale provided
        
        """
        fn = cxt.conversion_fn( self, dst_scale )
 
        return Expression(
            fn( self._token ),
            dst_scale,
            self._aspect
        )

    # ---------------------------------------------------------------------------
    def cast(self,dst_scale,dst_aspect=None):
        """
        Return a new ``Expression`` in terms of the aspect and scale provided

        If the argument ``dst_aspect`` is not specified the aspect of the 
        new expression will be the same as ``self``.
                
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
            fn( self._token ),
            dst_scale,
            dst_aspect
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
    
def cast(xp,dst_scale,dst_aspect=None):
    return xp.cast(dst_scale,dst_aspect)
    
def aspect(xp):
    return xp.aspect 
    
kind_of_quantity = aspect
    
def scale(xp):
    return xp.scale 
    
# ===========================================================================
if __name__ == '__main__':
    
    pass

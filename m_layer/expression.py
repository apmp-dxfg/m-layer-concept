# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer.context import default_context as cxt
from m_layer.scale_aspect import ScaleAspect
from m_layer.scale import Scale

__all__ = (
    'expr', 
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
        """Return a new M-layer expression in the scale ``dst_scale``
        
        The aspect of ``xp`` will be used for the new expression
        if ``dst_scale`` is an :class:`~scale.Scale` object
        or an :class:`~scale_aspect.ScaleAspect` object with 
        no defined aspect.
        
        Args:
            xp (:class:`~expression.Expression`) : the expression to be converted    
            dst_scale (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 
        
        Returns:
            :class:`~expression.Expression` 

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
        """Return a new M-layer expression in the scale-aspect ``dst_scale_aspect``
            
        The aspect of ``xp`` will be used for the new expression
        if ``dst_scale_aspect`` is has no defined aspect.

        Args:
            xp (:class:`~expression.Expression`): the expression to be converted
            dst_scale_aspect (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 

        Returns:
            an  M-layer :class:`~expression.Expression` 

        Raises:
            RuntimeError: if no aspect is specified by ``xp`` 
            
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

# ---------------------------------------------------------------------------
# Unbound functions and aliases corresponding to ``Expression`` operations
#
def token(xp):
    return xp.token

value = token

def convert(xp,dst_scale):
    """Return a new M-layer expression in the scale ``dst_scale``
    
    The aspect of ``xp`` will be used for the new expression
    if ``dst_scale`` is an :class:`~scale.Scale` object
    or an :class:`~scale_aspect.ScaleAspect` object with 
    no defined aspect.
    
    Args:
        xp (:class:`~expression.Expression`) : the expression to be converted    
        dst_scale (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 
    
    Returns:
        :class:`~expression.Expression` 

    """        
    return xp.convert(dst_scale)
    
def cast(xp,dst_scale_aspect):
    """Return a new M-layer expression in the scale-aspect ``dst_scale_aspect``
            
    The aspect of ``xp`` will be used for the new expression
    if ``dst_scale_aspect`` is has no defined aspect.

    Args:
        xp (:class:`~expression.Expression`): the expression to be converted
        dst_scale_aspect (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 

    Returns:
        an  M-layer :class:`~expression.Expression` 

    Raises:
        RuntimeError: if no aspect is specified by ``xp`` 
        
    """
    return xp.cast(dst_scale_aspect)
    
def aspect(xp):
    return xp.aspect 
    
kind_of_quantity = aspect
    
def scale(xp):
    return xp.scale 

def scale_aspect(xp):
    return xp.scale_aspect 
  
# ---------------------------------------------------------------------------
# For the API 
#   
def expr(v,s,a=None):
    """Returns an M-layer expression 
    
    Args:
        v: the value or token of the expression 
        s(:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): 
        the scale-aspect pair for the expression 
        a(:class:`~aspect.Aspect`, optional) the aspect fro the expression
    Returns:
        an  M-layer :class:`~expression.Expression`  
    
    """
    # `s` may be a scale-aspect pair or just a scale 
    if isinstance(s,ScaleAspect):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, s.to_scale_aspect(a) )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        
# ===========================================================================
if __name__ == '__main__':
    
    pass

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from m_layer.context import default_context as cxt
from m_layer.scale import Scale, ScaleAspect
from m_layer.aspect import no_aspect

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
    An ``Expression`` is defined by a token and a scale-aspect. 
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
        
        if self.aspect is no_aspect:
            return "Expression({},{})".format(v,r)
        else:
            a = "{}".format( self.aspect._from_json(locale,short) )
            return "Expression({},{},{})".format(v,r,a)
            
    @property
    def token(self):
        "The token or value of the Expression"
        return self._token

    # Alias
    # In future it may be sensible to define a subclass of Expression 
    # for (the majority of) cases where the tokens are real numbers 
    value = token 
 
    @property 
    def scale(self):
        "The Scale of the Expression"
        return self._scale_aspect.scale 
 
    @property 
    def aspect(self):
        "The Aspect of the Expression"
        return self._scale_aspect.aspect 
        
    # Alias
    # See also the comment for ``value`` above     
    kind_of_quantity = aspect 
 
    @property 
    def scale_aspect(self):
        "The ScaleAspect of the Expression"
        return self._scale_aspect
        
 
    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """Return a new M-layer expression in the scale ``dst_scale``
        
        If ``dst_scale`` is a :class:`~scale_aspect.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        Args:
            dst_scale (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 
        
        Returns:
            :class:`~expression.Expression` 
            
        Raises:
            RuntimeError: if the aspect of the existing expression is incompatible with ``dst_scale``.

        """     
        if isinstance(dst_scale,ScaleAspect):
            # The source and destination aspects must match
            if self.aspect != dst_scale.aspect:          
                raise RuntimeError(
                    "incompatible aspects: {!r}".format( 
                        [self.aspect, dst_scale.aspect] 
                    )
                ) 
            else:
                dst_scale_aspect = dst_scale 
        else: 
            # Create a ScaleAspect object
            dst_scale_aspect = dst_scale.to_scale_aspect( self.aspect ) 
        
        fn = cxt.conversion_fn( self, dst_scale_aspect.scale )
        
        return Expression(
            fn( self._token ),
            dst_scale_aspect
        )

    # ---------------------------------------------------------------------------
    def cast(self,dst,aspect=no_aspect):
        """Return a new M-layer expression 
            
        If ``dst`` does not define an aspect, the value of ``aspect``  
        is attributed to the final scale-aspect.
        
        If the initial expression does not specify an aspect, the
        aspect of ``dst_scale_aspect`` is assumed to apply to both.

        If neither ``dst`` or ``aspect`` specifies an aspect,
        the existing expression aspect is attributed to the 
        final scale-aspect.
        
        Args:            
            dst(:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): 
                the scale or scale-aspect pair for the new expression. 
            aspect: may specify an aspect for the new expression if ``dst``
                only specifies the scale 

        Returns:
            an  M-layer :class:`~expression.Expression` 

        Raises:
            RuntimeError 
            
        """
        if isinstance(dst,Scale):
            if aspect is no_aspect:
                # Use the initial expression's aspect 
                dst_scale_aspect = dst.to_scale_aspect(
                    self.scale_aspect.aspect
                )
            else:
                # use the optional argument aspect 
                dst_scale_aspect = dst.to_scale_aspect(aspect)
         
            
        # If `aspect` has been specified, it must agree with `dst`
        elif aspect is not no_aspect and dst_scale_aspect.aspect != aspect:
            raise RuntimeError(
                "conflicting final aspects {!r}".format( 
                    (dst_scale_aspect.aspect,aspect) 
                ) 
            )
        
        # dst_scale_aspect is now a valid ScaleAspect
        if dst_scale_aspect.aspect is no_aspect: 
            if self.scale_aspect.aspect is no_aspect:
                raise RuntimeError(
                    "an aspect must be specified"
                )
            else:
                dst_scale_aspect = ScaleAspect(
                    dst_scale_aspect.scale,
                    self.scale_aspect.aspect
                )          
        
        # self.aspect may be no_aspect at this point
        # but if so dst_scale_aspect.aspect will 
        # specify the aspect
        fn = cxt.casting_fn(self, dst_scale_aspect )

        return Expression(
            fn( self._token ),
            dst_scale_aspect
        )

# ---------------------------------------------------------------------------
# Unbound functions and aliases corresponding to ``Expression`` operations
#
def token(xp):
    "Return the token or value from an expression"
    return xp.token

value = token

def convert(xp,dst_scale):
    """Return a new M-layer expression in the scale ``dst_scale``
    
    If ``dst_scale`` does not specify an aspect, 
    the aspect of the initial expression,
    ``xp``, will be applied.

    If ``dst_scale`` and the initial expression, ``xp``, 
    each specify an aspect, they must match.   

    Args:
        xp (:class:`~expression.Expression`) : the expression to be converted    
        dst_scale (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 
    
    Returns:
        :class:`~expression.Expression` 

    """        
    return xp.convert(dst_scale)
    
def cast(xp,dst,aspect=no_aspect):
    """Return a new M-layer expression in the scale-aspect ``dst_scale_aspect``
            
    If ``dst`` does not specify the aspect, the optional argument ``aspect``
    will be used but if that is ``None`
    the aspect of ``xp`` will be applied to the new expression

    Args:
        xp (:class:`~expression.Expression`): the expression to be converted.
        
        dst_scale_aspect (:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): 
            the scale-aspect pair for the new expression 
            
        aspect

    Returns:
        an  M-layer :class:`~expression.Expression` 

    Raises:
        RuntimeError: if no aspect is specified by ``xp`` 
        
    """
    return xp.cast(dst,aspect)
    
def aspect(xp):
    "Return the aspect or kind of quantity of an expression"
    return xp.aspect 
    
kind_of_quantity = aspect
    
def scale(xp):
    "Return the scale of an expression"
    return xp.scale 

def scale_aspect(xp):
    "Return the scale-aspect of an :class:`~expression.Expression`"
    return xp.scale_aspect 
  
# ---------------------------------------------------------------------------
# For the API 
#   
def expr(v,s,a=no_aspect):
    """Returns an M-layer expression 
    
    Args:
        v: the expression value or token
        s(:class:`~scale_aspect.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the expression 
        a(:class:`~aspect.Aspect`, optional): the expression aspect 
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
    
        

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import numbers
import math 

from m_layer.context import default_context as cxt
from m_layer.scale import Scale, ScaleAspect, ComposedScaleAspect
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
    An ``Expression`` is defined by a token and a scale-aspect pair. 
    """
    
    __slots__ = ("_token","_scale_aspect")
    
    def __init__(self,token,scale_aspect):
        self._token = token 
        self._scale_aspect = scale_aspect
      
    def __str__(self):
        short=True
        locale=cxt.locale       
        
        return "{} {}".format( 
            self.token, 
            self.scale 
        )
        
    def __repr__(self):
        locale=cxt.locale
        short=False
                
        if self.aspect is no_aspect:
            return "Expression({},{})".format(
                self.token,
                self.scale 
            )
        elif str(self.scale) == "": 
            # Special case, not sure how better to do this
            return "Expression({},1,{})".format(
                self.token,
                self.aspect
            )
        else:
            return "Expression({},{},{})".format(
                self.token,
                self.scale,
                self.aspect
            )
            
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
        
        If ``dst_scale`` is a :class:`~scale.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        Args:
            dst_scale (:class:`~scale.ScaleAspect` or 
            :class:`~scale.ComposedScaleAspect` or
            :class:`~scale.Scale`) 
        
        Returns:
            :class:`~expression.Expression` 
            
        Raises:
            RuntimeError: if the existing expression aspect is incompatible with ``dst_scale``.

        """     
        if (
            isinstance(dst_scale,ScaleAspect) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ):
            # The source and destination aspects must match
            if self.aspect != dst_scale.aspect:          
                raise RuntimeError(
                    "incompatible aspects: {!r}".format( 
                        [self.aspect, dst_scale.aspect] 
                    )
                ) 
            else:
                dst_scale_aspect = dst_scale  
                new_token = cxt.conversion_fn( 
                    self.scale.uid,self.aspect.uid,dst_scale_aspect.scale.uid 
                )(self._token)

        elif (
            isinstance(dst_scale,Scale) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ): 
            # Create a ScaleAspect object
            dst_scale_aspect = dst_scale.to_scale_aspect( self.aspect ) 
            new_token = cxt.conversion_fn( 
                self.scale.uid,self.aspect.uid,dst_scale_aspect.scale.uid 
            )(self._token)
            
        elif ( 
            isinstance(dst_scale,ComposedScaleAspect) 
        and isinstance(self.scale_aspect,ComposedScaleAspect)
        ):
            # Conversion of one expression to another.
            # The expressions must match up, so that 
            # pairs of source-destination scales can 
            # be found in the register. 
            # In this way, the conversion factors are 
            # combined to get the final factor.
                        
            # Note: the Context knows nothing about composed 
            # ScaleAspects. I take the view that the Context 
            # deals only with registered objects.
            
            # TODO: This routine requires the unit expressions 
            # to have the same form (e.g., x**2 is not the same as x*x).
            # An improvement would be to first reduce the expressions to 
            # products of powers and then evaluate the conversion factor.
            
            stack = []
            s_scale_it = iter(self.scale)
            d_scale_it = iter(dst_scale.scale)
            s_aspect_it = iter(self.aspect)
            d_aspect_it = iter(dst_scale.aspect)

            src_s = next(s_scale_it)
            dst_s = next(d_scale_it)
            src_a = next(s_aspect_it)
            dst_a = next(d_aspect_it)
            
            while True:
                try:
                
                    if isinstance(src_s,Scale):                        
                        assert isinstance(dst_s,Scale)                
                    
                        # A scale must correspond to an aspect
                        assert src_a == dst_a,\
                            "{!r} != {!r}".format(src_a,dst_a)
                    
                        # Evaluates the conversion factor
                        stack.append( 
                            cxt.conversion_fn( 
                                src_s.uid,src_a.uid,dst_s.uid 
                            )(1.0) 
                        )
                        
                        src_s = next(s_scale_it)
                        dst_s = next(d_scale_it)
                        src_a = next(s_aspect_it)
                        dst_a = next(d_aspect_it)

                        continue
                        
                    elif src_s == 'mul':                        
                        assert src_s == dst_s,\
                            "{!r}, {!r}".format(src_s, dst_s)
                            
                        x,y = stack.pop(),stack.pop()
                        stack.append(x*y)

                        # The aspect stack should have a 'mul' operation too
                        src_s = next(s_scale_it)
                        dst_s = next(d_scale_it)
                        src_a = next(s_aspect_it)
                        dst_a = next(d_aspect_it)

                        continue

                    elif src_s == 'div':
                        
                        assert src_s == dst_s,\
                            "{}, {}".format(src_s, dst_s)
                            
                        x,y = stack.pop(),stack.pop()
                        stack.append(y/x)

                        # The aspect stack should have a 'div' operation too
                        src_s = next(s_scale_it)
                        dst_s = next(d_scale_it)
                        src_a = next(s_aspect_it)
                        dst_a = next(d_aspect_it)
                       
                        continue

                    elif src_s == 'pow':
                        
                        assert src_s == dst_s,\
                            "{}, {}".format(src_s, dst_s)
                            
                        x,y = stack.pop(),stack.pop()
                        stack.append(y**x)
                        
                        src_s = next(s_scale_it)
                        dst_s = next(d_scale_it)

                        # The aspect stack should have a number and a 'pow' operation
                        src_a = next(s_aspect_it)
                        dst_a = next(d_aspect_it)
                        src_a = next(s_aspect_it)
                        dst_a = next(d_aspect_it)
                        
                        continue
                      
                    # The next steps work independently because a `numb 'rmul'`
                    # operation may occur on just one of the two stacks 
                    if isinstance(src_s,numbers.Integral):  
                        # cases are processed independently
                        stack.append( src_s )
                        src_s = next(s_scale_it)
                        
                        # Deal with 'rmul' case immediately
                        if src_s == 'rmul':
                            src_s = next(s_scale_it)
                            # do nothing else
                         
                    if isinstance(dst_s,numbers.Integral): 
                        stack.append( dst_s )
                        dst_s = next(d_scale_it)
     
                        # Deal with 'rmul' case immediately
                        if dst_s == 'rmul':
                            # require the inverse 
                            x = stack.pop()
                            stack.append( 1.0/x )
                            
                            dst_s = next(d_scale_it)
                            
                except StopIteration:
                    break
                    
            new_token = math.prod(stack)*self._token
            dst_scale_aspect = dst_scale
            
        return Expression(
            new_token,
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
            dst(:class:`~scale.ScaleAspect` or :class:`~scale.Scale`): 
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
        
        # self.aspect may be `no_aspect` at this point.
        fn = cxt.casting_fn(
            self.scale.uid,
            self.aspect.uid,
            dst_scale_aspect.scale.uid,
            dst_scale_aspect.aspect.uid 
        )

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
        dst_scale (:class:`~scale.ScaleAspect` or :class:`~scale.Scale`): the scale-aspect pair for the new expression 
    
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
        
        dst_scale_aspect (:class:`~scale.ScaleAspect` or :class:`~scale.Scale`): 
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
        s (:class:`~scale.ScaleAspect`, :class:`~scale.Scale`): the scale-aspect pair for the expression 
        a (:class:`~aspect.Aspect`, optional): the expression aspect 
    Returns:
        an  M-layer :class:`~expression.Expression`  
    
    """
    # `s` may be a scale-aspect pair or just a scale 
    if isinstance(s,(ScaleAspect,ComposedScaleAspect)):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, s.to_scale_aspect(a) )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        

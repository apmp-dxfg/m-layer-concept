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
        
        If ``dst_scale`` is a :class:`~scale_aspect.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        Args:
            dst_scale (:class:`~scale_aspect.ScaleAspect` or 
            :class:`~scale_aspect.ComposedScaleAspect` or
            :class:`~scale.Scale`): the scale-aspect pair for the new expression 
        
        Returns:
            :class:`~expression.Expression` 
            
        Raises:
            RuntimeError: if the existing expression aspect is incompatible with ``dst_scale``.

        """     
        if isinstance(dst_scale,ScaleAspect) and isinstance(self.scale_aspect,ScaleAspect):
            # The source and destination aspects must match
            if self.aspect != dst_scale.aspect:          
                raise RuntimeError(
                    "incompatible aspects: {!r}".format( 
                        [self.aspect, dst_scale.aspect] 
                    )
                ) 
            else:
                dst_scale_aspect = dst_scale  
                new_token = cxt.conversion_fn( self, dst_scale_aspect.scale )(self._token)

        elif isinstance(dst_scale,Scale) and isinstance(self.scale_aspect,ScaleAspect): 
            # Create a ScaleAspect object
            dst_scale_aspect = dst_scale.to_scale_aspect( self.aspect ) 
            new_token = cxt.conversion_fn( self, dst_scale_aspect.scale )(self._token)
            
        elif ( 
            isinstance(dst_scale,ComposedScaleAspect) 
        and isinstance(self.scale_aspect,ComposedScaleAspect)
        ):
            src_aspect_stack = self.aspect
            dst_aspect_stack = dst_scale.aspect
            
            src_scale_stack = self.scale
            dst_scale_stack = dst_scale.scale
            
            a_N = len(src_aspect_stack)
            
            assert a_N == len(dst_scale.aspect),\
                "incompatible aspects: {!}, {!r}".format(
                    self.aspect, dst_scale.aspect
                 )
            
            assert s_N == len(dst_scale.scale),\
                "incompatible scales: {!}, {!r}".format(
                    self.scale, dst_scale.scale
                 )
           
            # Step through the stacks and obtain a factor for each ScaleAspect pair.
            # The scale stack may have numerical factors associated with 'rmul', 
            # if these do not match then they should be consumed in the conversion factor.
            # Expect 1-to-1 matching between aspect stack contents 
            # (note, 'rmul' is omitted from aspect stacks).
            
            stack = []
            a_ptr = 0
            s_ptr = 0
            d_ptr = 0
            
            while a_ptr < a_N:
            
                if isinstance(src_scale_stack[s_ptr],Scale):
                    assert isinstance(dst_scale_stack[d_ptr],Scale)                
                
                    src_s = src_scale_stack[s_ptr]
                    s_ptr += 1
                    dst_s = dst_scale_stack[d_ptr]
                    d_ptr += 1              
                    
                    # A scale must correspond to an aspect
                    src_a = src_aspect_stack[a_ptr]
                    a_ptr += 1
                    assert src_a == dst_aspect_stack[a_ptr]
                
                    stack.append( cxt.conversion_fn( src_s, dst_s )(1.0) )
                    
                    continue
                    
                elif src_scale_stack[s_ptr] == 'mul':
                    assert src_s == dst_scale_stack[d_ptr],\
                        "{}, {}".format(src_s, dst_scale_stack[d_ptr])
                        
                    src_s = src_scale_stack[s_ptr]
                    s_ptr += 1
                    dst_s = dst_scale_stack[d_ptr]
                    d_ptr += 1              
                    
                    print(src_s)
                    x,y = stack.pop(),stack.pop()
                    stack.append(x*y)

                    # The aspect stack should have a 'mul' operation too
                    a_ptr += 1
                    
                    continue

                elif src_scale_stack[s_ptr] == 'div':
                    assert src_s == dst_scale_stack[d_ptr],\
                        "{}, {}".format(src_s, dst_scale_stack[d_ptr])
                        
                    src_s = src_scale_stack[s_ptr]
                    s_ptr += 1
                    dst_s = dst_scale_stack[d_ptr]
                    d_ptr += 1              
                    
                    print(src_s)
                    x,y = stack.pop(),stack.pop()
                    stack.append(y/x)

                    # The aspect stack should have a 'div' operation too
                    a_ptr += 1
                    
                    continue

                elif src_scale_stack[s_ptr] == 'pow':
                    assert src_s == dst_scale_stack[d_ptr],\
                        "{}, {}".format(src_s, dst_scale_stack[d_ptr])
                        
                    src_s = src_scale_stack[s_ptr]
                    s_ptr += 1
                    dst_s = dst_scale_stack[d_ptr]
                    d_ptr += 1              
                    
                    print(src_s)
                    x,y = stack.pop(),stack.pop()
                    stack.append(y**x)
                    
                    # The aspect stack should have a number and a 'pow' operation
                    a_ptr += 2
                    
                    continue
                  
                # The next steps work independently because a `numb 'rmul'`
                # operation may occur on just one of the two stacks 
                if isinstance(src_scale_stack[s_ptr],numbers.Integral):  
                    # cases are processed independently
                    stack.append( src_scale_stack[s_ptr] )
                    s_ptr += 1
                    print("src value",src_scale_stack[s_ptr])
                    
                    # Deal with 'rmul' case immediately
                    if src_scale_stack[s_ptr] == 'rmul':
                        s_ptr += 1
                        # do nothing else
                     
                if isinstance(dst_scale_stack[d_ptr],numbers.Integral): 
                    stack.append( dst_scale_stack[d_ptr] )
                    d_ptr += 1
                    print("dst value",dst_scale_stack[d_ptr])
 
                    # Deal with 'rmul' case immediately
                    if dst_scale_stack[d_ptr] == 'rmul':
                        d_ptr += 1
                        # require the inverse 
                        x = stack.pop()
                        stack.append( 1.0/x )
            
            new_token = math.fprod(stack)*self._token
            
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
    if isinstance(s,(ScaleAspect,ComposedScaleAspect)):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, s.to_scale_aspect(a) )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        

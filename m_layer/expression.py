# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import numbers
import math 

from m_layer.context import default_context as cxt
from m_layer.scale import Scale, ScaleAspect, ComposedScaleAspect
from m_layer.aspect import no_aspect
from m_layer.stack import normal_form

__all__ = (
    'expr', 
    'token', 'value',
    'convert', 
    'cast',
    'scale_aspect',
)

# ---------------------------------------------------------------------------
class Expression(object):
    
    """
    An ``Expression`` is defined by a token and a scale-aspect pair. 
    The scale-aspect may be a composition of several scale-aspect pairs.
    """
    
    __slots__ = ("_token","_scale_aspect")
    
    def __init__(self,token,mdata):
        self._token = token 
        
        if isinstance(mdata,(ScaleAspect,ComposedScaleAspect)):
            self._scale_aspect = mdata
        else:
            assert False, repr(mdata)
      
    def __str__(self):
        # TODO: something sensible when scale_aspect is ComposedScaleAspect 
        if isinstance(self._scale_aspect,ScaleAspect):
            return "{} {}".format( 
                self.token, 
                self.scale_aspect.scale 
            )
        else:
            return "{} {}".format( 
                self.token, 
                self.scale_aspect 
            )
        
    def __repr__(self):
        # TODO: something sensible when scale_aspect is ComposedScaleAspect 
        if isinstance(self._scale_aspect,ScaleAspect):
            if self.scale_aspect.aspect is no_aspect:
                return "Expression({},{})".format(
                    self.token,
                    self.scale_aspect.scale 
                    )
            elif str(self.scale_aspect.scale) == "": 
                # Special case, not sure how better to do this
                return "Expression({},1,{})".format(
                    self.token,
                    self.scale_aspect.aspect
                )
            else:
                return "Expression({},{},{})".format(
                    self.token,
                    self.scale_aspect.scale,
                    self.scale_aspect.aspect
                )                
        else:
            return "Expression({},{})".format( 
                self.token, 
                self.scale_aspect 
            )
            
    # In future it may be sensible to define a subclass of Expression 
    # for (the majority of) cases where the tokens are real numbers 
    @property
    def token(self):
        "The token or value of the Expression"
        return self._token

    # Alias
    value = token 
  
    # Note `_scale_aspect` may be a ComposedScaleAspect, so 
    # there is no reason to provide access to individual `aspect`
    # and `scale` properties.
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
            dst_scale (:class:`~scale.ComposedScaleAspect` or
            :class:`~scale.ScaleAspect` or 
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
            if self.scale_aspect.aspect != dst_scale.aspect:          
                raise RuntimeError(
                    "incompatible aspects: {!r}".format( 
                        [self.scale_aspect.aspect, dst_scale.aspect] 
                    )
                ) 
            else:
                dst_scale_aspect = dst_scale  
                new_token = cxt.conversion_fn( 
                    self.scale_aspect.scale.uid,
                    self.scale_aspect.aspect.uid,
                    dst_scale_aspect.scale.uid 
                )(self._token)

        elif (
            isinstance(dst_scale,Scale) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ): 
            # Create a ScaleAspect object
            dst_scale_aspect = dst_scale.to_scale_aspect( self.scale_aspect.aspect ) 
            new_token = cxt.conversion_fn( 
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid 
            )(self._token)
            
        elif ( 
            isinstance(dst_scale,ComposedScaleAspect) 
        and isinstance(self.scale_aspect,ComposedScaleAspect)
        ):
            # Conversion of one expression to another.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
                        
            # Note: I take the view that the Context 
            # deals only with registered objects.
            # The Context knows nothing about composed 
            # ScaleAspects. 
            
            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)
            dst_pops = normal_form(dst_scale.stack)
            
            # Step 2: take into account any stand-alone numerical factors
            conversion_factor = src_pops.prefactor/dst_pops.prefactor
            
            # Step 3: step through the scale-aspect terms,
            # obtaining a conversion factor for each
            src_factors = src_pops.factors
            dst_factors = dst_pops.factors
            for src_i,dst_i in zip(src_factors.keys(),dst_factors.keys()):
            
                # Each term also has an exponent
                src_exp = src_factors[src_i]
                assert src_exp == dst_factors[dst_i],\
                    "{} != {}".format(src_exp,dst_factors[dst_i])

                src_s_uid,src_a_uid = src_i.uid
                dst_s_uid = dst_i.uid[0]

                c = cxt.conversion_fn( 
                        src_s_uid,src_a_uid,dst_s_uid                     
                )(1.0) 
                conversion_factor *= c**src_exp
            
            new_token = conversion_factor*self._token
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
            self.scale_aspect.scale.uid,
            self.scale_aspect.aspect.uid,
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
    
# ---------------------------------------------------------------------------
def scale_aspect(xp):
    """
    Args:
        xp: class:`~expression.Expression`
        
    Returns:
        a :class:`ScaleAspect` or a :class:`ComposedScaleAspect`
        
    """
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
    
        

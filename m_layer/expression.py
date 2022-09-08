# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import numbers
import math 

from m_layer.context import default_context as cxt
from m_layer.scale import Scale, ComposedScale, ScaleAspect, ComposedScaleAspect
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
        """Return a new expression in terms of the scale ``dst_scale``
        
        If ``dst_scale`` is a :class:`~scale.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        Args:
            dst_scale (:class:`~scale.ComposedScaleAspect` or
            :class:`~scale.ScaleAspect` or 
            :class:`~scale.ComposedScale`
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
                    "incompatible aspects: {!r} and {!r}".format( 
                        self.scale_aspect.aspect, 
                        dst_scale.aspect 
                    )
                )
                
            else:
                dst_scale_aspect = dst_scale 
                
                new_token = cxt.conversion_from_scale_aspect( 
                    self.scale_aspect.scale.uid,
                    self.scale_aspect.aspect.uid,
                    dst_scale_aspect.scale.uid 
                )(self._token)

        elif (
            isinstance(dst_scale,Scale) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ): 
            # The source aspect will be applied to the result.
            # Create a ScaleAspect return object with the initial aspect 
            # Again, the aspect can be `no_aspect`.
            dst_scale_aspect = dst_scale.to_scale_aspect( 
                self.scale_aspect.aspect 
            ) 
            
            new_token = cxt.conversion_from_scale_aspect( 
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid 
            )(self._token)
            
        elif ( 
            isinstance(dst_scale,(ComposedScale,ComposedScaleAspect) ) 
        and isinstance(self.scale_aspect,ComposedScaleAspect)
        ):
            # Conversion from one composed expression to another.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
                        
            # Note: I take the view that the Context 
            # deals only with registered objects.
            # The Context knows nothing about composed 
            # ScaleAspects. 

            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)
            
            if isinstance(dst_scale,ComposedScale):
                # Copy the various src aspects to a new ComposedScaleAspect.
                dst_scale_aspect = dst_scale.composed_scale_aspect( 
                    self.scale_aspect
                ) 
                dst_pops = normal_form(dst_scale_aspect.stack)
            
            else:    
                dst_scale_aspect = dst_scale                
                dst_pops = normal_form(dst_scale_aspect.stack)
            
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
                dst_s_uid, dst_a_uid = dst_i.uid
                
                # Aspects must match
                assert src_a_uid == dst_a_uid,\
                    "{!r} != {!r}".format(src_a_uid,dst_a_uid)

                c = cxt.conversion_from_scale_aspect( 
                        src_s_uid,src_a_uid,dst_s_uid                     
                )(1.0) 
                conversion_factor *= c**src_exp
            
            new_token = conversion_factor*self._token
          
        return Expression(
            new_token,
            dst_scale_aspect
        )

    # ---------------------------------------------------------------------------
    def cast(self,dst,aspect=no_aspect):
        """Return a new M-layer expression 
        
        The aspect of the resulting expression is determined as follows:
        i) the aspect specified in ``dst``, or, 
        ii) the aspect specified in ``aspect``, or,
        iii) the aspect of the initial expression 
                
        Args:            
            dst(:class:`~scale.ScaleAspect` or :class:`~scale.Scale`): 
                the scale or scale-aspect pair for the new expression. 
                
            aspect(:class:`~aspect.Aspect`): is used
            if ``dst`` is a :class:`~scale.Scale`. When an aspect
            is specified, it will be attributed to 
            the result, otherwise the expression aspect is carried over.  

        Returns:
            an  M-layer :class:`~expression.Expression` 
            
        Raises:
            RuntimeError 
            
        """
        # TODO: Other casting operations
        # 
        # i) ComposedScale to ScaleAspect or Scale and `aspect` 
        #       If the source is dimensionally compatible 
        #       with `dst_scale`. The aspect is determined 
        #       by `dst_scale`, or `aspect` and could be `no_aspect`
        #
        # ii) ComposedScaleAspect to ScaleAspect
        #       This will be the same as for ComposedScale.       
        #       There will be information about the aspect expression 
        #       in the source that is ignored.
        
        if (
            isinstance(dst,Scale) 
        and 
            isinstance(self.scale_aspect,ScaleAspect)
        ):
        
            if aspect is no_aspect:
                # Nothing specifies a destination aspect
                # carry forward the initial aspect
                dst_scale_aspect = dst.to_scale_aspect(
                    self.scale_aspect.aspect
                )
            else:
                # use ``aspect`` 
                dst_scale_aspect = dst.to_scale_aspect(aspect)
                 
        elif (
            isinstance(dst,ScaleAspect)
        and 
            isinstance(self.scale_aspect,ScaleAspect)
        ):
            if dst_scale_aspect.aspect is no_aspect: 
                if aspect is no_aspect:
                    # Nothing specifies a destination aspect
                    # carry forward the initial aspect
                    dst_scale_aspect = ScaleAspect(
                        dst_scale_aspect.scale,
                        self.scale_aspect.aspect
                    )  
                else:
                    # use ``aspect`` 
                    dst_scale_aspect = ScaleAspect(
                        dst_scale_aspect.scale,
                        aspect
                    )  
        
        fn = cxt.casting_from_scale_aspect(
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
    
        

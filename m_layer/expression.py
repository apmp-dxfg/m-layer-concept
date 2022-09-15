# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
import numbers
import math 

from fractions import Fraction

from m_layer.lib import *
from m_layer.context import global_context as cxt
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
        
        if isinstance(mdata,(ScaleAspect,CompoundScale,CompoundScaleAspect)):
            self._scale_aspect = mdata
        else:
            assert False, repr(mdata)
      
    def __str__(self):
        # TODO: something sensible when scale_aspect is CompoundScaleAspect
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
        # TODO: something sensible when scale_aspect is CompoundScaleAspect 
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
        # The Fraction display can be disconcerting when 
        # the ratio involves large integers
        if isinstance(self._token,Fraction):
            x = float(self._token) 
        else:
            x = self._token
        return x

    # Alias
    value = token 
  
    # Note `_scale_aspect` may be a CompoundScaleAspect, so 
    # there is no reason to provide access to individual `aspect`
    # and `scale` properties.
    @property 
    def scale_aspect(self):
        "The ScaleAspect of the Expression"
        return self._scale_aspect
        
 
    # ---------------------------------------------------------------------------
    def convert(self,dst_scale):
        """Return a new expression in terms of the scale ``dst_scale``
        
        If ``dst_scale`` is a :class:`~lib.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        Args:
            dst_scale (:class:`~lib.CompoundScaleAspect` or
            :class:`~lib.ScaleAspect` or 
            :class:`~lib.CompoundScale`
            :class:`~lib.Scale`) 
        
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
            isinstance(dst_scale,(CompoundScale,CompoundScaleAspect) ) 
        and isinstance(self.scale_aspect,CompoundScaleAspect)
        ):
            # Conversion from a compound expression.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
            # If the destination is just a CompoundScale, then 
            # the current aspects are copied into the result.
                        
            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)
            
            if isinstance(dst_scale,CompoundScale):
                # Copy the various src aspects to a new CompoundScaleAspect.
                dst_scale_aspect = dst_scale.compound_scale_aspect( 
                    self.scale_aspect
                ) 
            
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

        elif ( 
            isinstance(dst_scale,CompoundScale ) 
        and isinstance(self.scale_aspect,CompoundScale)
        ):
            # This is the generic case, where no aspect is available
            
            # Conversion from one compound expression to another.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
                        
            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)            
            dst_pops = normal_form(dst_scale.stack)         
            
            # Step 2: take into account any stand-alone numerical factors
            conversion_factor = src_pops.prefactor/dst_pops.prefactor
            
            # Step 3: step through the scale terms,
            # obtaining a conversion factor for each
            src_factors = src_pops.factors
            dst_factors = dst_pops.factors
            for src_i,dst_i in zip(src_factors.keys(),dst_factors.keys()):
            
                # Each term also has an exponent
                src_exp = src_factors[src_i]
                assert src_exp == dst_factors[dst_i],\
                    "{} != {}".format(src_exp,dst_factors[dst_i])

                src_s_uid = src_i.uid
                dst_s_uid = dst_i.uid
                src_a_uid = no_aspect.uid

                c = cxt.conversion_from_scale_aspect( 
                        src_s_uid,src_a_uid,dst_s_uid                     
                )(1.0) 
                conversion_factor *= c**src_exp
            
            new_token = conversion_factor*self._token
 
            # Set the aspect component of the new CompoundScaleAspect.
            dst_scale_aspect = dst_scale.to_compound_scale_aspect( 
                self.scale_aspect
            ) 
 
        elif ( 
            isinstance(dst_scale,(Scale,ScaleAspect) ) 
        and isinstance(self.scale_aspect,CompoundScaleAspect)
        ):
            # Conversion from a compound scale to a specific one,
            # which must be dimensionally equivalent and generic. 
            
            if isinstance(dst_scale,Scale):            
                dst_scale_aspect = dst_scale.to_scale_aspect(no_aspect)
                
            elif isinstance(dst_scale,ScaleAspect):
                if dst_scale.aspect is not no_aspect:
                    raise RuntimeError(
                        "cannot change aspect: {!r}".format(dst_scale)
                    ) 
                else:
                    dst_scale_aspect = dst_scale 
            else:
                assert False, repr(dst_scale) 
                
            src_dim = self.scale_aspect.dimension.simplify     
            if src_dim != dst_scale_aspect.dimension:
                raise RuntimeError(
                    "dimensions must match: {}, {}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
                )           

            try:
                src_scale_uid = self.dimension_conversion_reg[src_dim]   
            except KeyError:
                raise RuntimeError(
                    "no scale defined for {!r}".format(src_dim)
                )           
                        
            new_token = cxt.conversion_from_scale_aspect( 
                src_scale_uid,
                no_aspect.uid,
                dst_scale_aspect.scale.uid 
            )(self._token)

        else:
            assert False
            
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
        
            dst(:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): the scale or scale-aspect pair for the new expression. 
                
            aspect(:class:`~lib.Aspect`): is used
            if ``dst`` is a :class:`~lib.Scale`. When an aspect
            is specified, it will be attributed to 
            the result, otherwise the expression aspect is carried over.  

        Returns:
            an  M-layer :class:`~expression.Expression` 
            
        Raises:
            RuntimeError 
            
        """        
        if isinstance(self.scale_aspect,ScaleAspect):
        
            if isinstance(dst,Scale):            
                if aspect is no_aspect:
                    # carry forward the initial aspect
                    dst_scale_aspect = dst.to_scale_aspect(
                        self.scale_aspect.aspect
                    )
                else:
                    dst_scale_aspect = dst.to_scale_aspect(aspect)
                     
            elif isinstance(dst,ScaleAspect):
                if dst_scale_aspect.aspect is no_aspect: 
                    if aspect is no_aspect:
                        # carry forward the initial aspect
                        dst_scale_aspect = ScaleAspect(
                            dst_scale_aspect.scale,
                            self.scale_aspect.aspect
                        )  
                    else:
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

        elif isinstance(
            self.scale_aspect,
            (CompoundScale,CompoundScaleAspect)
        ):
            src_dim = self.scale_aspect.dimension.simplify
            
            if src_dim != dst.dimension:
                raise RuntimeError(
                    "dimensions must match: {}, {}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
                )           
            
            if isinstance(dst,Scale):            
                if aspect is no_aspect:
                    # cannot carry forward an initial aspect,
                    # so use no_aspect
                    dst_scale_aspect = dst.to_scale_aspect(no_aspect)
                else:
                    dst_scale_aspect = dst.to_scale_aspect(aspect)

            elif isinstance(dst,ScaleAspect):
                if dst_scale_aspect.aspect is no_aspect:
                    # Note `aspect` may just be `no_aspect` anyway
                    dst_scale_aspect = ScaleAspect(
                        dst_scale_aspect.scale,
                        aspect
                    ) 
                        
            fn = cxt.casting_from_compound_scale(
                src_dim,
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
        dst_scale (:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): the scale-aspect pair for the new expression 
    
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
        
        dst_scale_aspect (:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): 
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
        a :class:`~lib.ScaleAspect` or a :class:`~lib.CompoundScaleAspect`
        
    """
    return xp.scale_aspect 
  
# ---------------------------------------------------------------------------
# For the API 
#   
def expr(v,s,a=no_aspect):
    """Returns an M-layer expression 
    
    Args:
        v: the expression value or token
        s (:class:`~lib.ScaleAspect`, :class:`~lib.Scale`): the scale-aspect pair for the expression 
        a (:class:`~lib.Aspect`, optional): the expression aspect 
    Returns:
        an  M-layer :class:`~expression.Expression`  
    
    """
    # `s` may be a scale-aspect pair or just a scale 
    if isinstance(s,(ScaleAspect,CompoundScale,CompoundScaleAspect)):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, s.to_scale_aspect(a) )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        

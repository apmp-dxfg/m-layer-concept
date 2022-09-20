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
    def convert(self,dst):
        """Return a new expression in terms of ``dst``
        
        Args:
            dst (:class:`~lib.CompoundScaleAspect` or
            :class:`~lib.CompoundScale`
            :class:`~lib.ScaleAspect` or 
            :class:`~lib.Scale`) 
        
        Returns:
            :class:`~expression.Expression` 

        If ``dst`` is a :class:`~lib.ScaleAspect`,
        the associated aspect must match the existing expression.   
        
        
        """
        if (
            isinstance(dst,ScaleAspect) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ):
            # The source and destination aspects must match
            if self.scale_aspect.aspect != dst.aspect:          
                raise RuntimeError(
                    "incompatible aspects: {!r} and {!r}".format( 
                        self.scale_aspect.aspect, 
                        dst.aspect 
                    )
                )
                
            else:
                dst_scale_aspect = dst 
                
                new_token = cxt.conversion_from_scale_aspect( 
                    self.scale_aspect.scale.uid,
                    self.scale_aspect.aspect.uid,
                    dst_scale_aspect.scale.uid 
                )(self._token)

        elif (
            isinstance(dst,Scale) 
        and isinstance(self.scale_aspect,ScaleAspect)
        ): 
            # The source aspect will be applied to the result.
            # Create a ScaleAspect return object with the initial aspect 
            # Again, the aspect can be `no_aspect`.
            dst_scale_aspect = dst.to_scale_aspect( 
                self.scale_aspect.aspect 
            ) 
            
            new_token = cxt.conversion_from_scale_aspect( 
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid 
            )(self._token)
            
        elif ( 
            isinstance(dst,(CompoundScale,CompoundScaleAspect) ) 
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
            
            if isinstance(dst,CompoundScale):
                # Copy the various src aspects to a new CompoundScaleAspect.
                dst_scale_aspect = dst.compound_scale_aspect( 
                    self.scale_aspect
                ) 
            
            else:    
                dst_scale_aspect = dst                
                
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
            isinstance(dst,CompoundScale ) 
        and isinstance(self.scale_aspect,CompoundScale)
        ):
            # This is the generic case, where no aspect is available
            
            # Conversion from one compound expression to another.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
                        
            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)            
            dst_pops = normal_form(dst.stack)         
            
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
            dst_scale_aspect = dst.to_compound_scale_aspect( 
                self.scale_aspect
            ) 
 
        elif ( 
            isinstance(dst,(Scale,ScaleAspect) ) 
        and isinstance(self.scale_aspect,CompoundScale)
        ):
            # Conversion from a compound scale to a specific one,
            # which must be dimensionally equivalent and generic. 
            
            if isinstance(dst,Scale):            
                dst_scale_aspect = dst.to_scale_aspect(no_aspect)
                
            elif isinstance(dst,ScaleAspect):
                if dst.aspect is not no_aspect:
                    raise RuntimeError(
                        "cannot change aspect: {!r}".format(dst)
                    ) 
                else:
                    dst_scale_aspect = dst 
            else:
                assert False, repr(dst) 
                
            src_dim = self.scale_aspect.dimension.simplify     
            if src_dim != dst_scale_aspect.dimension:
                raise RuntimeError(
                    "dimensions must match: {}, {}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
                )           
                        
            new_token = cxt.conversion_from_compound_scale_dim( 
                src_dim,
                dst_scale_aspect.scale.uid 
            )(self._token)
            
        elif ( 
            isinstance(dst,(Scale,ScaleAspect) ) 
        and isinstance(self.scale_aspect,CompoundScaleAspect)
        ):
            # Conversion from a compound scale-aspect to a specific one.
            # Since the result must have a single aspect, we are limited
            # to just the generic no_aspect. So this function must 
            # fail if there are any non-trivial aspects in the expression.
            if not self.scale_aspect.to_compound_scales_and_aspects()[1].no_aspect: 
                raise RuntimeError(
                    "conversion would loose aspect information {}".format(
                        self.scale_aspect
                    )
                )
            if isinstance(dst,Scale):            
                dst_scale_aspect = dst.to_scale_aspect(no_aspect)
                
            elif isinstance(dst,ScaleAspect):
                if dst.aspect is not no_aspect:
                    # A cast would be required to change the aspect
                    raise RuntimeError(
                        "cannot change aspect: {!r}".format(dst)
                    ) 
                else:
                    dst_scale_aspect = dst 
            else:
                assert False, repr(dst) 
                
            src_dim = self.scale_aspect.dimension.simplify     
            if src_dim != dst_scale_aspect.dimension:
                raise RuntimeError(
                    "dimensions must match: {}, {}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
                )           
                        
            new_token = cxt.conversion_from_compound_scale_dim( 
                src_dim,
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
        
        Args:
        
            dst(:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): the scale-aspect pair for the new expression 
            aspect(:class:`~lib.Aspect`):   

        Returns:
            class:`~expression.Expression` 
            
        Casting determines an aspect for the new expression as follows:
        i) the aspect as specified in ``dst``, or, 
        ii) the aspect as specified by ``aspect``, or,
        iii) the aspect of the initial expression                 
            
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
                if dst.aspect is no_aspect: 
                    if aspect is no_aspect:
                        # carry forward the initial aspect
                        dst_scale_aspect = ScaleAspect(
                            dst.scale,
                            self.scale_aspect.aspect
                        )  
                    else:
                        dst_scale_aspect = ScaleAspect(
                            dst.scale,
                            aspect
                        )
                else:
                    dst_scale_aspect = dst
            else:
                assert False, repr(dst)
                
            fn = cxt.casting_from_scale_aspect(
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid,
                dst_scale_aspect.aspect.uid 
            )

        elif isinstance(
            self.scale_aspect,(CompoundScale,CompoundScaleAspect)
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
                if dst.aspect is no_aspect:
                    # Note `aspect` may just be `no_aspect` anyway
                    dst_scale_aspect = ScaleAspect(
                        dst.scale,
                        aspect
                    ) 
                else:
                    dst_scale_aspect = dst                
                
            else:
                assert False, repr(dst)
                
            fn = cxt.casting_from_compound_scale_dim(
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

def convert(xp,dst):
    """Return a new expression in terms of ``dst``
    
    If ``dst`` does not specify an aspect, 
    the aspect of the initial expression will be carried over.

    If ``dst`` and the initial expression, ``xp``, 
    each specify an aspect, they must match.   

    Args:
        xp (:class:`~expression.Expression`) : the initial expression    
        dst (:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): the scale-aspect for the new expression 
    
    Returns:
        :class:`~expression.Expression` 

    """        
    return xp.convert(dst)
    
# ---------------------------------------------------------------------------
def cast(xp,dst,aspect=no_aspect):
    """Return a new expression in terms of ``dst``
            
    If ``dst`` does not specify an aspect, ``aspect`` is used. 
    If ``aspect`` is ``None``, the aspect of ``xp`` is carried over to 
    the new expression

    Args:
        xp (:class:`~expression.Expression`): the initial expression
        
        dst (:class:`~lib.ScaleAspect` or :class:`~lib.Scale`): 
            the scale-aspect for the new expression 
            
        aspect (:class:`~lib.Aspect`, optional)

    Returns:
        :class:`~expression.Expression` 
        
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
    """Create a new expression 
    
    Args:
        v: the expression value or token
        s (:class:`~lib.ScaleAspect`, :class:`~lib.Scale`): the scale
        a (:class:`~lib.Aspect`, optional): the aspect 
    Returns:
        :class:`~expression.Expression`  
    
    """
    # `s` may be a scale-aspect pair or just a scale 
    if isinstance(s,(ScaleAspect,CompoundScale,CompoundScaleAspect)):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, s.to_scale_aspect(a) )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        

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
        
    #------------------------------------------------------------------------    
    def _to_src_dst_lists(self,set_of_pairs):
        """
        Create a pair of list of Scales,
        one for transformation sources 
        and one for destinations
        
        """
        src = [ Scale(i[0]) for i in set_of_pairs ]
        dst = [ Scale(i[1]) for i in set_of_pairs ]
        
        return src,dst 

    #------------------------------------------------------------------------    
    def _closest(self,systematic,scale_lst):
        """
        Find the Scale in ``scale_lst`` closest to ``systematic`` 
        
        Args:
            systematic (:class:`~systematic.Systematic`)
            scale_lst (sequence of :class:`~lib.Scale`)
            
        Returns:
            :class:`~lib.Scale`
            
        """
        # The closest scale factor match
        factors = [
            abs( math.log10( s_i.systematic.prefix / systematic.prefix ) )
                for s_i in scale_lst
        ]
        idx = factors.index( min(factors) )
        
        return scale_lst[idx]
        
    #------------------------------------------------------------------------    
    def _systematic_conversion_factor(self,src_systematic,dst_systematic):
        """
        Return a conversion factor for ``src`` to ``dst`` 
                
        Args:
            src_systematic (:class:`~systematic.Systematic`)
            dst_systematic (:class:`~systematic.Systematic`)
        
        Returns:
            float
            
        """
        src_key = (src_systematic.system,src_systematic.dimensions)
        dst_key = (dst_systematic.system,dst_systematic.dimensions)
     
        if src_key != dst_key:
            raise RuntimeError(
                "no conversion from {} to {}".format(src_key,dst_key)
            )  
     
        return dst_systematic.prefix / src_systematic.prefix 
                        
    # ---------------------------------------------------------------------------
    def _systematic_src_conversion(self,dst_scale_aspect):
        # Look for a direct match with the destination scale

        # For now, we can't infer a src aspect
        src_aspect = no_aspect
    
        src_systematic = self.scale_aspect.systematic.simplify
        src_key = (src_systematic.system,src_systematic.dimensions)

        c = None
        
        _key = (src_key,dst_scale_aspect.scale.uid)
        if _key in cxt.dim_dst_conversion_reg:
            set_of_scale_pairs = cxt.dim_dst_conversion_reg[
                src_key,
                dst_scale_aspect.scale.uid
            ]  
            src_scales, dst_scales = self._to_src_dst_lists( 
                set_of_scale_pairs 
            )
            int('_systematic_src_conversion: ', src_scales)
            
            if (
                len(src_scales) 
            and dst_scale_aspect.scale in dst_scales
            ):
                ssrc = self._closest(src_systematic,src_scales)
                
                c = self._systematic_conversion_factor(
                    src_systematic,ssrc.systematic
                )
                c *= cxt.conversion_from_scale_aspect( 
                    ssrc.uid,
                    src_aspect.uid,
                    dst_scale_aspect.scale.uid 
                )(1)
                
        return c  
            
    # ---------------------------------------------------------------------------
    def _systematic_dst_conversion(self,dst_scale_aspect):
    
        src_key = self.scale_aspect.scale.uid
        dst_key = (dst_systematic.system,dst_systematic.dimensions)
        
        c = None
        
        if (src_key,dst_key):
            set_of_scale_pairs = cxt.src_dim_conversion_reg[
                (src_key,dst_key)
            ]                       
            src_pairs, dst_pairs = self._to_src_dst_lists( set_of_scale_pairs )
            if len(src_pairs) == 0:
                raise RuntimeError(
                    "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                )

            sdst = self._closest(dst_systematic,dst_pairs)
            c = self._systematic_conversion_factor(dst_systematic,dst)
            c *= cxt.conversion_from_scale_aspect( 
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                sdst_uid 
            )(1)
            
        return c

    # ---------------------------------------------------------------------------
    def _systematic_src_dst_conversion(self,dst_scale_aspect):
        # Look for a systematic match using the initial and final scales
    
        # For now, we can't infer a src aspect
        src_aspect = no_aspect
        
        src_systematic = self.scale_aspect.systematic.simplify
        src_key = (src_systematic.system,src_systematic.dimensions)

        dst_systematic = dst_scale_aspect.systematic
        dst_key = (dst_systematic.system,dst_systematic.dimensions)
        
        c = None 
        
        _key = (src_key,dst_key)
        if _key in cxt.dim_dim_conversion_reg:
            set_of_scale_pairs = cxt.dim_dim_conversion_reg[
                src_key,
                dst_scale_aspect.scale.uid
            ]  
            src_scales, dst_scales = self._to_src_dst_lists( 
                set_of_scale_pairs 
            )
            
            if len(src_scales) and len(dst_scales):
                # Use existing conversions
                ssrc = self._closest(src_systematic,src_scales)
                sdst = self._closest(dst_systematic,dst_scales)
                
                c = self._systematic_conversion_factor(
                    src_systematic,ssrc.systematic
                )
                c *= self._systematic_conversion_factor(
                    sdst.systematic,dst_systematic
                )
                c *= cxt.conversion_from_scale_aspect( 
                    ssrc.uid,
                    src_aspect.uid,
                    sdst.uid
                )(1)
                
        if c is None:
            c = self._systematic_conversion_factor(
                src_systematic,dst_systematic
            )        

        return c
            
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
        # Expressions hold a ScaleAspect, or a CompoundScaleAspect,
        # which is the starting point.
        # The conversion operation may specify the result in different ways.
        #
        # Different conversion cases to consider :
        # i) ScaleAspect -> Scale
        # ii) ScaleAspect -> ScaleAspect 
        # iii) CompoundScaleAspect -> CompoundScaleAspect
        # iv) CompoundScaleAspect -> CompoundScale 
        # v) CompoundScaleAspect -> ScaleAspect or Scale
        
        # Cases i) & ii):
        if (
            isinstance(self.scale_aspect,ScaleAspect)
        and isinstance(dst,(Scale,ScaleAspect)) 
        ):        
            src = self.scale_aspect
            
            if isinstance(dst,ScaleAspect):
                # Source and destination aspects must match
                if src.aspect != dst.aspect:          
                    raise RuntimeError(
                        "incompatible aspects: {!r} and {!r}".format( 
                            src.aspect, 
                            dst.aspect 
                        )
                    )
                else:
                    dst_scale_aspect = dst 
                    
            elif isinstance(dst,Scale):
                # The initial aspect is applied to the result.
                dst_scale_aspect = ScaleAspect(dst,self.scale_aspect.aspect) 
            else:
                assert False, repr(dst)
            
            fn = cxt.conversion_from_scale_aspect( 
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid 
            )
            
            if fn is None:

                c = None 
                
                if (
                    self.scale_aspect.is_systematic 
                and dst_scale_aspect.is_systematic
                ):
                    c = self._systematic_src_dst_conversion(dst_scale_aspect)
                    
                if c is None and self.scale_aspect.is_systematic:
                    c = self._systematic_src_conversion(dst_scale_aspect)
                    
                elif c is None and dst.is_systematic:
                    c = self._systematic_dst_conversion(dst_scale_aspect)
                
                if c is None:
                    raise RuntimeError(
                        "cannot convert {} to {}".format(
                            self.scale_aspect,
                            dst_scale_aspect
                        )
                    )             
                else:            
                    fn = lambda x: c*x 
                
            new_token = fn(self._token)
        

        # Cases iii) and iv)  
        elif ( 
            isinstance(self.scale_aspect,CompoundScaleAspect)
        and isinstance(dst,(CompoundScale,CompoundScaleAspect) ) 
        ):
            # Conversion from compound to compound expressions.
            # The expressions must be arithmetically equivalent,  
            # so that pairs of source-destination scale-aspects  
            # can be found in the register. 
            
            # If the destination is a CompoundScale, 
            # the initial aspects are copied to the result.
                        
            # Step 1: convert to products of powers
            src_pops = normal_form(self.scale_aspect.stack)
            
            if isinstance(dst,CompoundScale):
                # Copy the src aspects to a new CompoundScaleAspect.
                dst_scale_aspect = dst._to_compound_scale_aspect( 
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
                if src_a_uid != dst_a_uid:
                    raise RuntimeError(
                        "aspects do not match: {!r} != {!r}".format(
                            src_a_uid,dst_a_uid
                        )
                    )

                c = cxt.conversion_from_scale_aspect( 
                        src_s_uid,src_a_uid,
                        dst_s_uid                     
                )(1.0) 
                conversion_factor *= c**src_exp
            
            new_token = conversion_factor*self._token
            
        # Case v)
        elif ( 
            isinstance(self.scale_aspect,CompoundScaleAspect)
        and isinstance(dst,(Scale,ScaleAspect) ) 
        ):
            # Conversion from a compound scale-aspect to a specific one.
            # We are limited to just the generic no_aspect. So this  
            # function must fail if there are any non-trivial aspects in 
            # the initial expression.
            _scales, _aspects = self.scale_aspect.to_compound_scales_and_aspects()           
            if not _aspects.no_aspect: 
                raise RuntimeError(
                    "conversion would loose aspect information {!r}".format(
                        self.scale_aspect
                    )
                )

            # The CompoundScaleAspect must reduce to a systematic scale 
            if not _scales.is_systematic: 
                raise RuntimeError(
                    "compound scale conversion is not supported for {!r}".format(
                        _scales
                    )
                )
            
            if isinstance(dst,Scale):            
                dst_scale_aspect = ScaleAspect(dst,no_aspect)
                
            elif isinstance(dst,ScaleAspect):
                if dst.aspect is not no_aspect:
                    # A cast would be required to change the aspect
                    raise RuntimeError(
                        "conversion cannot change the aspect: {!r}".format(dst)
                    ) 
                else:
                    dst_scale_aspect = dst 
            else:
                assert False, repr(dst) 
                            
            # Look for a direct match to dst 
            c = self._systematic_src_conversion(dst_scale_aspect)
            
            # Otherwise, if the destination scale is systematic
            # there may be a match.
            if c is None and dst_scale_aspect.is_systematic:         
                c = self._systematic_src_dst_conversion(dst_scale_aspect)
                
            if c is None:
                raise RuntimeError(
                    "cannot convert {} to {}".format(
                        self.scale_aspect,
                        dst_scale_aspect
                    )
                )             
            else:            
                new_token = c*self.token
            
        else:
            assert False
            
        return Expression(
            new_token,
            dst_scale_aspect
        )
        

    # ---------------------------------------------------------------------------
    def _systematic_src_casting(self,dst_scale_aspect):
    
        if isinstance(self.scale_aspect,CompoundScaleAspect):
            src_aspect = no_aspect
            src_systematic = self.scale_aspect.systematic.simplify 
        else:
            src_aspect = self.scale_aspect.aspect
            src_systematic = self.scale_aspect.systematic
            
        src_key = ( 
            (src_systematic.system,src_systematic.dimensions),
            src_aspect.uid
        )
        dst_key = dst_scale_aspect.uid
        
        if (src_key,dst_key) in cxt.dim_dst_cast_reg:
        
            set_of_scale_pairs = cxt.dim_dst_cast_reg[
                (src_key,dst_key)
            ]  
            
            src_scales, dst_scales = self._to_src_dst_lists( 
                set_of_scale_pairs 
            )
            ssrc = self._closest(src_systematic,src_scales)

            c = self._systematic_conversion_factor(
                src_systematic,ssrc.systematic
            )
            c *= cxt.cast_from_scale_aspect( 
                ssrc.uid,
                src_aspect.uid,
                dst_scale_aspect.scale.uid, 
                dst_scale_aspect.aspect.uid 
            )(1)
            
            return lambda x: c*x  
            
        else:
            return None
            
    # ---------------------------------------------------------------------------
    def _systematic_src_dst_casting(self,dst_scale_aspect):

        if isinstance(self.scale_aspect,CompoundScaleAspect):
            src_aspect = no_aspect
            src_systematic = self.scale_aspect.systematic.simplify 
        else:
            src_aspect = self.scale_aspect.aspect
            src_systematic = self.scale_aspect.systematic
            
        dst_systematic = dst_scale_aspect.scale.systematic
        dst_aspect = dst_scale_aspect.aspect
        
        src_key = (
            (src_systematic.system,src_systematic.dimensions),
            src_aspect.uid
        )
        dst_key = (
            (dst_systematic.system,dst_systematic.dimensions),
            dst_aspect.uid
        )
        
        if (src_key,dst_key) in cxt.dim_dim_cast_reg:
        
            set_of_scale_pairs = cxt.dim_dim_cast_reg[
                (src_key,dst_key)
            ]  

            src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
            ssrc = self._closest(src_systematic,src_scales)
            sdst = self._closest(dst_systematic,dst_scales)
            
            c = self._systematic_conversion_factor(
                src_systematic,ssrc.systematic
            )
            c *= self._systematic_conversion_fn(sdst,dst_scale)(1)
            c *= cxt.cast_from_scale_aspect( 
                ssrc.uid,
                src_aspect.uid,
                sdst.uid,
                dst_aspect.uid 
            )(1)
            
            return lambda x: c*x
            
        else:
            return None
 
    # ---------------------------------------------------------------------------
    def _systematic_dst_casting(self,dst_scale_aspect):
    
        if isinstance(self.scale_aspect,(CompoundScaleAspect,CompoundScale)):
            assert False, 'should not happen' 
        if isinstance(dst_scale_aspect,(CompoundScaleAspect,CompoundScale)):
            assert False, 'not implemented' 

        src_aspect = self.scale_aspect.aspect
        src_systematic = self.scale_aspect.systematic

        dst_scale = dst_scale_aspect.scale
        dst_systematic = dst_scale.systematic
        
        # Only look for direct match 
        src_key = self.scale_aspect.uid
        dst_key = (
            (dst_systematic.system,dst_systematic.dimensions), 
            dst_aspect.uid
        )
        
        if (src_key,dst_key) in cxt.src_dim_cast_reg:
            set_of_scale_pairs = cxt.src_dim_cast_reg[
                (src_key,dst_key)
            ] 
            
            src_pairs, dst_pairs = self._to_src_dst_lists( 
                set_of_scale_pairs 
            )
            sdst = self._closest(dst_systematic,dst_pairs)
            c = self._systematic_conversion_factor(
                sdst.systematic,dst_systematic
            )
            c *= cxt.cast_from_scale_aspect( 
                self.scale_aspect.uid,
                sdst.uid,
                dst_aspect.uid 
            )(1)
            return lambda x: c*x  
            
        else:
            return None
            
    # ---------------------------------------------------------------------------
    def cast(self,dst,aspect=no_aspect):
        """Return a new M-layer expression 
        
        Args:
        
            dst(:class:`~lib.ScaleAspect` or :class:`~lib.Scale`)
            aspect(:class:`~lib.Aspect`)  

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
                    dst_scale_aspect = ScaleAspect(
                        dst,
                        self.scale_aspect.aspect
                    )
                else:
                    dst_scale_aspect = ScaleAspect(dst,aspect)
                     
            elif isinstance(dst,ScaleAspect):
                if dst.aspect is no_aspect: 
                    if aspect is no_aspect:
                        # Carry forward the initial aspect
                        dst_scale_aspect = ScaleAspect(
                            dst.scale,
                            self.scale_aspect.aspect
                        )  
                    else:
                        # Replace 'no_aspect' in dst
                        dst_scale_aspect = ScaleAspect(
                            dst.scale,
                            aspect
                        )
                else:
                    dst_scale_aspect = dst
            else:
                assert False, repr(dst)
               
            fn = cxt.cast_from_scale_aspect(
                self.scale_aspect.scale.uid,
                self.scale_aspect.aspect.uid,
                dst_scale_aspect.scale.uid,
                dst_scale_aspect.aspect.uid 
            )
            if fn is None:  
                # Look at systematic possibilities
                if (
                    self.scale_aspect.is_systematic 
                and dst_scale_aspect.is_systematic
                ):
                    fn = self._systematic_src_dst_casting(dst)
                    
                if fn is None and self.scale_aspect.is_systematic:
                    fn = self._systematic_src_casting(dst)
                    
                elif fn is None and dst_scale_aspect.is_systematic:
                    fn = self._systematic_dst_casting(dst)
                
                if fn is None:
                    raise RuntimeError(
                        "cannot cast {} to {}".format(
                            self.scale_aspect,
                            dst_scale_aspect
                        )
                    )             

        elif isinstance(
            self.scale_aspect,(CompoundScale,CompoundScaleAspect)
        ):
            if not self.scale_aspect.is_systematic:
                # Unsupported at the moment
                raise RuntimeError(
                    "cannot cast from {} to {}".format(self.scale_aspect,dst)
                )
                
            if isinstance(dst,Scale):            
                if aspect is no_aspect:
                    dst_scale_aspect = ScaleAspect(dst,no_aspect)
                else:
                    dst_scale_aspect = ScaleAspect(dst,aspect)

            elif isinstance(dst,ScaleAspect):
                dst_scale_aspect = dst                
                
            else:
                assert False, repr(dst)

            src_systematic = self.scale_aspect.systematic.simplify                          
            
            # Try a match to dst first
            fn = self._systematic_src_casting(dst_scale_aspect)
            if fn is None and dst_scale_aspect.is_systematic:
                fn = self._systematic_src_dst_casting(dst_scale_aspect)                
            
            if fn is None:
                raise RuntimeError(
                    "cannot cast {} to {}".format(
                        self.scale_aspect,
                        dst_scale_aspect
                    )
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
    if isinstance(s,(ScaleAspect,CompoundScaleAspect)):
        return Expression(v,s)
    elif isinstance(s,Scale):
        return Expression(v, ScaleAspect(s,a) )
    elif isinstance(s,CompoundScale):
        return Expression(
            v, 
            s._to_compound_scale_aspect(a) 
         )
    else:
        assert False, "unexpected: {!r}, {!r}".format(s,a)
    
        

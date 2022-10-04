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
    def _closest(self,scale,scale_lst):
        """
        Find the Scale in ``scale_lst`` closest to ``scale`` in magnitude
        
        Args:
            scale (:class:`~lib.Scale`)
            scale_lst (sequence of :class:`~lib.Scale`)
            
        Returns:
            :class:`~lib.Scale`
            
        """
        dimension = scale.reference.dimension
        
        # The closest scale factor match
        factors = [
            abs( math.log10( s_i.dimension.prefix / dimension.prefix ) )
                for s_i in scale_lst
        ]
        idx = factors.index( min(factors) )
        
        return scale_lst[idx]
        
    #------------------------------------------------------------------------    
    def _systematic_conversion_factor(self,src,dst):
        """
        Return the conversion factor from ``src`` to ``dst`` 
        
        ``src`` and ``dst`` must both be systematic 
        and have the same dimensional exponents in 
        the same unit system.
        
        Args:
            src (:class:`Scale`)
            dst (:class:`Scale`)
        
        Returns:
            float
            
        """
        if src.systematic or dst.systematic:
            
            src_dim = src.reference.dimension 
            dst_dim = dst.reference.dimension
         
            if src_dim.system != dst_dim.system:
                raise RuntimeError(
                    "different systems: {!r}, {!r}".format(
                        src_dim.system,
                        dst_dim.system
                    )
                )
            
            if src_dim.dimensions != dst_dim.dimensions:
                raise RuntimeError(
                    "different dimensions: {!r}, {!r}".format(
                        src_dim.dimensions,
                        dst_dim.dimensions
                    )
                )
         
            return dst_dim.prefix / src_dim.prefix 
            
        else:
            raise RuntimeError(
                "no conversion from {!r} to {!r}".format(src,dst)
            )  
            
    # ---------------------------------------------------------------------------
    def _systematic_conversion(self,dst):
        assert isinstance(dst,Scale), repr(dst)
        
        # Systematic alternatives
        src = self.scale_aspect.scale
        if src.reference.systematic and dst.reference.systematic:
            src_dim = src.reference.dimension 
            dst_dim = dst.reference.dimension
            
            src_key = (src_dim.system,src_dim.dimensions)
            dst_key = (dst_dim.system,dst_dim.dimensions)
            
            if src_key == dst_key:
                c = src_dim.prefix / dst_dim.prefix 
                return lambda x: c*x
                
            try:
                set_of_scale_pairs = cxt.dim_dim_conversion_reg[
                    (src_key,dst_key)
                ]  
            except KeyError:
                raise RuntimeError(
                    "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                )
            else:
                src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
                if len(src_scales) == 0:
                    raise RuntimeError(
                        "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                    )
                
                ssrc = self._closest(self.scale_aspect.scale,src_scales)
                sdst = self._closest(dst_scale_aspect.scale,dst_scales)
                
                c = self._systematic_conversion_factor(src,ssrc)
                c *= self._systematic_conversion_factor(sdst,dst)
                c *= cxt.conversion_from_scale_aspect( 
                    ssrc.uid,
                    self.scale_aspect.aspect.uid,
                    sdst.uid 
                )(1)
                return lambda x: c*x
                
        elif src.reference.systematic:
            src_dim = src.reference.dimension 
            
            src_key = (src_dim.system,src_dim.dimensions)
            dst_key = dst.uid
            
            try:
                set_of_scale_pairs = cxt.dim_dst_conversion_reg[
                    (src_key,dst_key)
                ]                       
            except KeyError:
                raise RuntimeError(
                    "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                )
            else:
                src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
                if len(src_scales) == 0:
                    raise RuntimeError(
                        "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                    )

                ssrc = self._closest(self.scale_aspect.scale,src_scales)
                # Could check that dst is in dst_pairs 
                c = self._systematic_conversion_factor(src,ssrc)
                c *= cxt.conversion_from_scale_aspect( 
                    ssrc.uid,
                    self.scale_aspect.aspect.uid,
                    sdst_uid 
                )(1)
                return lambda x: c*x

        elif dst.reference.systematic:
            dst_dim = dst.reference.dimension
            
            src_key = self.scale_aspect.scale.uid
            dst_key = (dst_dim.system,dst_dim.dimensions)
            
            try:
                set_of_scale_pairs = cxt.src_dim_conversion_reg[
                    (src_key,dst_key)
                ]                       
            except KeyError:
                raise RuntimeError(
                    "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                )
            else:
                src_pairs, dst_pairs = self._to_src_dst_lists( set_of_scale_pairs )
                if len(src_pairs) == 0:
                    raise RuntimeError(
                        "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
                    )

                ssrc = self._closest(self.scale_aspect.scale,src_pairs)
                sdst = self._closest(dst_scale_aspect.scale,dst_pairs)
                c = self._systematic_conversion_factor(Scale(sdst_uid),dst)
                c *= cxt.conversion_from_scale_aspect( 
                    ssrc_uid,
                    self.scale_aspect.aspect.uid,
                    sdst_uid 
                )(1)
                return lambda x: c*x
        else:
            # Nothing worked         
            raise RuntimeError(
                "no conversion from {!r} to {!r}".format(self.scale_aspect,dst)
            ) 
            
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
            
            try:
                fn = cxt.conversion_from_scale_aspect( 
                    self.scale_aspect.scale.uid,
                    self.scale_aspect.aspect.uid,
                    dst_scale_aspect.scale.uid 
                )
            except RuntimeError:

                fn = self._systematic_conversion(dst)
                
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
            _aspects = self.scale_aspect.to_compound_scales_and_aspects()[1]
            
            if not _aspects.no_aspect: 
                raise RuntimeError(
                    "conversion would loose aspect information {!r}".format(
                        self.scale_aspect
                    )
                )
                
            if isinstance(dst,Scale):            
                dst_scale_aspect = ScaleAspect(dst,no_aspect)
                
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
                    "dimensions must match: {!r}, {!r}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
                )           
                        
            # new_token = cxt.dim_dst_conversion_reg( 
                # src_dim,
                # dst_scale_aspect.scale.uid 
            # )(self._token)

                
            try:
                set_of_scale_pairs = cxt.dim_dst_conversion_reg[
                    (src_dim.system,src_dim.dimensions),
                    dst_scale_aspect.scale.uid
                ]  
            except KeyError:
                raise RuntimeError(
                    "unable to convert {} to {}".format(src_dim,dst)
                )
            else:
                src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
                ssrc = self._closest(src_scale,src_scales)
                
                c = self._systematic_conversion(src_scale,ssrc)
                c *= self._systematic_conversion(sdst,dst_scale)
                c *= cxt.convert_from_scale_aspect( 
                    ssrc.uid,
                    dst_scale_aspect.scale.uid 
                )(1)
                new_token *= c
            
        # elif ( 
            # isinstance(self.scale_aspect,CompoundScale)
        # and isinstance(dst,CompoundScale ) 
        # ):
            # # This is the generic case, where no aspect is available
            
            # # The expressions must be arithmetically equivalent,  
            # # so that pairs of source-destination scales  
            # # can be found in the register. 
                        
            # # Step 1: convert to products of powers
            # src_pops = normal_form(self.scale_aspect.stack)            
            # dst_pops = normal_form(dst.stack)         
            
            # # Step 2: take into account any stand-alone numerical factors
            # conversion_factor = src_pops.prefactor/dst_pops.prefactor
            
            # # Step 3: step through the scale terms,
            # # obtaining a conversion factor for each
            # src_factors = src_pops.factors
            # dst_factors = dst_pops.factors
            # for src_i,dst_i in zip(src_factors.keys(),dst_factors.keys()):
            
                # # Each term also has an exponent
                # src_exp = src_factors[src_i]
                # assert src_exp == dst_factors[dst_i],\
                    # "{} != {}".format(src_exp,dst_factors[dst_i])

                # src_s_uid = src_i.uid
                # dst_s_uid = dst_i.uid
                # src_a_uid = no_aspect.uid

                # c = cxt.conversion_from_scale_aspect( 
                        # src_s_uid,src_a_uid,dst_s_uid                     
                # )(1.0) 
                # conversion_factor *= c**src_exp
            
            # new_token = conversion_factor*self._token
 
            # # Set the aspect component of the new CompoundScaleAspect
            # # to the default value.
            # dst_scale_aspect = dst._to_compound_scale_aspect() 
 
        # elif ( 
            # isinstance(self.scale_aspect,CompoundScale)
        # and isinstance(dst,(Scale,ScaleAspect) ) 
        # ):
            # # To convert from a compound scale, to a specific one,
            # # the compound scale must be dimensionally equivalent 
            # # to the final scale, which must not have an aspect.             
                
            # if isinstance(dst,ScaleAspect):
                # if dst.aspect is not no_aspect:
                    # raise RuntimeError(
                        # "conversion cannot change from ``no_aspect`` "
                        # "to {!r}".format(dst.aspect)
                    # ) 
                # else:
                    # dst_scale_aspect = dst 
                    
            # elif isinstance(dst,Scale):            
                # dst_scale_aspect = ScaleAspect(dst,no_aspect)
                
            # else:
                # assert False, repr(dst) 
                
            # # TODO: 
            # # A pair of commensurate systematic units 
            # # can always be converted. However, we need
            # # an exact match otherwise.
            # src_dim = self.scale_aspect.dimension.simplify     
            # if self.scale_aspect.systematic and dst.systematic:
                # if not src_dim.commensurate(dst.dimension):
                    # raise RuntimeError(
                        # "incommensurate dimensions: {}, {}".format(
                        # src_dim, dst.dimension
                    # )
                # else:
                    # new_token = cxt.systematic_conversion(
                        # src_dim,
                        # dst_scale_aspect.scale.uid
                    # )(self._token)
                    
            # elif src_dim != dst_scale_aspect.dimension:
                # raise RuntimeError(
                    # "dimensions do not match: {}, {}".format(
                        # src_dim,
                        # dst_scale_aspect.dimension
                    # )
                # )           
                        
                # new_token = cxt.conversion_from_dim( 
                    # src_dim,
                    # dst_scale_aspect.scale.uid 
                # )(self._token)

        else:
            assert False
            
        return Expression(
            new_token,
            dst_scale_aspect
        )
        

    # ---------------------------------------------------------------------------
    def _systematic_casting(self,dst):
        # Systematic alternatives
        
        src_scale = self.scale_aspect.scale
        src_aspect = self.scale_aspect.aspect
        dst_scale = dst.scale 
        dst_aspect = dst.aspect
        
        if src_scale.systematic and dst_scale.systematic:
        
            src_dim = src_scale.dimension 
            dst_dim = dst_scale.dimension
            
            src_key = ((src_dim.system,src_dim.dimensions),src_aspect.uid)
            dst_key = ((dst_dim.system,dst_dim.dimensions),dst_aspect.uid)
            
            try:
                set_of_scale_pairs = cxt.dim_dim_cast_reg[
                    (src_key,dst_key)
                ]  
            except KeyError:
                raise RuntimeError(
                    "unable to cast {} to {}".format(self.scale_aspect,dst)
                )
            else:
                src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
                ssrc = self._closest(src_scale,src_scales)
                sdst = self._closest(dst_scale,dst_scales)
                
                c = self._systematic_conversion(src_scale,ssrc)
                c *= self._systematic_conversion(sdst,dst_scale)
                c *= cxt.cast_from_scale_aspect( 
                    ssrc.uid,src_aspect.uid,
                    sdst.uid,dst_aspect.uid 
                )(1)
                return lambda x: c*x
                
        elif src_scale.systematic:
            src_dim = src_scale.dimension   
            
            src_key = ((src_dim.system,src_dim.dimensions),src_aspect.uid)
            dst_key = dst_scale_aspect.uid
            
            try:
                set_of_scale_pairs = cxt.dim_dst_cast_reg[
                    (src_key,dst_key)
                ]                       
            except KeyError:
                raise RuntimeError(
                    "unable to cast {} to {}".format(self.scale_aspect,dst)
                )
            else:
                src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
                ssrc = self._closest(src_scale,src_scales)
                # Could check that dst is in dst_pairs 
                c = self._systematic_conversion(src_scale,ssrc)
                c *= cxt.cast_from_scale_aspect( 
                    ssrc.uid,src_aspect.uid,
                    dst_scale_aspect.uid 
                )(1)
                return lambda x: c*x 

        elif dst_scale.systematic:
            dst_dim = dst_scale.dimension
            
            src_key = self.scale_aspect.uid
            dst_key = ((dst_dim.system,dst_dim.dimensions), dst_aspect.uid)
            
            try:
                set_of_scale_pairs = cxt.src_dim_cast_reg[
                    (src_key,dst_key)
                ]                       
            except KeyError:
                raise RuntimeError(
                    "unable to cast {} to {}".format(self.scale_aspect,dst)
                )
            else:
                src_pairs, dst_pairs = self._to_src_dst_lists( set_of_scale_pairs )
                ssrc = self._closest(self.scale_aspect.scale,src_pairs)
                sdst = self._closest(dst_scale_aspect.scale,dst_pairs)
                c = self._systematic_conversion(Scale(sdst_uid),dst)
                c *= cxt.cast_from_scale_aspect( 
                    self.scale_aspect.uid,
                    sdst.uid,dst_aspect.uid 
                )(1)
                return lambda x: c*x
        else:
            # Nothing worked         
            raise RuntimeError(
                "unable to cast {} to {}".format(self.scale_aspect,dst)
            ) 
 
    # ---------------------------------------------------------------------------
    def _systematic_src_casting(self,src_dimension,dst_scale_aspect):
        from m_layer.dimension import Dimension
        assert isinstance(src_dimension,Dimension), repr(src_dimension)
        
        dst_key = dst_scale_aspect.uid
        src_key = (src_dimension.system,src_dimension.dimensions)
        
        set_of_scale_pairs = set()
        
        try:
            set_of_scale_pairs = cxt.dim_dst_cast_reg[
                (src_key,dst_key)
            ]                       
        except KeyError:
            pass

        try:
            set_of_scale_pairs = cxt.dim_dst_for_aspect_reg[
                dst_scale_aspect.aspect.uid][
                    (src_key,dst_scale_aspect.scale.uid)
                ]                                 
        except KeyError:
            pass
        
        if len(set_of_scale_pairs) == 0:
            raise RuntimeError(
                "unable to cast {} to {}".format(
                    self.scale_aspect,dst_scale_aspect
                )
            )
            
        src_scales, dst_scales = self._to_src_dst_lists( set_of_scale_pairs )
        if not len(src_scales) or dst_scale_aspect.scale not in dst_scales:
            raise RuntimeError(
                "unable to cast {} to {}".format(
                    self.scale_aspect,
                    dst_scale_aspect
                )
            )
        
        # No way to choose
        ssrc = src_scales.pop()
        
        c = src_dimension.prefix
        c *= cxt.cast_from_scale_aspect( 
            ssrc.uid,no_aspect.uid,
            dst_scale_aspect.scale.uid, 
            dst_scale_aspect.aspect.uid, 
        )(1)
        return lambda x: c*x 
            
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
               
            try:
                fn = cxt.cast_from_scale_aspect(
                    self.scale_aspect.scale.uid,
                    self.scale_aspect.aspect.uid,
                    dst_scale_aspect.scale.uid,
                    dst_scale_aspect.aspect.uid 
                )
            except RuntimeError:            
                fn = self._systematic_casting(dst_scale_aspect)

        elif isinstance(
            self.scale_aspect,(CompoundScale,CompoundScaleAspect)
        ):
            if not self.scale_aspect.systematic:
                raise RuntimeError(
                    "cannot cast from {} to {}".format(self.scale_aspect,dst)
                )
                
            src_dim = self.scale_aspect.dimension.simplify            
            if src_dim != dst.dimension:
                raise RuntimeError(
                    "dimensions do not match: {}, {}".format(
                        src_dim,
                        dst_scale_aspect.dimension
                    )
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
            
            fn = self._systematic_src_casting(src_dim,dst_scale_aspect)
           
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
    
        

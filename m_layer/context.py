"""
The Context is an interface between external M-layer registers 
and the local Python session where the M-layer is being used.

"""
import json 
import glob

from m_layer import register 
from m_layer import conversion_register
from m_layer import casting_register
from m_layer import scales_for_aspect_register

__all__ = (
    'Context',
    'default_context',
)

# ---------------------------------------------------------------------------
def uid_as_str(uid,short=True):
    """
    Shorten the number of digits in the UUID for human readers, 
    because the chances of a collision in just a few digits is small.
    
    """
    s = str( uid )
    return "{}...".format(s[:6]) if short else s 
          

# ---------------------------------------------------------------------------
class Context(object):
    
    """
    A `Context` object contains M-layer records for aspects, scales, 
    conversions, casting, and conventional references. 
    """
    
    def __init__(
            self,
            locale = 'default',
            value_fmt = "{:.5f}",
            scale_reg = None,
            reference_reg = None,
            aspect_reg = None,
            conversion_reg = None,
            casting_reg = None,
            scales_for_aspect_reg = None
            
        ):
        self.locale = locale 
        self.value_fmt = value_fmt
        
        if scale_reg is None:
            self.scale_reg = register.Register(self)
        else:
            self.scale_reg = scale_reg
        
        if reference_reg is None:
            self.reference_reg = register.Register(self)
        else:
            self.reference_reg = reference_reg
        
        if aspect_reg is None:
            self.aspect_reg = register.Register(self)
        else:
            self.aspect_reg = aspect_reg

        if conversion_reg is None:
            self.conversion_reg = conversion_register.ConversionRegister(self)
        else:
            self.conversion_reg = conversion_reg

        if casting_reg is None:
            self.casting_reg = casting_register.CastingRegister(self)
        else:
            self.casting_reg = casting_reg

        if scales_for_aspect_reg is None:
            self.scales_for_aspect_reg =\
                scales_for_aspect_register.ScalesForAspectRegister(self)
        else:
            self.scales_for_aspect_reg = scales_for_aspect_reg


    def _load_entity(self,entity):
        entity_type = entity['__entry__']
        if entity_type == "Reference":
            self.reference_reg.set(entity)
        elif entity_type == "Aspect":
            self.aspect_reg.set(entity)
        elif entity_type == "Scale":
            self.scale_reg.set(entity)
        elif entity_type == "Conversion":
            self.conversion_reg.set(entity)
        elif entity_type == "Cast":
            self.casting_reg.set(entity)
        elif entity_type == "ScalesForAspect":
            self.scales_for_aspect_reg.set(entity)
        else:
            raise RuntimeError(
               "unknown type: {}".format(entity_type)
            )
        
    def _loader(self,data):
        # A single entity will be presented as a dict
        # A json array is a list.
        if isinstance(data,list):
            for l_i in data:
                self._load_entity(l_i)
        else:       
            self._load_entity(data)
            
    def loads(self,json_str,**kwargs):
        data = json.loads(json_str,**kwargs)
        self._loader(data)
            
    def load_json(self,file_path,**kwargs):
        with open(file_path,'r') as f:
            data = json.load(f,**kwargs)        
        self._loader(data)
 
    def load(self,path,**kwargs):
        """
        Called to initialise internal M-layer records
        
        Args:
            path: an expression to glob M-layer JSON files 
            **kwargs: keyword arguments passed to glob
            
        """
        for f_json in glob.glob( path ):
            try:
                default_context.load_json( f_json, **kwargs )
            except json.decoder.JSONDecodeError as e:
                # Report errors but do not stop execution
                print("json.decoder.JSONDecodeError",e, 'in:',f_json)
 
    @property
    def locale(self):
        return self._locale 
        
    @locale.setter
    def locale(self,l):
        self._locale = l 
  
    # def conversion_fn(self,src_expr,dst_scale):
    def conversion_fn(self,src_scale_uid,src_aspect_uid,dst_scale_uid):
        """
        Return a function that converts a value expressed 
        in the `src` scale and aspect to one in the `dst` scale.
        
        The aspect does not change.  
        
        Args:
            src_scale_uid (unique m-layer identifier): initial scale   
            src_aspect_uid (unique m-layer identifier): initial aspect
            dst_scale_uid (unique m-layer identifier): final scale
        
        Returns:
            A Python function 
            
        """                
        scale_pair = (src_scale_uid,dst_scale_uid)
        
        # Note, the register should probably not allow an aspect-free conversion 
        # to be defined when there is already an aspect-specific one defined.
        # However, by doing the aspect-specific look-up first, this implementation
        # will allow multiple definitions to coexist and give precedence to 
        # aspect-specific definitions.
        
        # Has an aspect argument been given that restricts conversions?
        # Look first in the aspect-specific conversion table
        if( src_aspect_uid is not None 
        and src_aspect_uid in self.scales_for_aspect_reg
        ):
            scales_for_aspect = self.scales_for_aspect_reg[src_aspect_uid]
            try:
                return scales_for_aspect[scale_pair]
            except KeyError:
                pass
                
        # Aspect-free conversions are possible
        try:
            return self.conversion_reg[scale_pair] 
        except KeyError:
            pass
                        
        # This is a failure 
        if src_aspect_uid is None:
            raise RuntimeError(
                "no conversion from Scale({!r}) to Scale({!r})".format(
                    src_scale_uid,
                    dst_scale_uid
                )
            )
        else:
            raise RuntimeError(
                "no conversion from Scale({!r}) to Scale({!r}) for Aspect{!r}".format(
                    src_scale_uid,
                    dst_scale_uid,
                    src_aspect_uid
                )
            )

    def casting_fn(
        self,
        src_scale_uid, src_aspect_uid,
        dst_scale_uid, dst_aspect_uid
    ):
        """
        Return a function that transforms the initial expression 
        to an expression in terms of a different scale and aspect.
        
        If the initial expression does not specify an aspect,
        ``dst_aspect_uid`` is assumed to apply to both.
        
        Args:
            src_scale_uid (unique m-layer identifier): initial scale   
            src_aspect_uid (unique m-layer identifier): initial aspect
            dst_scale_uid (unique m-layer identifier): final scale
            dst_aspect_uid (unique m-layer identifier): final aspect
            
        Returns:
            A Python function 
            
        """ 
        dst_pair = dst_scale_uid, dst_aspect_uid
        
        if src_aspect_uid is None:
            src_pair = src_scale_uid, dst_aspect_uid 
        else:
            src_pair = src_scale_uid, src_aspect_uid    
          
        if src_pair[1] == dst_pair[1]:
        
            # Look for aspect-specific conversions first
            scales_for_aspect = self.scales_for_aspect_reg[ dst_aspect_uid ]
            try:
                return scales_for_aspect[ (src_scale_uid, dst_scale_uid) ]
            except KeyError:
                pass
            
        try:
            return self.casting_reg[ (src_pair,dst_pair) ]   
        except KeyError:
            raise RuntimeError(
                "no cast defined from '{!r}' to '{!r}'".format(
                    src_pair,
                    dst_pair
                )
            ) from None          

# ---------------------------------------------------------------------------
# Configure a default context object by reading all JSON files
# in the directories.
#
import os.path

default_context = Context()

for p_i in (
        r'json/references', 
        r'json/scales',
        r'json/conversion',
        r'json/casting',
        r'json/aspects',
        r'json/scales_for'
    ):
    path = os.path.join( 
        os.path.dirname(__file__), 
        p_i, 
        r'*.json'
    )
    default_context.load(path)


# ===========================================================================
    
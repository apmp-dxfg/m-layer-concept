# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
    A `Context` contains information about aspects, scales, conversions,
    and conventional references that provide contextual information about 
    `AspectValue` objects. 
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
        entity_type = entity['__type__']
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
        """
        """
        data = json.loads(json_str,**kwargs)
        self._loader(data)
            
    def load_json(self,file_path,**kwargs):
        with open(file_path,'r') as f:
            data = json.load(f,**kwargs)        
        self._loader(data)
 
    def load(self,path,**kwargs):
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
        
    def conversion_fn(self,src_exp,dst_scale_id):
        """
        Return a function to convert the value in `src_exp` 
        to a different expression in terms of `dst_scale_id`.
        
        """                
        scale_uid_pair = (src_exp._scale,dst_scale_id)
        
        # If there is a pair of scales in the register
        # then use it without checking aspect.
        fn = self.conversion_reg.get( scale_uid_pair ) 
        
        if fn is not None: 
            return fn
                
        else:    
            # If the first search fails, look for  
            # conversions that are aspect-specific 
            # (e.g., wavenumber to frequency for photon energy)
        
            # Has an aspect has been declared?
            _aspect = src_exp._aspect
            if( _aspect is not None 
            and _aspect in self.scales_for_aspect_reg
            ):
                fn = self.scales_for_aspect_reg.get(
                    _aspect, 
                    scale_uid_pair, 
                    None 
                )
            
                if fn is not None:
                    return fn
            
        # This is a failure    
        raise RuntimeError(
            "no conversion for '{!r}' to '{!r}'".format(
                src_exp,
                dst_scale_id
            )
        )

    def casting_fn(self,src_exp,dst_scale_aspect):
        """
        Return a function to cast the value in `src_exp` to a 
        different scale and aspect.
        
        """        
        src_scale_aspect = (src_exp._scale,src_exp._aspect)
                        
        try:
            return self.casting_reg[ (src_scale_aspect,dst_scale_aspect) ]
            
        except KeyError:
            raise RuntimeError(
                "no cast defined from '{!r}' to '{!r}'".format(
                    src_scale_aspect,
                    dst_scale_aspect
                )
            )            

# ---------------------------------------------------------------------------
# Configure a default context object by reading all JSON files
# in the directories.
#
import os.path

default_context = Context()

for p_i in (
        r'json/references', 
        r'json/scales',
        r'json/conversion_casting',
        r'json/aspects',
        r'json/scales_for_aspects'
    ):
    path = os.path.join( 
        os.path.dirname(__file__), 
        p_i, 
        r'*.json'
    )
    default_context.load(path)


# ===========================================================================
    
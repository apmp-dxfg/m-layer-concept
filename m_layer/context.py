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
        
    def conversion_fn(self,src_scale,dst_scale,aspect=None):
        """
        Return a function to convert a value expressed 
        in `src_scale` to an expression in terms of `dst_scale`.
        
        The ``aspect`` argument extends the search to
        aspect-specific conversion definitions.  
        
        Args:
            src_scale (:class:`~scale.Scale`): the initial scale 
            dst_scale (:class:`~scale.Scale`): the final scale
            aspect (:class:`~aspect.Aspect`, optional): the aspect for scales
        
        Returns:
            A Python function 
            
        """                
        scale_pair = (src_scale.uid,dst_scale.uid)
        
        # Note, the register should probably not allow an aspect-free conversion 
        # to be defined when there is already an aspect-specific one defined.
        # However, by doing the aspect-specific look-up first, this implementation
        # will allow multiple definitions to coexist and give precedence to 
        # aspect-specific definitions.
        
        # Has an aspect argument been given that restricts conversions?
        # Look first in the aspect-specific conversion table
        if( aspect is not None 
        and aspect.uid in self.scales_for_aspect_reg
        ):
            scales_for_aspect = self.scales_for_aspect_reg[aspect.uid]
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
        if aspect is None:
            raise RuntimeError(
                "no conversion from {!r} to {!r}".format(
                    src_scale,
                    dst_scale
                )
            )
        else:
            raise RuntimeError(
                "no conversion from {!r} to {!r} for {!r}".format(
                    src_scale,
                    dst_scale,
                    aspect
                )
            )

    def casting_fn(self,src_exp,dst_scale_aspect):
        """
        Return a function to cast the value of ``src_exp`` to an
        expression in ``dst_scale_aspect``.
        
        Args:
            src_exp (:class:`~expression.Expression`): the initial expression
            dst_scale_aspect (:class:`scale_aspect.ScaleAspect`): the scale-aspect pair for the final expression
            
        Returns:
            A Python function 
            
        """        
        src_pair = src_exp.scale_aspect.uid     # scale-aspect pair
        dst_pair = dst_scale_aspect.uid         # scale-aspect pair
        
        try:
            return self.casting_reg[ (src_pair,dst_pair) ]
            
        except KeyError:
            raise RuntimeError(
                "no cast defined from '{!r}' to '{!r}'".format(
                    src_pair,
                    dst_pair
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
    
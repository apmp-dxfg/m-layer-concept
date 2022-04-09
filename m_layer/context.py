# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import json 
import os.path

from m_layer import scale_register 
from m_layer import reference_register 
from m_layer import conversion_register 
from m_layer import aspect_register 

__all__ = (
    'Context',
    'default_context'
)

# ---------------------------------------------------------------------------
class Context(object):
    
    """
    """
    
    def __init__(
            self,
            locale = 'default',
            scale_reg = None,
            reference_reg = None,
            aspect_reg = None,
            conversion_reg = None
        ):
        self.locale = locale 
        
        if scale_reg is None:
            self.scale_reg = scale_register.ScaleRegister(self)
        else:
            self.scale_reg = scale_reg
        
        if reference_reg is None:
            self.reference_reg = reference_register.ReferenceRegister(self)
        else:
            self.reference_reg = reference_reg
        
        if aspect_reg is None:
            self.aspect_reg = aspect_register.AspectRegister(self)
        else:
            self.aspect_reg = aspect_reg

        if conversion_reg is None:
            self.conversion_reg = conversion_register.ConversionRegister(self)
        else:
            self.conversion_reg = conversion_reg

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
        else:
            raise RuntimeError(
               "unknown type: {}".format(entity_type)
            )
        
    def _loader(self,data):
        # A single entity in json will be presented as a dict
        # A json array will be presented as a list.
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
            
    def load(self,file_path,**kwargs):
        with open(file_path,'r') as f:
            data = json.load(f,**kwargs)        
        self._loader(data)
        
    @property
    def locale(self):
        return self._locale 
        
    @locale.setter
    def locale(self,l):
        self._locale = l 
        
    def conversion_fn(self,src_av,dst_ml_ref_id):
        """
        """        
        # The aspect will stay the same
        aspect_id = src_av._aspect
        
        # The M-layer extended reference 
        src_ml_ref_id = src_av._ml_ref
                
        table = self.conversion_reg
        if (src_ml_ref_id,dst_ml_ref_id) not in table:
            raise RuntimeError(
                "no conversion from '{}' to '{}'".format(
                    src_ml_ref_id[0],
                    dst_ml_ref_id[0]
                )
            )
        else:
            return table[ (src_ml_ref_id,dst_ml_ref_id) ]
                
        
# ---------------------------------------------------------------------------
# Configure a default context object
#
default_context = Context()

path = os.path.join( os.path.dirname(__file__),'json')

default_context.load(os.path.join(path,'scales.json'))
default_context.load(os.path.join(path,'aspects.json'))
default_context.load(os.path.join(path,'references.json'))

# ===========================================================================
if __name__ == '__main__':
    
    pass 
    
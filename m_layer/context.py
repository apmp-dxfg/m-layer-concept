"""
The Context provides a local interface to external M-layer registers.
The Context is not intended to be used directly in applications.
"""
import json 
import glob
import os.path

from m_layer import register 
from m_layer import conversion_register
from m_layer import casting_register
from m_layer import scales_for_aspect_register

from m_layer.uid import UID 

__all__ = ('global_context', )

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
    A `Context` provide a Python interface to M-layer registry records. 
    """
    
    def __init__(
            self,
            locale = 'default',
            scale_reg = None,
            reference_reg = None,
            aspect_reg = None,
            conversion_reg = None,
            casting_reg = None,
            scales_for_aspect_reg = None,
            system_reg = None
            
        ):   
        
        # Default inputs are used at the moment, but the 
        # idea is perhaps to allow contextual information 
        # to be built up over several registries.
        
        self.locale = locale 
        
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
                
        if system_reg is None:
            self.system_reg = register.Register(self)
        else:
            self.system_reg = reference_reg
            

    def _load_entity(self,entity):
        # Handles one JSON object
        
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
        elif entity_type == "UnitSystem":
            self.system_reg.set(entity)
        else:
            raise RuntimeError(
               "unknown type: {}".format(entity_type)
            )

    def _loader(self,data):
        # A JSON object is a dict
        # A JSON array of objects is a list.
        if isinstance(data,list):
            for l_i in data:
                self._load_entity(l_i)
        else:       
            self._load_entity(data)
            
    def load_json(self,file_path,**kwargs):
        with open(file_path,'r') as f:
            data = json.load(f,**kwargs)        
        self._loader(data)
 
    def load(self,type_dir,**kwargs):
        """
        Called to initialise internal M-layer records
        
        Args:
            path: an expression to glob M-layer JSON files 
            **kwargs: keyword arguments passed to glob
            
        """
        for f_json in glob.glob( "**/*.json",root_dir=type_dir,recursive=True ):

            f_i = os.path.join(type_dir,f_json)
            try:
                self.load_json( f_i, **kwargs )
            except json.decoder.JSONDecodeError as e:
                # Report errors but do not stop execution
                print("json.decoder.JSONDecodeError",e, 'in:',f_i)
 
    @property
    def locale(self):
        return self._locale 
        
    @locale.setter
    def locale(self,l):
        self._locale = l 
    
    # -----------------------------------------------------------------------
    def convertible(
            self,
            src_scale_uid,src_aspect_uid,
            dst_scale_uid
        ):
        """
        Raise ``RuntimeError`` if there is not a registered conversion  
        from the source scale and aspect to the destination scale. 
        
        """
        assert isinstance(src_scale_uid,UID), repr(src_scale_uid)
        assert isinstance(src_aspect_uid,UID), repr(src_aspect_uid)
        assert isinstance(dst_scale_uid,UID), repr(dst_scale_uid)

        if src_scale_uid == dst_scale_uid:
            return True
            
        scale_pair = (src_scale_uid,dst_scale_uid)
        
        if( 
            src_aspect_uid != self.no_aspect_uid
        and 
            src_aspect_uid in self.scales_for_aspect_reg
        ):
            if src_aspect_uid in self.scales_for_aspect_reg:
                scales_for_aspect = self.scales_for_aspect_reg[src_aspect_uid]
                if scale_pair in scales_for_aspect:
                    return True

        if scale_pair in self.conversion_reg: 
            return True
                        
        # Otherwise it's a failure 
        if src_aspect_uid == self.no_aspect_uid:
            msg = "no conversion from {} to {}".format(
                    src_scale_uid,
                    dst_scale_uid
                )
        else:
            msg = "no conversion from {} to {} for {}".format(
                    src_scale_uid,
                    dst_scale_uid,
                    src_aspect_uid
                )
         
        raise RuntimeError(msg)
         
    #------------------------------------------------------------------------    
    def conversion_from_scale_aspect(
        self,
        src_scale_uid,
        src_aspect_uid,
        dst_scale_uid
    ):
        """
        Return a function to convert data expressed 
        in the `src` scale and aspect to the `dst` scale.
        
        The aspect does not change.  
        
        Args:
            src_scale_uid: initial scale   
            src_aspect_uid: initial aspect
            dst_scale_uid: final scale
        
        Returns:
            A Python function or ``None``
            
        """ 
        assert isinstance(src_scale_uid,UID), repr(src_scale_uid)
        assert isinstance(src_aspect_uid,UID), repr(src_aspect_uid)
        assert isinstance(dst_scale_uid,UID), repr(dst_scale_uid)
        
        if src_scale_uid == dst_scale_uid:
            # Trivial case where no conversion is required
            return lambda x: x
            
        scale_pair = (src_scale_uid,dst_scale_uid)
        
        # Doing the aspect-specific look-up first, makes
        # multiple definitions possible with precedence  
        # given to aspect-specific cases.
        
        if( 
            src_aspect_uid != self.no_aspect_uid 
        and 
            src_aspect_uid in self.scales_for_aspect_reg
        ):
            scales_for_aspect = self.scales_for_aspect_reg[src_aspect_uid]
            try:
                return scales_for_aspect[scale_pair]
            except KeyError:
                pass
                
        # If a generic conversion is available it can be used 
        # in which case the initial aspect is carried forward.
        try:
            return self.conversion_reg[scale_pair] 
        except KeyError:
            pass
                        
        # Otherwise it's a failure 
        return None 

    #------------------------------------------------------------------------    
    def cast_from_scale_aspect(
        self,
        src_scale_uid, src_aspect_uid,
        dst_scale_uid, dst_aspect_uid
    ):
        """
        Return a function to transform data on an initial scale-aspect  
        to a different scale and aspect.
        
        Args:
            src_scale_uid: initial scale   
            src_aspect_uid: initial aspect
            dst_scale_uid: final scale
            dst_aspect_uid: final aspect
            
        Returns:
            A Python function or ``None``
            
        When the initial and final aspect is the same 
        and no cast has been defined, a matching 
        conversion will be used.   

        When the initial aspect is unspecified, an 
        aspect-specific conversion can be used.
            
        """ 
        src_pair = src_scale_uid, src_aspect_uid    
        dst_pair = dst_scale_uid, dst_aspect_uid
        
        # First, is there an exact match?
        try:
            return self.casting_reg[ src_pair,dst_pair ]   
        except KeyError:
            pass 
 
        # Is there a match after replacing the source aspect?
        if src_aspect_uid == self.no_aspect_uid:
            try:
                return self.casting_reg[ 
                    (src_scale_uid, dst_aspect_uid),
                    dst_pair 
                ]   
            except KeyError:
                pass 
 
        # No registered casting found, but conversions may apply
        if src_aspect_uid == self.no_aspect_uid:
            
            if src_scale_uid == dst_scale_uid:
                # Accept the dst aspect without question
                # This is the same as defining a ScaleAspect using
                # a Scale and an aspect.
                return lambda x: x 
                         
        # A conversion may be possible for a common aspect.
        # Or casting may promote an unspecified aspect to the final aspect.
        if src_aspect_uid == self.no_aspect_uid or src_aspect_uid == dst_aspect_uid:   
        
            # Aspect-specific conversions
            try:
                scales_for_aspect = self.scales_for_aspect_reg[ dst_aspect_uid ]
                return scales_for_aspect[ (src_scale_uid, dst_scale_uid) ]
            except KeyError:
                pass
                
        if src_aspect_uid == dst_aspect_uid:
            # If the aspect is not changing,
            # generic conversions are legitimate
            try: 
                return self.conversion_reg[ (src_scale_uid, dst_scale_uid) ]
            except KeyError:
                pass
                
        # Everything failed
        return None

# ---------------------------------------------------------------------------
# Configure the global context object 
#
_dir = os.path.dirname(__file__)

global_context = Context()
"""The Context object used during a Python session"""

for p_i in (
        r'json/references', 
        r'json/scales',
        r'json/conversion',
        r'json/casting',
        r'json/aspects',
        r'json/scales_for',
        r'json/systems'
    ):
    global_context.load( os.path.join(_dir,p_i) )

# The `no_aspect` entry is special, we need the uid
file_path = os.path.join( _dir, r'json/aspects/no_aspect.json' )
assert os.path.isfile( file_path ), repr( file_path )

with open(file_path,'r') as f:
    data = json.load(f)        

global_context.no_aspect_uid = UID( data[0]['uid'] )   
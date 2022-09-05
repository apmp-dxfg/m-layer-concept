from ast import literal_eval

from m_layer.context import default_context as cxt
from m_layer.uid import UID
from m_layer.system import System

# ---------------------------------------------------------------------------
class Reference(object):

    slots = ( 'uid', '_json_entry', '_dimension'  )
    
    def __init__(self,json_uid):
    
        # This provides access to the JSON entry
        self.uid = UID(json_uid)
        self._json_entry = cxt.reference_reg[self.uid]


    def __hash__(self):
        # M-layer objects are equivalent
        return hash(self.uid)
    
    def __repr__(self):
        return "Reference({})".format(self.uid)
    
    def __str__(self):    
        return self._json_entry['locale']['default']['symbol'] 
        
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
        
            to_dim_tuple = lambda x: tuple( literal_eval(x) )
            
            # The JSON prefix is a pair of string-formatted
            # integers for the numerator and denominator
            to_prefix_tuple = lambda x: tuple( 
                int( literal_eval(i) ) 
                    for i in literal_eval(x) 
            )

            _json = self._json_entry
            
            if 'system' in _json:
                self._dimension = Dimension( 
                    System( UID( _json['system']['uid'] ) ),
                    to_dim_tuple( _json['system']['dimensions'] ),
                    to_prefix_tuple( _json['system']['prefix'] )
                )
                return self._dimension 
                
            else:
                raise RuntimeError("No dimension for {!r}".format(self))
            
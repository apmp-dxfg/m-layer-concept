from ast import literal_eval

from m_layer.context import default_context as cxt
from m_layer.uid import UID
from m_layer.system import System
from m_layer.dimension import Dimension

__all__ = (
    'Reference',
)

# ---------------------------------------------------------------------------
def entry_to_dimension(json_ref):
    """
    """
    to_dim_tuple = lambda x: tuple( literal_eval(x) )
    
    # The JSON prefix is a pair of string-formatted
    # integers for the numerator and denominator
    to_prefix_tuple = lambda x: tuple( 
        int( literal_eval(i) ) for i in x 
    )

    if 'system' in json_ref:
        return Dimension( 
            System( UID( json_ref['system']['uid'] ) ),
            to_dim_tuple( json_ref['system']['dimensions'] ),
            to_prefix_tuple( json_ref['system']['prefix'] )
        )
        
    else:
        return None 
        
# ---------------------------------------------------------------------------
class Reference(object):

    """
    A Reference encapsulates access to an M-layer entry about a
    measurement unit or other type of reference.  

    """

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
        return "{}".format(
            self._json_entry['locale']['default']['symbol'] 
        )
        
    @property
    def dimension(self):
        try:
            return self._dimension
        except AttributeError:
            dim = entry_to_dimension(self._json_entry)
            if dim is None:
                raise RuntimeError("no unit system for {!r}".format(
                        UID( json_ref["uid"] )
                    )
                )
            else:
                self._dimension = dim
                
            return self._dimension
                            
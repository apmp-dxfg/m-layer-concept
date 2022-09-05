# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
from ast import literal_eval 

from m_layer.uid import UID

# ---------------------------------------------------------------------------
class Register(object):
    
    """
    
    """
    
    def __init__(self,context):
        self._context = context 
        self._objects = {}
        
    def __getitem__(self,uid):
        return self._objects[ uid ]
        
    def get(self,uid,default=None):
        """
        """
        # # `uid` may be a list from json
        # return self._objects.get( tuple(uid), default ) 
        return self._objects.get( uid, default )
        
    def set(self,entry):
        """
        """
        # Convert the string representation of a JSON sequence to tuple
        if isinstance( entry['uid'],str ):
            # Is this still needed?
            assert False
            uid = tuple( literal_eval(entry['uid']) )
        else:
            # Encapsulate the JSON uid
            uid = UID( entry['uid'] )
        
        if uid in self._objects:
            raise RuntimeError(
                "existing register entry: {}".format(uid)
            )
        else:
            self._objects[uid] = entry 
                          
                
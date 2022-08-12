# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

import json
from ast import literal_eval 

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
        # `uid` may be a list from json
        return self._objects.get( tuple(uid), default ) 
        
    def set(self,entry):
        """
        """
        # Convert string of sequence from json to tuple
        if isinstance(entry['uid'],str):
            # literal_eval will safely handle Python types
            uid = tuple( literal_eval(entry['uid']) )
        else:
            uid = tuple( entry['uid'] )
        
        if uid in self._objects:
            raise RuntimeError(
                "existing register entry: {}".format(uid)
            )
        else:
            self._objects[uid] = entry 
                          
                
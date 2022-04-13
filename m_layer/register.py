# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

import json

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
        
    # There is a difference between minting a new reference and reading a record.
    # The context will mint new reference objects, here we just register them
    def set(self,entry):
        """
        """
        # Convert string of sequence from json to tuple
        if isinstance(entry['uid'],str):
            uid = tuple( eval(entry['uid']) )
        else:
            uid = tuple( entry['uid'] )
        
        if uid in self._objects:
            raise RuntimeError(
                "existing register entry: {}".format(uid)
            )
        else:
            self._objects[uid] = entry 
                          
    # def dumps_entry(self,uid): 
         # """
         # """
         # return json.dumps( self._objects[uid] )
     
    # def dumps(self,choice=None):
        # """
        # """
        # if choice is None:
            # choice = self._objects.keys()
            
        # return json.dumps( [ 
            # self.dumps_entry(uid) for uid in choice
        # ] )
                
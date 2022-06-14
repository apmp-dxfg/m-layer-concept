# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
"""
Declared conversions must be enabled for each aspect.
This register holds a sequence of M-layer scales for each aspect. 
"""
from m_layer.register import Register

# ---------------------------------------------------------------------------
class ScalesForAspectRegister(Register):
    """
    """
    
    def __init__(self,context):
        super().__init__(context) 
        
    def set(self,entry):
        uid = tuple( entry['aspect'] )
        
        if uid in self._objects:
            raise RuntimeError(
                "existing register entry: {}".format(uid)
            )
        else:
            self._objects[uid] = [
                tuple( json_id ) 
                    for json_id in entry['scales']
            ]
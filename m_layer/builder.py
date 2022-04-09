# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The `Builder` takes JSON object definitions that are complete except for 
# a UUID. It expects each JSON object to have an element in the form
#   "uid" : "(name,None)", where 'None' occupies the place for a UUID. 
# A UUID will be generated to replace 'None' and the JSON record may 
# be exported to a file or as a string. 
#
# This Builder scaffolding could be used to check JSON objects.
#
import json 
import uuid 

# ---------------------------------------------------------------------------
class Builder(object):
    
    """
    """
    
    def __init__(self):
        self._entities = {}

    def new_uid(self,name):
        """
        Return a tuple `(name, uuid)` where the `uuid` element is a 
        random UUID in the form of a 128-bit integer.
        
        """
        return (name,uuid.uuid4().int)
        
    def _load_entity(self,entity):
        # Convert string of sequence from json to tuple
        if isinstance(entity['uid'],str):
            name = eval(entity['uid'])[0]
        else:
            name = entity['uid'][0]

        uid = self.new_uid(name)
        entity['uid'] = uid 

        if entity['uid'] in self._entities:
            raise RuntimeError(
               "uid is already used: {}".format(self._entities[uid])
            )
        else:
            self._entities[uid] = entity 
        
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
        with open(file_path,'r') as fp:
            data = json.load(fp,**kwargs)        
        self._loader(data)

    def dumps(self,**kwargs):
        return json.dumps( 
            list( self._entities.values() ),
            **kwargs
        )

    def dump(self,file_path,**kwargs):
        return json.dump( 
            list( self._entities.values() ), 
            file_path, 
            **kwargs 
        )

# ===========================================================================
if __name__ == '__main__':
    
    json_data = """[
    {
        "__type__": "Reference",
        "uid": [
            "imp-pound",
            188151331508313165897603768130808181784
        ],
        "locale": {
            "default": {
                "name": "pound",
                "symbol": "lb"
            }
        },
        "metadata": {
            "url": "https://en.wikipedia.org/wiki/Pound_(mass)"
        }
    }
]"""

    build = Builder()
    build.loads(json_data)
    # with open('scales.json','w') as fp:
    print( build.dumps() ) 
        
        


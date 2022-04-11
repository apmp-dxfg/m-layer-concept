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

# ---------------------------------------------------------------------------
def create():
    """
    Helper for creating JSON entries.
    
    """
    record = ''
    
    prompt = "Type: "
    data = input(prompt).strip()
    line = '"__type__": "{}",'.format(data)
    # print(line)
    record += line
    
    prompt = "uid (n)? "
    data = input(prompt).strip()
    if len(data):
        line = '"uid": [ "{}", {} ],'.format( data,uuid.uuid4().int )
        # print(line)
        record += line
        
    prompt = "locale required (n)? "
    if input(prompt).strip().upper() == 'Y':
        line = '"locale":{'
        while True:
            prompt = "locale name, or return: "
            lname = input(prompt).strip()
            if len(lname):
                line += '"{}": {{'.format(lname)
                while True:
                    prompt = 'key, or return: '
                    key = input(prompt).strip()
                    if not len(key):
                        if line[-1] == ',': 
                            line = line[:-1] + '},'
                        break
                    prompt = 'value: '
                    value = input(prompt).strip()
                    line += '"{}":"{}",'.format(key,value)
            else:
                if line[-1] == ',': 
                    line = line[:-1] + '},'
                break                    
        # print(line)
        record += line
    
    line = ''
    while True:
        prompt = "JSON object name (n)? "
        xname = input(prompt).strip()
        if not len(xname):
            break            
                
        line += '"{}":{{'.format(xname)
        while True:
            prompt = "item name or return: "
            xkey = input(prompt).strip()
            if not len(xkey):
                if line[-1] == ',': 
                    line = line[:-1] + '},'
                if line[-1] == '{': 
                    line += '},'
                break                    
            prompt = "item value: "
            xvalue = input(prompt).strip()
            line += '"{}":"{}",'.format(xkey,xvalue)
                    
    # Done
    if line[-1] == ',': line = line[:-1]
    # print(line)
    record += line
    
    try:
        j = json.loads('[{{ {} }}]'.format(record) )
       
    except json.decoder.JSONDecodeError as e:
        print("JSON error:")
        print(e)
        print(record)
    else:
        print()
        print( json.dumps(j,indent=4) )

        
def UUID():
    print(uuid.uuid4().int) 
    
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

    # build = Builder()
    # build.loads(json_data)
    # # with open('scales.json','w') as fp:
    # print( build.dumps() ) 
    
    # create()
    UUID()
        


"""
The ``new_uuid`` module is a command line script that generates 
a new UUID in the command prompt. 

Usage:

.. code:: text

    C:\m_layer>python new_uuid.py
    87456781262672120497206789902336639091
    
"""
import uuid 

if __name__ == '__main__':

    print(uuid.uuid4().int) 
    


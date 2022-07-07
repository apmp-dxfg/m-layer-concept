.. _src_json:

=============================
M-layer JSON register entries
=============================
For the purposes of this proof of concept project, the M-layer registry 
of scales, aspects, conversions, etc., is implemented in JSON.


.. contents::
   :local:

Registry database in JSON files
===============================

The is a directory called ``json`` under ``m_layer`` in the Python distribution
with the following substructure::

    json/
        |
        +---> aspects/
        |
        +---> conversion_casting/
        |
        +---> references/
        |
        +---> scales/
        |
        +---> scales_for_aspects/

All JSON files (with file extension '.json') in these 
directories are automatically read when the m_layer 
module is imported. The file contents is parsed for entries to the M-layer central register.

Files contain a single JSON array (starting and ending with ``[`` and ``]``),
which may contain any number of JSON objects (starting and ending with ``{`` and ``}``)
that define register entries.


Aspect entries
--------------
An example of an aspect entry is shown below. The following named elements are used by the M-layer currently:

    - ``__entry__``: the type of entry (used during parsing)
    - ``uid``:  the M-layer unique identifier for the aspect
    - ``locale``: an object containing information used to render the aspect 

.. code:: json 

    {
        "__entry__": "Aspect",
        "uid": [
            "ml-reflectance",
            77619173328682587252206794509402414758
        ],
        "locale": {
            "default": {
                "name": "reflectance",
                "symbol": "R"
            }
        }
    }        

Scale entries 
-------------
An example of a scale entry is shown below. The JSON object has the following named elements:

    - ``__entry__``: the type of entry (used during parsing)
    - ``uid``:  the M-layer unique identifier for the scale
    - ``reference``: the M-layer unique identifier for the reference associated with the scale 
    - ``scale_type``: the name of the type of scale
    
.. code:: json 

    {
        "__entry__": "Scale",
        "uid": [
            "ml-reflectance-ratio",
            231644681522224058023728516454961855496
        ],
        "reference": [
            "si-one",
            86027072402622903744975433595176472531
        ],
        "scale_type": "ratio"
    }

Reference entries 
-----------------
An example of a reference entry is shown below. The following named elements are used by the M-layer currently:

    - ``__entry__``: the type of entry (used during parsing)
    - ``uid``:  the M-layer unique identifier for the reference
    - ``locale``: an object containing information used to render the aspect 
        
.. code:: json 

    {
        "__entry__": "Reference",
        "uid": [
            "si-one",
            86027072402622903744975433595176472531
        ],
        "locale": {
            "default": {
                "name": "one",
                "symbol": ""
            }
        }
    }
    
Conversion entries
------------------
An example of a conversion entry is shown below. The following named elements are used by the M-layer currently:

    - ``__entry__``: the type of entry (used during parsing)
    - ``src``:  the unique identifier for the initial (source) scale
    - ``dst``: the unique identifier for the final (destination) scale 
    - ``factors``: an array expressions that will evaluate to numerical conversion function coefficients (the number and nature of these factors depends on the scale type) 
        
.. code:: json 

    {
        "__entry__": "Conversion",
        "src": [
            "ml-si-kilogram-ratio",
            12782167041499057092439851237297548539
        ],
        "dst":[
            "ml-imp-pound-ratio", 
            188380796861507506602975683857494523991
        ],
        "factors": [ "2.2046" ]
    }
    
Aspect-specific conversion entries
----------------------------------

An example of an aspect-specific conversion entry is shown below. The following named elements are used by the M-layer currently:

    - ``__entry__``: the type of entry (used during parsing) 
    - ``aspect``: the unique identifier for the aspect
    - ``src``:  the unique identifier for the initial (source) scale
    - ``dst``: the unique identifier for the final (destination) scale 
    - ``factors``: an array expressions that will evaluate to numerical conversion function coefficients (the number and nature of these factors depends on the scale type) 
        
.. code:: json 

    {
        "__entry__": "ScalesForAspect",
        "aspect" : [
            "ml-photon-energy",
            291306321925738991196807372973812640971
        ],
        "src": [
            "ml-si-terahertz-ratio",
            271382954339420591832277422907953823861
        ],
        "dst":[
            "ml-si-per-centimetre-ratio",
            333995508470114516586033303775415043902
        ],
        "factors": [ "si.tera/si.c*si.centi" ]
    }
    
Casting entries
---------------
An example of a casting entry is shown below. The following named elements are used by the M-layer currently:

    - ``__entry__``: the type of entry (used during parsing)
    - ``src``:  dentifiers for the initial (source) scale and aspect
    - ``dst``: identifiers for the final (destination) scale and aspect
    - ``function``: a string that will be evaluated to define a Python casting function
    - ``factors``: an object that will be evaluated to define a Python dictionary in which casting function parameters are defined 
        
.. code:: json 

   {
        "__entry__": "Cast",
        "src": [
            [
                "ml-electronvolt-ratio",
                121864523473489992307630707008460819401
            ],
                        [
                "ml-photon-energy",
                291306321925738991196807372973812640971
            ]
        ],
        "dst":[
            [
                "ml-si-nanometre-ratio",
                257091757625055920788370123828667027186
            ],
                        [
                "ml-photon-energy",
                291306321925738991196807372973812640971
            ]
        ],
        "function" : "lambda x: c/x",
        "parameters" : { "c" : "si.h*si.c/si.e/si.nano" }
    }
    
Python module of defined constants
----------------------------------
The functions and coefficients used to convert and cast data are created from strings stored in the JSON entries. 
The built-in Python function :func:`eval` is used to convert these strings to Python objects.

The following file is imported during this evaluation process to provide numeric constants.

.. literalinclude:: ../m_layer/si_constants.py
    :language: py


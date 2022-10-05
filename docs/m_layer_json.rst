.. _src_json:

=========================
M-layer-concept JSON data
=========================

.. contents::
   :local:

Registry file structure
=======================

The ``m-layer-concept`` registry is implemented in JSON files.

There is a root directory named ``json``, under ``m_layer`` in the Python distribution.
This ``json`` directory has subdirectories that contain the JSON files (with file extension '.json').
The structure is as follows::

    json/
        |
        +---> aspects/
        |
        +---> casting/
        |
        +---> conversion/
        |
        +---> references/
        |
        +---> scales/
        |
        +---> scales_for/
        |
        +---> systems/
    
General comments about JSON data 
================================
Each file contains a single JSON array (starting and ending with ``[`` and ``]``),
which contains a sequence of M-layer JSON objects (starting and ending with ``{`` and ``}``),
each defining a register entry. 

The objects for M-layer entities begin with the name ``__entry__``, which identifies the type (aspect, reference, scale, etc.)

All entities that could be rendered include the name ``locale``, which holds information about display options. This feature has not been developed beyond simple default behaviour yet.

If the type of entity has a unique identifier, that element is named ``uid`` in the JSON object. 

.. note::

    The M-layer will use persistent globally unique identifiers for elements, but the details are not determined yet. This concept project adopts an *ad hoc* arrangement (see `M-layer-concept identifier names`_ below).


M-layer-concept identifier names
-------------------------------- 

The *ad hoc* structure adopted for unique identifiers uses two components in a JSON array: a name (string) and a UUID (integer). 
The names help people navigate entries, although the UUID already provides uniqueness. 

The combination of the name and UUID is considered to be the unique identifier. Two identifiers are considered equal when *both* the name and UUID match.

A naming convention has been followed:

    * **aspect**: the name is prefixed with ``ml`` followed by an arbitrary descriptor (e.g., ``ml_length``).

    * **system**: the name is prefixed with initials associated with the system's name and ends with the suffix '_system', e.g., ``si_system``.

    * **reference**: the name is prefixed with initials that identify a system or (broadly) a family of units. This is followed by a descriptor. When the reference is a single unit, the unit name is used, but for compound unit names the descriptor adopts a short form based on unit symbols. Hence, for example, ``si_kilogram`` and ``si_m.s-1``.

    * **scale**: the name is prefixed with ``ml`` followed by a string associated with the reference and ends with a suffix for the scale type. Hence, for example, ``ml_si_kg.m2.s-3.A-1_ratio`` and ``ml_si_volt_ratio`` (note, alternative strings may related to a single reference, as in this example).

JSON objects shown below provide naming examples.
       
        
Aspect
======
Aspects have a unique identifier, but do not refer to other M-layer entities.  

.. code:: json 

    {
        "__entry__": "Aspect",
        "uid": [
            "ml_reflectance",
            77619173328682587252206794509402414758
        ],
        "locale": {
            "default": {
                "name": "reflectance",
                "symbol": "R"
            }
        }
    }        
    
Reference 
=========
References have a unique identifier. 

If the reference is a unit belonging to a system of units then 
additional information is entered under the name ``system``. 

The 'system' object holds an M-layer identifier for the system, 
the dimensions of the reference in the system, and the numerical
prefix of the unit (expressed in rational form, as a numerator and denominator strings)
with respect to the corresponding coherent system unit.
        
.. code:: json 

    {
        "__entry__": "Reference",
        "uid": [
            "si_m.s-1",
            209336055680499528994573882116031757760
        ],
        "locale": {
            "default": {
                "name": "metre per second",
                "symbol": "m.s-1"
            }
        },
        "system": {
            "uid": [
                "si_system",
                88156805987886421108624908988601219537
            ],
            "dimensions": "[0, 1, -1, 0, 0, 0, 0]",
            "prefix": [
                "1",
                "1"
            ]
        }
    }
    
System 
======
A system has a unique identifier and an array of identifiers for the system base units (references). 
The order of elements in this array is important. 
It matches the order of exponents in the ``system.dimensions`` array in a JSON Reference.

.. code:: json 

    {
        "__entry__": "UnitSystem",
        "uid": [
            "si_system",
            88156805987886421108624908988601219537
        ],
        "name": "SI",
        "basis": [
            [
                "si_kilogram",
                188151331508313165897603768130808181784
            ],
            [
                "si_metre",
                61268972265076316018593147152102406832
            ],
            [
                "si_second",
                110730041758233939215703442037761569190
            ],
            [
                "si_ampere",
                264081801568151063132838497538090031099
            ],
            [
                "si_kelvin",
                25703533220788919988679332108037098600
            ],
            [
                "si_mole",
                96713855510406467826626480289106173630
            ],
            [
                "si_candela",
                107700549721211215242458620140782394628
            ]
        ]
    }
    
Scale 
=====
A scale combines a reference with 'scale type' ('ratio', 'interval', etc.). A scale has a unique identifier and referes to the identifier of an M-layer reference. 

A scale may include the name ``systematic`` when the scale's name is composed of products of powers of base-unit symbols (the base units of a unit system). 
    
.. code:: json 

    {
        "__entry__": "Scale",
        "uid": [
            "ml_si_kg.m2.s-2.A-1_ratio",
            123074114253301537873407416011262630402
        ],
        "reference": [
            "si_weber",
            3389824025561912595583897462196041346
        ],
        "scale_type": "ratio",
        "systematic": 1
    }


    
Conversion
==========
Conversion is a mathematical operation related to a pair of M-layer scales.

A JSON conversion entry holds a definition of the mathematical operation required to transform data from one scale to the other. 
The M-layer distinguishes between conversions that are aspect-independent and conversions restricted to specific aspects.

Aspect-specific conversion
--------------------------

An aspect-specific conversion is identified by the combination of: an aspect, the initial (source) scale and the final (destination) scale.

The conversion function is specified in text, as are the parameters needed (see :ref:`ml_math-label` for details). In this example, the transformation is a simple identity mapping.
        
.. code:: json 

    {
        "__entry__": "ScalesForAspect",
        "aspect": [
            "ml_frequency",
            153247472008167864427404739264717558529
        ],
        "src": [
            "ml_si_s-1_ratio",
            323506565708733284157918472061580302494
        ],
        "dst": [
            "ml_si_hertz_ratio",
            307647520921278207356294979342476646905
        ],
        "function": "lambda x: x",
        "parameters": {}
    }
  
Aspect-independent conversion
-----------------------------
  
An aspect-independent conversion is identified by the M-layer identifiers for the initial (source) scale and the final (destination) scale. 

In this example, the transformation is the conversion function :math:`y = x + 273.15`, where :math:`x` is data on the Celsius scale and :math:`y` is the data converted to kelvin.
        
.. code:: json 

    {
        "__entry__": "Conversion",
        "src": [
            "ml_si_celsius_interval",
            245795086332095731716589481707012001072
        ],
        "dst": [
            "ml_si_kelvin_ratio",
            302952256288207449238881076502466548054
        ],
        "function": "lambda x: x + b",
        "parameters": {
            "a": "1",
            "b": "+273.15"
        }
    }
    

    
Casting
=======
An M-layer cast is an operation to transform data from one scale-aspect pair to another. 

A cast is identified by the initial (source) scale-aspect pair and the final (destination) scale-aspect pair.
 
In the following example, the casting operation transforms data in inverse seconds with aspect undefined to data expressed in hertz (aspect is frequency). 
The numerical part of this operation is trivial, but the change of aspect must be directly specified, because data in inverse seconds could also be associated with activity (with SI unit becquerel). 
        
.. code:: json 

    {
        "__entry__": "Cast",
        "src": [
            [
                "ml_si_s-1_ratio",
                323506565708733284157918472061580302494
            ],
            [
                "ml_no_aspect",
                295504637700214937127120941173285352815
            ]
        ],
        "dst": [
            [
                "ml_si_hertz_ratio",
                307647520921278207356294979342476646905
            ],
            [
                "ml_frequency",
                153247472008167864427404739264717558529
            ]
        ],
        "function": "lambda x: x",
        "parameters": {}
    }
    

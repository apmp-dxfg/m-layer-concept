.. _src_json:

=========================
M-layer-concept JSON data
=========================

.. contents::
   :local:

Registry file structure
=======================

The ``m-layer-concept`` registry is implemented in JSON files.

There is a root directory ``json``, under the directory ``m_layer`` in the Python distribution.
The ``json`` directory contains subdirectories where the JSON files (with file extension '.json') are stored.
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
Each file contains one JSON array (starting and ending with ``[`` and ``]``),
containing any number of M-layer JSON objects (starting and ending with ``{`` and ``}``),
each defining a register entry. 

The JSON objects for M-layer entities begin with the name ``__entry__``, which identifies the type (aspect, reference, scale, etc.)

All entities that could be rendered include the name ``locale``, which holds information about display options. This feature has not been developed beyond default behaviour yet.

Entities that have a unique identifier name that element ``uid`` in the JSON object. 

.. note::

    Although the M-layer will use persistent globally unique identifiers for elements, such as aspects and scales, the details are not determined yet. This project adopts an *ad hoc* arrangement (see `M-layer-concept unique identifiers`_ below).


M-layer-concept unique identifiers
---------------------------------- 

Unique identifiers have two components in a JSON array: a name (string) and a UUID (integer). 
Although the UUID provides a unique identifier of register entries, the names help people navigate entries.

Two identifiers are considered equal when *both* the name and UUID match.

The naming convention is as follows.

    * For an **aspect**, the name begins with ``ml_`` followed by an arbitrary descriptor (``ml_[aspect_name]``).

    * For a unit **system**, the name begins with initials associated with the system and ends with '_system', e.g., ``si_system``.

    * For a **reference**, the name begins with initials that identify (broadly) the system or family of units. This is followed by a descriptor. When the reference is a compound unit, the descriptor takes on a short form but when there is a single unit name the long form is used. Hence, ``si_kilogram`` and ``si_m.s-1``, for example.

    * For a **scale**, the name begins with ``ml`` followed by a string associated reference and ending in the name of the scale type. Hence, ``ml_si_kg.m2.s-3.A-1_ratio`` and ``ml_si_volt_ratio``, for example (note, there may be alternative strings associated with a single reference).

The examples of JSON objects in the following sections provide many examples of the unique identifier format.
       
        
Aspect
======
Aspects require a unique identifier, but do not refer to other M-layer entities. An example follows. 

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
References require a unique identifier. 

If the reference is a unit belonging to a system of units then 
additional information is entered against the name ``system``. 
This 'system' object holds an M-layer identifier of the system, 
the dimensions of the unit in the system, and the numerical
prefix of the unit (expressed in rational form as a numerator and denominator)
with respect to the corresponding coherent unit.
        
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
A system requires a unique identifier and contains references to the references that form the system basis. An example follows. 

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
A scale requires a unique identifier and identifies a reference in the M-layer. 

The type of scale is identified ('ratio', 'interval', etc.).

The name ``systematic`` is included when a scale is associated with a reference belonging to a unit system and the scale name is composed of products of powers of base-unit names.
    
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
A conversion entry holds an operation to transform data from one scale to another. We distinguish between conversions that are restricted to specific aspects and conversions that are aspect-independent.

Aspect-specific conversion
--------------------------

An example of an aspect-specific conversion entry is shown below. The conversion is identified by the combination of three M-layer identifiers: the aspect, the initial (source) scale and the final (destination) scale.

The transformation function is specified in text as are the parameters needed (see ??? for details). In this example, the transformation is a trivial mapping.
        
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
  
The aspect-independent conversion data has the same form, except there is no ``aspect`` name. The conversion is identified by the combination of two M-layer identifiers: the initial (source) scale and the final (destination) scale.
        
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

A cast entry holds an operation to transform data from one scale-aspect pair to another. The cast is identified by the combination of identifiers for the initial (source) scale-aspect pair and the final (destination) scale-aspect pair.
 
In the following example, the cast transforms data expressed in inverse seconds to data expressed in hertz.
        
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
    

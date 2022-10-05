.. _src_docs:

===========================
M-layer-concept Python code
===========================

.. contents::
   :local:

The Python code has two main roles: 

    i) to refer to the M-layer registry (the JSON files), and 
    ii) to support client-side code that will uses the M-layer representation. 
    
(There are also some Python modules that can assist when extending the M-layer JSON entries.)

M-layer-register API
====================
The first role is handled by the :class:`~context.Context` class, which provides access to conversion and casting tables in the registry. Client-side software does not see the context. 

A default context is created when the Python package is imported. This object reads and internally organises all the JSON data.

.. _ml_math-label:

Support for scale transformation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As part of the initialisation process, mathematical transformation functions are instantiated from string descriptors for the functions and parameters stored in the registry.  

The built-in Python function :func:`eval` is used to convert parameter strings and functions into Python objects. During evaluation, some numerical constants defined in the SI and mathematical constants are available. There is also a small number of scale transformation functions.
  

Defined SI constants
^^^^^^^^^^^^^^^^^^^^

The following definitions of numeric values are available in the namespace ``si``  during evaluation. 

.. literalinclude:: ../m_layer/si_constants.py
    :language: py
   
Mathematical constants
^^^^^^^^^^^^^^^^^^^^^^

The following definitions provide numeric constants in the namespace ``number``  during evaluation.

.. literalinclude:: ../m_layer/math_constants.py
    :language: py

Defined transformations
^^^^^^^^^^^^^^^^^^^^^^^

The following conversion functions for scales are defined in the ``ml_math`` namespace during evaluation.

.. automodule:: ml_math
    :members: bounded_convert, interval_convert, ratio_convert

The Context
~~~~~~~~~~~

The :class:`~context.Context` methods used to access registry entries are shown here.

.. autoclass:: context.Context
    :members: conversion_from_scale_aspect, cast_from_scale_aspect

Modules that support the context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A number of other modules support :class:`~context.Context`
        
.. automodule:: register
    :members:

.. automodule:: conversion_register
    :members:

.. automodule:: casting_register
    :members:
   
.. automodule:: scales_for_aspect_register
    :members:
  
Client-side API
===============

The :class:`~lib.Aspect` and :class:`~lib.Scale` classes encapsulate unique identifiers.

.. autoclass:: lib.Aspect
    :members: 
    :special-members: __eq__
  
.. autoclass:: lib.Scale
    :members: 
    :special-members: __eq__

There is also :class:`~lib.ScaleAspect`, in which a scale-aspect pair are encapsulated.

.. autoclass:: lib.ScaleAspect
    :members: 
    :special-members: __eq__
  
Supporting classes for compound expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aspects, Scales or ScaleAspects can be multiplied, divided and exponentiated, which will generate corresponding compound objects. 

.. autoclass:: lib.CompoundAspect
    :members: 
    :special-members: __eq__
  
.. autoclass:: lib.CompoundScale
    :members: 
    :special-members: __eq__

.. autoclass:: lib.CompoundScaleAspect
    :members: 
    :special-members: __eq__
   
Systematic and CompoundSystematic 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When the expression encapsulated in a :class:`~lib.CompoundScale` or :class:`~lib.CompoundScaleAspect` consists of scales associated with a unit system, a :class:`systematic.Systematic` can express the dimensional exponents in that system's dimensions. 
  
.. autoclass:: systematic.Systematic
    :members: 
    :special-members: __eq__
 
Dimensions can be multiplied, divided and exponentiated, which generates a corresponding compound class. 

.. autoclass:: systematic.CompoundSystematic
    :members: 
    :special-members: __eq__

UID and CompoundUID 
^^^^^^^^^^^^^^^^^^^
The :class:`~uid.UID` class encapsulates M-layer unique identifiers 

.. autoclass:: uid.UID
    :members: 
    :special-members: __eq__

A :class:`~uid.CompoundUID` encapsulates the individual uids of the scales, or scale-aspects, in a compound unit expression. 

.. autoclass:: uid.CompoundUID
    :members: 
    :special-members: __eq__
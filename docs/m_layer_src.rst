.. _src_docs:

===========================
M-layer-concept Python code
===========================

.. contents::
   :local:

The Python code has two main roles: i) to connect to the M-layer registry (the JSON files), and ii) to support client-side Python code that will make use of the M-layer representation system. There is also some Python code that can assist when extending the M-layer JSON entries. 

M-layer-register API
====================
The first role is handled by the :class:`~context.Context` class, which provides access to conversion and casting tables in the registry. Client-side software does not see the context. 

A default context is created when the Python package is imported. This object reads and internally organises all the JSON data.

Support for scale transformation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As part of the initialisation process, transformation functions are instantiated from the string descriptors stored in the registry. The parameters to these functions are also stored in string format. 

The built-in Python function :func:`eval` is used to convert parameter strings and functions into Python objects.
  

Defined SI constants
^^^^^^^^^^^^^^^^^^^^

The following definitions of numeric values are available in the namespace ``si``  during evaluation of JSON strings. 

.. literalinclude:: ../m_layer/si_constants.py
    :language: py
   
Mathematical constants
^^^^^^^^^^^^^^^^^^^^^^

The following definitions provide numeric constants in the namespace ``number``  during evaluation of JSON strings.

.. literalinclude:: ../m_layer/math_constants.py
    :language: py

Defined transformations
^^^^^^^^^^^^^^^^^^^^^^^

The following conversion functions for scales are defined in the ``ml_math`` namespace during evaluation of JSON strings.

.. automodule:: ml_math
    :members: bounded_convert, interval_convert, ratio_convert

The Context
^^^^^^^^^^^
The :class:`~context.Context` methods that are used to access the registry are documented here.

.. autoclass:: context.Context
    :members: conversion_from_scale_aspect, casting_from_scale_aspect, casting_from_compound_scale_dim, conversion_from_compound_scale_dim

Supporting modules
^^^^^^^^^^^^^^^^^^

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

The user API is supported by the :class:`~lib.Aspect` and :class:`~lib.Scale` classes, which encapsulate unique identifiers.

.. autoclass:: lib.Aspect
    :members: 
    :special-members: __eq__
  
.. autoclass:: lib.Scale
    :members: 
    :special-members: __eq__

There is also a class in which a scale and an aspect are encapsulated,  :class:`~lib.ScaleAspect`.

.. autoclass:: lib.ScaleAspect
    :members: 
    :special-members: __eq__
   
These objects can be multiplied, divided and exponentiated, which generates corresponding compound classes.

.. autoclass:: lib.CompoundAspect
    :members: 
    :special-members: __eq__
  
.. autoclass:: lib.CompoundScale
    :members: 
    :special-members: __eq__

.. autoclass:: lib.CompoundScaleAspect
    :members: 
    :special-members: __eq__
   
The :class:`dimension.Dimension` class encapsulates the dimensional signature of a scale in terms
of the corresponding system dimensions. The object also holds a 
  
.. autoclass:: dimension.Dimension
    :members: 
    :special-members: __eq__
 
Dimension objects can be multiplied, divided and exponentiated, which generates the corresponding compound class. 

.. autoclass:: dimension.CompoundDimension
    :members: 
    :special-members: __eq__

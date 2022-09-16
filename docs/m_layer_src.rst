.. _src_docs:

===========================
M-layer-concept Python code
===========================

.. contents::
   :local:

Package overview
================ 

The Python code has two main roles: i) to connect to the M-layer registry (the JSON files), and ii) to support client-side Python code that will make use of the M-layer representation system. There is also some Python code that can assist when extending the M-layer JSON entries. 

M-layer-register API
--------------------
The first role is handled by the :class:`~context.Context` class, which provides access to conversion and casting tables in the registry. Client-side software does not see the context. 

A default context is created when the Python package is imported. This object reads and internally organises all the JSON data.

.. autoclass:: context.Context
    :noindex:
    :members: conversion_from_scale_aspect, casting_from_scale_aspect, casting_from_compound_scale_dim, conversion_from_compound_scale_dim


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

    

        
Register
--------

.. automodule:: register
    :members:
    
Conversion register
-------------------

.. automodule:: conversion_register
    :members:

Casting register
----------------

.. automodule:: casting_register
    :members:
   
Scales for Aspect register
--------------------------

.. automodule:: scales_for_aspect_register
    :members:
    
Lib
---

.. automodule:: lib
    :members:
    :special-members: __eq__
   
Dimension
---------
.. automodule:: dimension
    :members: 
    :special-members: __eq__
    

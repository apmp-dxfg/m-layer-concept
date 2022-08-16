.. _api:

===========
M-layer API
===========

.. contents::
   :local:
  
Functions
---------  
.. autofunction:: expression.expr

.. autofunction:: expression.convert
.. autofunction:: expression.cast
.. autofunction:: expression.token

.. py:function:: value(xp) 

    An alias for :func:`~expression.token` that returns the value of an expression
    
.. autofunction:: expression.scale
.. autofunction:: expression.aspect

.. py:function:: kind_of_quantity(xp) 

    An alias for :func:`~expression.aspect` that returns the kind of quantity of an expression
 
Classes
-------
 
.. autoclass:: expression.Expression
    :members: token, value, scale, aspect, scale_aspect, convert, cast 

.. autoclass:: aspect.Aspect
    :members: uid
    :special-members: __eq__
    
.. autoclass:: scale.Scale
    :members: uid
    :special-members: __eq__
    
.. autoclass:: scale.ScaleAspect
    :members: uid, scale, aspect
    :special-members: __eq__
   
  
Utility functions
-----------------
   
.. automodule:: ml_to_py_key


   

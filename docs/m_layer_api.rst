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
     
Classes
-------
 
.. autoclass:: expression.Expression
    :members: token, value, scale_aspect, convert, cast 

.. autoclass:: lib.Aspect
    :noindex:
    :members:
    :special-members: __eq__
  
.. autoclass:: lib.Scale
    :noindex:
    :members: 
    :special-members: __eq__
    
.. autoclass:: lib.ScaleAspect
    :noindex:
    :members: uid, scale, aspect
    :special-members: __eq__
      
      

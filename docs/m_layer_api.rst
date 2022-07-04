.. _api:

===========
M-layer API
===========

.. contents::
   :local:

.. _api_module:

.. automodule:: api
	:members: 
	:inherited-members:
    
.. autoclass:: aspect.Aspect
    :members: uid
    :special-members: __eq__
    
.. autoclass:: scale.Scale
    :members: uid, to_scale_aspect
    :special-members: __eq__
    
.. autoclass:: scale_aspect.ScaleAspect
    :members: uid, to_scale_aspect, scale, aspect
    :special-members: __eq__
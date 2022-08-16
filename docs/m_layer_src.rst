.. _src_docs:

=================================
M-layer source code documentation
=================================

.. contents::
   :local:

Context
-------

.. automodule:: context
    :members:
    :special-members: __init__
    
.. autodata:: context.default_context
    :annotation: = the Context object used during a Python session
    
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
    
Scale
-----

.. automodule:: scale
    :noindex:
    :members:
    :special-members: __eq__

Aspect
------
.. automodule:: aspect
    :noindex:
    :members:
    :special-members: __eq__
        
Composition
-----------
.. automodule:: composition
    :members: 
    :special-members: __eq__
    
Dimension
---------
.. automodule:: dimension
    :members: 
    :special-members: __eq__
    
JSON register entries
---------------------
.. toctree::
   :maxdepth: 0

   JSON register <m_layer_json>

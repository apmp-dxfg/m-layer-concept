.. _concept_m_register: 

The M-layer register of scales and aspects
==========================================

.. contents::
   :local:

M-layer expressions of data use compact digital objects to identify scales and aspects.
Each aspect, scale, and reference has a unique digital identifier, which is used to access more detailed information in a central register. 

The register holds records of aspects, scales, and references (units and other types of reference),
that provide support for scale conversions and casting expressions to different scales and aspects.
 
.. figure:: pictures/MlayerRegisterClass.png
   :figwidth: 100%
   :align: center
   :alt: Class diagram for the M-layer central register
   
   A UML class diagram showing the central register and its associations. The register supports 
   scale conversion and casting from one expression to another. It does this by
   maintaining registers of legitimate conversions and casts, which are indexed by scale and aspect
   identifiers.   

Relationship between scales and references
------------------------------------------
In the M-layer, a 'reference' is a digital record corresponding to a unit of measure, or other 
measurement reference (e.g., a certified reference material). It holds information about the unit,
like formats for rendering, as well as related external links. 

An M-layer 'scale' is an association between a reference and a particular scale type (see :ref:`concept_m_expressions_scales`).

Expression conversion
---------------------
An expression can be converted from one scale to another if the operation to do so has been registered.

Scale conversion in the M-layer is similar to conversion in traditional unit systems.
However, the M-layer distinguishes between two classes of conversion: 

    1) those that are legitimate for any aspect; and 
    2) those that are legitimate for a particular aspect. 
    
An example of the first is conversion from metres to millimetres.
An example of the second is the conversion of an expression of photon energy in electronvolts to an expression in terahertz. 

Aspect-independent conversions are only permitted between scales of the same type, but
aspect-specific conversions may change the scale type (between ratio and interval scales); 
conversion *never* changes the aspect. 

A legitimate conversion can be queried by providing the unique identifiers for the source and destination (initial and final) 
scales, with a unique identifier for aspect as an optional argument.


Expression casting 
------------------

Expression casting is used to change the aspect of an expression or when the casting operation is not an invariance transformation for the scale type. Such operations might be termed a 'change of variables'. For instance, a cast is required to change an expression of photon energy from terahertz to nanometres (i.e., the change of variable is from frequency to wavelength). 

 
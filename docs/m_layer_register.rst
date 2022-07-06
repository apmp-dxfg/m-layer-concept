.. _concept_m_register: 

The M-layer register of scales and aspects
==========================================

.. contents::
   :local:

M-layer expressions of measurement data use compact digital objects to identify scales and aspects.
Each aspect, scale, and reference has a unique digital identifier, which is encapsulated 
in these digital objects and can be used to access more detailed information in a central authoritative register. 

The register holds records of aspects, scales, and references (units and other types of reference),
and provides support for scale conversions and casting expressions to different scales and aspects.
 
.. figure:: pictures/MlayerRegisterClass.png
   :figwidth: 100%
   :align: center
   :alt: Class diagram for the M-layer central register
   
   A UML class diagram showing the central register and its associations. The register provides 
   scale conversion functions and functions to cast from one expression to another. It does this by
   managing registers of legitimate conversions and casts, which are indexed by scale and aspect
   identifiers.   

Relationship between scales and references
------------------------------------------
An M-layer Reference is a digital record for a unit of measure, or other 
measurement reference (e.g., a certified reference material). It holds formats for 
rendering the reference, as well as other information and related external links. 

An M-layer scale is an association between a reference and a particular scale type (see :ref:`concept_m_expressions_scales`).

Expression conversion
---------------------
An expression can be converted from one scale to another if the operation has been registered.
The register can be queried by providing the unique identifiers of the source and destination (initial and final) 
scales. The unique identifier of the destination aspect is an additional optional argument.

Conversion in the M-layer is similar to conversion between units in traditional systems.
However, the M-layer distinguishes between two classes of conversion: 1) those that are independent of aspect; and 2) those that 
are only legitimate for certain aspects. 
An example of the first class is the conversion of an expression in metres to an expression in millimetres.
An example of the second class is the conversion of an expression of photon energy in electronvolts to an expression in terahertz. 

Expression conversion will *never* change the aspect. Usually, though not always, the type of scale will not change either
(an exception being conversion between temperature expressed in kelvin and degrees Celsius).

Expression casting 
------------------

Expression casting is used to change the aspect of an expression or when the casting operation is not an invariance transformation for the data. Such operations will be similar to what might be termed a 'change of variables'. For instance, a cast is required to change an expression of photon energy from terahertz to nanometres (i.e., the change is from a frequency to a wavelength). 

 
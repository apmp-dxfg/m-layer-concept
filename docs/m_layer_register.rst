.. _concept_m_register: 

The M-layer register of scales and aspects
==========================================

.. contents::
   :local:

M-layer uses compact digital objects to identify scales and aspects.
Each aspect, scale, and reference has a unique identifier, which can be used to access more detailed information in a central register. 

The register holds records of aspects, scales, and references (units or other types of reference),
and provides support for conversions and casting of expressions to different scales and aspects.
 
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
measurement reference (e.g., a certified reference material). The record holds information about the unit,
like formats for rendering, as well as related external links. 

An M-layer 'scale' is an association between a reference and a particular scale type (see :ref:`concept_m_expressions_scales`).

Expression conversion
---------------------
An expression can be converted from one scale to another when the operation to do so has been registered.

Scale conversion in the M-layer is similar to conversion in traditional unit systems.
However, the M-layer distinguishes between two types of conversion: 

    1) those that are legitimate for any aspect; and 
    2) those that are only legitimate for a particular aspect. 
    
An example of the first is conversion from metres to millimetres.
An example of the second is the conversion of an expression of photon energy in electronvolts to terahertz. 

Aspect-independent conversions are only permitted between scales of the same type, but
aspect-specific conversions may change the scale type (between ratio and interval scales); 
conversion *never* changes the aspect. 


Expression casting 
------------------

Expression casting can change the aspect as well as the type of scale for an expression. The distinction between conversion and casting is made so that operations which may substantially alter the data (casting operations) are kept separate from those that simply apply an invariance transformation. For instance, a cast is required to change an expression of photon energy from terahertz to nanometres (i.e., the change of variable is from frequency to wavelength), because wavelength is inversely related to frequency. 

 
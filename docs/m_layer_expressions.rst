.. _concept_m_expressions: 

The M-layer expression of measurement data
==========================================

.. contents::
   :local:

In traditional unit systems, like the SI, a quantity is expressed using two factors: a value and a name or symbol for a unit (e.g., 10 kg). 
The M-layer uses two or three components to express a datum: a token, a scale, or a token, a scale, and an aspect. 
These components are related to notions used in traditional unit systems. 

.. figure:: pictures/ExpressionClass.png
   :figwidth: 80%
   :align: center
   :alt: Class diagram for M-layer expression
   
   A UML class diagram showing an expression, consisting of: a token (value), 
   a scale and (optionally) an aspect (kind of quantity). 
   

Tokens
------

The token corresponds to the numeric factor in a traditional expression. A token will usually be numeric, but some data adopt symbols other than numbers, so the M-layer accommodates this possibility.

.. _concept_m_expressions_scales:

Scales
------
  

Scales combine a unit (or other reference) with information about the structure of data values. The additional information in a scale is sometimes helpful in distinguishing between closely related expressions. For example, a ratio scale associated with the unit degree Celsius is distinct from an interval scale associated with the same unit (the former could be for expression of a temperature difference whereas the latter would be used to express absolute temperature). 

The m-layer-concept includes 5 scale types. For each, there is a form of transformation that generates a different scale of the same type (an invariance transform). For example, multiplying values on a ratio scale by a positive real number produces another ratio scale.

.. list-table:: Scale types and invariance transforms. Note, here the 'mod' operator divides the left argument by the right and returns the remainder with the same sign as the right argument.
   :width: 75%
   :widths: 15 30
   :header-rows: 1

   * - Type
     - Invariance transforms
   * - ratio
     - :math:`x^\prime = a\, x ,\; a > 0`
   * - interval
     - :math:`x^\prime = a\, x + b ,\; a > 0`
   * - bounded-interval
     - :math:`x^\prime = (a\, x - x^\prime_\mathrm{low}) \;\text{mod}\; x^\prime_\mathrm{range} + x^\prime_\mathrm{low},\; a > 0`
   * - ordinal
     - any monotonic increasing function of :math:`x`
   * - nominal
     - any 1-to1 substitution for :math:`x`

Aspects
-------

The M-layer uses the component called aspect to represent the kind of quantity in an expression. Aspects may also be things that are not considered physical quantities (such as the intelligence of students, or the hardness of a material). 

In the SI, every unit can be expressed as a product of powers of base units (perhaps prefixed). However, this does not always identify a kind of quantity. There are 22 special unit names in the SI that are used for specific kinds of quantity, but many other cases are not supported.
The M-layer can use the aspect component to disambiguate legitimate conversion and casting operations for expressions based on kind of quantity information.



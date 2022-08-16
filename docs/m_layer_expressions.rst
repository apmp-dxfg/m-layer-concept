.. _concept_m_expressions: 

The M-layer expression of measurement data
==========================================

.. contents::
   :local:

The M-layer is intended to support the unambiguous representation of measurement data in digital systems. It does this in terms using *expressions*. 

In traditional unit systems, like the SI, a quantity is expressed using two factors: a value and a name or symbol for a unit (e.g., 10 kg). 
The M-layer goes further, using three components to express a datum: a token, a scale, and an aspect. 
These components allow the M-layer to represent a much wider range of measurement data than traditional unit systems. In some sense, these three components are generalisations of concepts used with traditional unit systems. 

.. figure:: pictures/ExpressionClass.png
   :figwidth: 80%
   :align: center
   :alt: Class diagram for M-layer expression
   
   A UML class diagram showing an expression an its associations 
   with token (value), scale and aspect (kind of quantity). Although 
   an aspect is not necessarily part of an expression, it is needed 
   to resolve some cases of ambiguity.
   

Tokens
------

A token corresponds to the numeric value in a traditional expression. A token will usually be numeric, but some measurement data adopt symbols other than numbers to denote a result, so the M-layer accommodates this possibility.

.. _concept_m_expressions_scales:

Scales
------
  

Traditional units do not convey information about the structure of data. However, the M-layer entities called scales associate a unit (or other reference) with information about the structure of data. This is used to manage changes of expression (conversion or casting) and is helpful in distinguishing between closely related expressions. For example, a ratio scale associated with unit degree Celsius is distinct from an interval scale associated with the same unit (the former would be appropriate for expression of a temperature difference whereas the latter would be used to express absolute temperature). 

There are 5 scale types in the M-layer. Each can be associated with a characteristic form of transformation that will generate a different scale of the same type (an invariance transform). For example, multiplying values on a ratio scale by a positive real number produces another ratio scale.

.. list-table:: Scale types and invariance transforms. Note, the operator 'mod' divides the left argument by the right and returns the remainder with the same sign as the right argument.
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

Unit systems like the SI do not make explicit reference to quantity. They take for granted that the kind of quantity can usually be inferred from contextual information. This poses a problem for digital systems, which need to operate in a systematic way. The M-layer uses the aspect component to represent the kind of quantity in an expression. The aspect is used to discern legitimate conversion and casting operations for expressions.

Aspect is interpreted more broadly than kind of quantity, because aspects may include things that are not considered physical quantities (such as the intelligence of students, or the hardness of a material). 

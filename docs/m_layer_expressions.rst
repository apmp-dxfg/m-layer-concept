.. _concept_m_expressions: 

The M-layer expression of measurement data
==========================================

.. contents::
   :local:

The M-layer is intended to support the unambiguous representation of measurement data in digital systems. It does this in terms using *expressions*. 

In traditional unit systems, like the SI, a quantity can be expressed using two factors: a value and a name or symbol for a unit (e.g., 10 kg). 
The M-layer goes further, using three components to express a datum: a token, a scale, and an aspect. 
These components allow the M-layer to represent a much wider range of measurement data than traditional unit systems. They are each, in some sense, generalisations of concepts used in traditional unit systems. 

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

An expression token corresponds to the numeric value in a traditional representation. In most cases, a token will be numeric but some kinds of measurement data use symbols rather than numbers to denote a result (e.g., a sequence of letters and numbers used to catalogue library books), so the M-layer accommodates this possibility.

.. _concept_m_expressions_scales:

Scales
------
  

Units do not convey information about the (numeric, or other) structure of results. So, the M-layer defines entities called scales that combine a unit or reference with information about the structure of data. This additional information can be used to control changes (conversion or casting) to expressions. 

There are currently 5 scale types in the M-layer. Each is associated with a particular form of transformation that will generate a new scale of the same type (an invariance transform). For example, multiplying the values on a ratio scale by a positive real number produces another ratio scale.

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
  
M-layer scales associate a unit, or some other reference, with a scale type. This is helpful in distinguishing between closely related expressions. For example, a ratio scale associated with unit degree Celsius is distinct from an interval scale associated with unit degree Celsius (the former could be appropriate for expression of a temperature difference whereas the latter would be used to express absolute temperature). 

Aspects
-------

Traditional systems like the SI do not make explicit reference to information about quantity in their expressions. Nevertheless, the kind of quantity is usually known implicitly from contextual information. This poses a problem for digital systems, because the kind of quantity cannot be deduced in a systematic way. The M-layer uses a third component, called aspect, to represent information about the kind of quantity in an expression. 

Aspect represents the nature of what is being measured and may be more general notion than kind of quantity. Aspects may include such things as the intelligence of a group of students, or the hardness of a material, neither of which is considered a physical quantity (like mass or length). The aspect is used to discern legitimate conversion and casting operations for expressions.  

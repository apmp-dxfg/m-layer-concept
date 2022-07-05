.. _intro_m_expressions: 

The M-layer expression of measurement data
==========================================

.. contents::
   :local:

The M-layer is intended to support the unambiguous representation of measurement data in digital systems. It does this in terms of digital expressions. 
In traditional unit systems, like the SI, a quantity is expressed using two factors: a value and a name or symbol for a unit (e.g., 10 kg). 
The M-layer goes further, using three components to express a datum: a token, a scale, and an aspect. 
These components are each, in some sense, generalisations of concepts from traditional unit systems. 
They allow the M-layer to represent a much wider range of measurement data than traditional unit systems.

Tokens
------

The token in an expression corresponds to the numeric value in a traditional representation. In most cases, the token will be numeric but there are some kinds of measurement data that use symbols rather than numeric values to denote a result (e.g., a sequence of letters and numbers used to catalogue library books), so the M-layer accommodates this possibility.

Scales
------

Units do not convey information about the (numeric, or other) structure of results. So, the M-layer defines entities called scales that combine a unit or reference with information about the structure of tokens. This additional information can be used to control changes (conversion or casting) of expressions. 

There are currently 5 scale types in the M-layer. For each, there is a characteristic form of transformation that generates a new scale of the same type. For example, multiplying the values on a ratio scale by a positive real number produces another ratio scale.

.. list-table:: Scale types and the transformations that leave the type of scale invariant. Note, the operator 'mod' divides the left argument by the right and returns the remainder with the same sign as the right argument.
   :widths: 15 30
   :header-rows: 1

   * - Type
     - Invariance transforms
   * - ratio
     - :math:`x^\prime = a\, x ,\; a > 0`
   * - interval
     - :math:`x^\prime = a\, x + b ,\; a > 0`
   * - bounded-interval
     - :math:`x^\prime = (a\, x - x^\prime_\mathrm{low}) \;\text{mod}\; x^\prime_\mathrm{range} + x^\prime_\mathrm{low}`
   * - ordinal
     - any monotonic increasing function of :math:`x`
   * - nominal
     - any 1-to1 substitution for :math:`x`
  
M-layer scales associate a unit, or reference, with a scale type. This is helpful in distinguishing between closely related expressions for data. For example, a ratio scale associated with unit degree Celsius is distinct from an interval scale associated with unit degree Celsius (the former would be appropriate for expression of a temperature difference whereas the latter would be used to express absolute temperature). 

Aspects
-------

Traditional systems like the SI do not explicitly include information in their expressions about quantity. Nevertheless, the kind of quantity is usually known implicitly from contextual information. This poses a problem for digital systems, because the kind of quantity cannot be deduced in a systematic way. The M-layer introduces a third component, called aspect, to represent information about the kind of quantity in an expression. 

The meaning of aspect is more general than kind of quantity. Aspect represents the nature of what is being measured, which may be such things as the intelligence of a group of students, or the hardness of a material, neither of which are considered as physical quantities such as mass and length. Aspects are needed to discern legitimate conversion and casting operations for expressions.  

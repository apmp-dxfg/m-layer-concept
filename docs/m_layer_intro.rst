.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

Why is the M-Layer needed?
==========================

The *International System of Units* (SI) has a few quirks. The names of many SI units are easily associated with particular types of quantity (like the kilogram and the metre, which are units of mass and length, respectively). So, we get used to thinking that the name of a unit will always identify the quantity. However, this is not correct because some units may be used to express several different quantities. The most obvious cases are quantities expressed with the SI unit 'one' (quantities of dimension zero, or dimensionless quantities, like aspect ratio, reflectance, refractive index, etc.).

There are also problems with units for temperature. You can legitimately express a temperature in kelvin or degrees Celsius in the SI. However, to convert between kelvin and degrees Celsius requires two arithmetic operations: addition and multiplication. No other SI units behave this way. Furthermore, a temperature difference can be also expressed in kelvin or degrees Celsius. This is a problem because you cannot tell if the quantity is a temperature or a temperature difference from the units alone. Moreover, in the case of temperature difference, conversion between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor). So the rules for conversion change for a temperature or a temperature difference, but you cannot choose the correct conversion method from the units alone.

Another difficulty with SI units occurs with plane angles. The SI unit for angle is the radian but the range of possible values may be limited. Sometimes the range extends from -pi to +pi, and sometimes from 0 to 2pi; in other cases there are no limits on a value of angle. This circular, or cyclic, property is again different from any other SI unit.

Although these may appear to be just exceptional cases, they are actually properties of measurement scales and units of measurement. 

The M-Layer provides support for these ideas to properly represent quantities and units in digital systems.  

What is the M-Layer?
====================

Traditionally, a quantity is expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, people use other contextual information to interpret such expressions. So, digital systems need more detailed representations. The M-Layer takes two extra things into account: 

    * the aspect being expressed (mass, temperature, angle, etc.)
    * the type of scale (based on the conversion operations required)
    
This allows digital systems to render data in different ways (including different units) according to user preferences.

The M-Layer extends the traditional notion of a unit, or reference, by combining a traditional unit with a scale type. This overcomes the ambiguity caused by allowing degrees Celsius to express temperature and temperature difference, because the types of scale are different. 

The M-Layer may be thought of as a triplet of information: an aspect, a value and an extended reference. We use the following notation for these components. For some arbitrary ``q``,  

    * Aspect: ``<q>`` 
    * Value: ``{q}`` 
    * Extended reference: ``[q]``
    
 
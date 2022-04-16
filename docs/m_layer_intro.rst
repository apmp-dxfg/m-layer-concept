.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

Why is the M-layer needed?
==========================

The *International System of Units* (SI) has a few quirks. For many SI units, the name is easily associated with a particular type of quantity (like the kilogram and the metre are units of mass and length, respectively). So, we get used to thinking that the name of a unit can identify the quantity involved. However, this is unreliable, because some units apply to different quantities. We must use information from the surrounding context to tell us exactly what a kind of quantity is referred to. The most obvious cases of ambiguity are those quantities that are expressed with the SI unit 'one' (quantities of dimension zero, or dimensionless quantities, like aspect ratio, reflectance, refractive index, etc.).

There are also problems with units for temperature. You can legitimately express a temperature in kelvin or degrees Celsius in the SI. However, to convert between kelvin and degrees Celsius requires two arithmetic operations: addition and multiplication. No other SI units are handled this way. Furthermore, a temperature difference can be also expressed in kelvin or degrees Celsius. So, you cannot tell if the quantity is a temperature or a temperature difference from the units alone. Moreover, conversion between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor) in the case of temperature difference. So the rules for conversion change according to whether the quantity is a temperature or a temperature difference, but you cannot choose the correct conversion method from the units alone.

Another difficulty with SI units is related to angle. The SI unit for angle is the radian but the SI does not specify the range of values. Sometimes, angle values are free to take on any value but often values are limited to a range of 2pi: sometimes the range extends from -pi to +pi while in other cases it ranges from 0 to 2pi. This circular, or cyclic, property of angle values is again different from any other SI unit.


Although these may appear to be just a few exceptional cases, they are features of measurement scales and units of measurement that are not recognised explicitly in the SI. 

The M-layer can represent quantities and units in digital systems because it provides rigorous support for these ideas.  

What is the M-layer?
====================

Traditionally, a quantity is expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, this is not enough for digital systems, because there is extra information that people use to interpret such expressions. The M-layer takes into account two extra things when expressing a quantity: 

    * the aspect of the quantity (mass, temperature, angle, etc.)
    * the type of scale (based on the conversion operations required)
    
This extra information allows a digital system to identify the aspect (the kind of quantity expressed) and to render it in different ways (including different units) according to user preferences.
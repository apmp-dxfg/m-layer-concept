.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

Why is the M-Layer needed?
==========================

The *International System of Units* (SI) has a few quirks. The names of many SI units are easily associated with particular types of quantity (like the kilogram and the metre, which are units of mass and length, respectively). So, we get used to thinking that the name of a unit will always identify the quantity. However, this is not correct because some units may be used to express several different quantities. The most obvious cases are quantities expressed with the SI unit 'one' (quantities of dimension zero, or dimensionless quantities, like aspect ratio, reflectance, refractive index, etc.).

There are also problems with units for temperature in the SI. You can legitimately express a temperature in kelvin or degrees Celsius. However, to convert between kelvin and degrees Celsius requires both addition and multiplication. No other SI units behave this way. Furthermore, a temperature difference can be expressed in the same units, kelvin or degrees Celsius. So, you cannot tell if the quantity is a temperature or a temperature difference from the units alone. Moreover, in the case of temperature difference, conversion between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor). So, the rules for conversion are different for a temperature and a temperature difference, but you cannot choose the correct conversion method from the units alone.

Another difficulty occurs with plane angles. The SI unit for angle is the radian but the range of possible values is not specified and can be limited. Sometimes the range extends from -pi to +pi, and sometimes from 0 to 2pi; in other cases there are no limits. This circular, or cyclic, property is quite different from any other SI unit.

Although these examples may appear to be exceptional cases, they actually reflect properties of measurement scales and units of measurement. To properly represent quantities and units in digital systems, the M-Layer provides support for these properties.  

What is the M-Layer?
====================

Traditionally, a quantity is expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, people use contextual information to interpret such expressions. So, digital systems need more detailed representations. The M-Layer takes two extra things into account: 

    * the aspect being expressed (mass, temperature, angle, etc.)
    * the type of scale (the conversion operations required)
    
This additional information allows digital systems to render data in different ways (including different units) according to user preferences.

The M-Layer extends the traditional notion of a unit, or reference, by combining a traditional unit with a scale type. This overcomes the ambiguity caused by allowing degrees Celsius to express temperature and temperature difference, because the types of scale are different. An absolute temperature expressed in degrees Celsius belongs to what is called an interval scale, whereas a temperature difference in degrees Celsius belongs to a ratio scale.

The M-Layer holds a triplet of information. For some arbitrary ``q``, there is: 

    * an aspect, ``<q>``; 
    * a value, ``{q}``; 
    * and an extended reference, ``[q]``.  
 
Here is a brief example involving mass ::

    from m_layer import *
    
    def display(av):
        print(av)       # String format
        print(repr(av)) # Representation format
        print()

    x = AspectValue(aspect.mass,12,si_unit.kg)
    display(x)

    y = x.convert(imperial_unit.pound)
    display(y)

The ``AspectValue`` object ``x`` is created by specifying an aspect, a value and a reference. A different ``AspectValue`` object ``y`` can be obtained by converting to another legitimate unit. 

Although elements like ``si_unit.kg`` are readable here, such names refer to unique digital identifiers in the M-Layer. 

The script produces the following output::

    12.00000 kg
    AspectValue(mass,12.00000,kilogram)

    26.45520 lb
    AspectValue(mass,26.45520,pound)
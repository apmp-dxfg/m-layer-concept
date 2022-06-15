.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

Why is the M-Layer needed?
==========================

The *International System of Units* (SI) has a few quirks. Many SI unit names are easy to associate with particular types of quantity (like the kilogram and the metre, which are units of mass and length, respectively). So, we get used to thinking that the name of a unit will always identify the quantity. However, that is not correct. Some units may be used to express several different quantities. The most obvious cases are quantities expressed with the SI unit 'one' (quantities of dimension one, or dimensionless quantities, like aspect ratio, reflectance, refractive index, etc.).

There are also problems with the units for temperature in the SI. You can legitimately express a temperature in kelvin or degrees Celsius. However, to change an expression between kelvin and degrees Celsius requires two operations: an addition and a multiplication. No other SI units behave this way. Furthermore, a temperature difference can be expressed in the same units, kelvin or degrees Celsius. So, you cannot tell from the units alone whether a quantity is a temperature or a temperature difference. Moreover, in the case of temperature difference, conversion between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor). So, the method of conversion is different for a temperature or a temperature difference, but you cannot distinguish between them from the units alone.

Another difficulty occurs with plane angles. The name of the SI unit for angle is radian, but the range of values is not specified and can be limited. Sometimes the range extends from -pi to +pi, and sometimes from 0 to 2pi; in other cases there are no limits. This circular, or cyclic, property is quite different from any other SI unit.

These are just exceptional cases that arise, but they reflect properties of measurement scales and units of measurement that the SI fails to support. To properly represent a wide range of quantities and units in digital systems, these properties should be handled better.  

What is the M-Layer?
====================

A quantity is usually expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, there is always more contextual information available that people use to interpret expressions. Digital systems are not as good as people at handling ambiguity, so they will need more detailed representations. 

The M-Layer takes two more things into account: 

    * the nature what is being expressed (mass, temperature, angle, etc.)
    * the type of scale being used (relates to conversion operations)
    
The M-Layer extends the traditional notion of a unit, or reference, by combining units with scale types. These new entities are called M-layer 'scales'. These scales can overcome the ambiguity caused, for example, by allowing degrees Celsius to express both temperature and temperature difference, because the type of scale is different in each case. 

The M-Layer expresses measurement data in terms of three components. For some datum ``q``, there is: 

    * an aspect, ``<q>``; 
    * a value, ``{q}``; 
    * and a scale, ``|[q]|``.  
 
The term 'aspect' has similar meaning to 'kind of quantity', as used in the context of SI units.

Here is a simple example involving mass. The script creates an object ``x`` as an expression of 12 kg. It then converts this to create another object ``y``, which is an expression of the same mass in Imperial pounds. ::

    from m_layer import *
    
    ml_mass = ('ml-mass', 321881801928222308627062904049725548287)

    ml_kg = ('ml-si-kilogram-ratio', 12782167041499057092439851237297548539)
    ml_lb = ('ml-imp-pound-ratio', 188380796861507506602975683857494523991)
    
    def display(xp):
        print(xp)       # String format
        print(repr(xp)) # Representation format
        print()

    x = Expression(ml_mass,12,ml_kg)
    display(x)

    y = x.convert(ml_lb)
    display(y)

The function ``display()`` is used to produce this output::

    12.00000 kg
    Expression(mass,12.00000,kilogram)

    26.45520 lb
    Expression(mass,26.45520,pound)
    
The initial object ``x`` is specified by an aspect, a value and a scale. The object ``y`` is obtained by converting to another unit. The M-layer will check that the conversion is legitimate.

The M-layer keeps a register of information about aspects and scales, and legitimate conversions. The client software only needs to use objects that identify M-layer records. The lines near the top of the script show this ::

    ml_mass = ('ml-mass', 321881801928222308627062904049725548287)

    ml_kg = ('ml-si-kilogram-ratio', 12782167041499057092439851237297548539)
    ml_lb = ('ml-imp-pound-ratio', 188380796861507506602975683857494523991)
 
The tuples on the right are M-layer identifiers. They combine a compound name with a universal unique identifier (UUID) in integer format. The compound name will help people to recognise different objects but need not be unique. These tuples can be given convenient Python names, as suggested here (``ml_kg``, etc.). 


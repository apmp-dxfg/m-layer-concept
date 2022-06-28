.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

Why is the M-layer needed?
==========================

The *International System of Units* (SI) has a few quirks. Many SI unit names are easy to associate with a particular type of quantity (like the kilogram and the metre, which are used as units of mass and length, respectively). So, we get used to thinking that the name of a unit will identify the quantity. However, that is not always correct. The same units may be used to express different quantities. The most obvious example being quantities expressed with the SI unit 'one' (quantities of dimension one, or 'dimensionless' quantities, like aspect ratio, reflectance, refractive index, etc.).

There are also problems with the units for temperature. You can legitimately express a temperature in kelvin or degrees Celsius in the SI. However, to convert a temperature between kelvin and degrees Celsius requires two operations: addition and multiplication. No other SI units behave this way. Furthermore, those same units can be used when expressing temperature differences, which is especially problematic because conversion of temperature differences between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor). So, you cannot tell whether a quantity is a temperature or a temperature difference from the units alone but you would need to know that to perform unit conversion. 

Another difficulty occurs with plane angles. The name of the SI unit for angle is radian, but the range of values is not specified and can be limited. Sometimes the range extends from -pi to +pi, and sometimes from 0 to 2pi; in other cases there are no limits. This circular, or cyclic, property is quite different from any other SI unit.

Although these are just exceptional cases, they reflect properties of measurement scales and units of measurement that the SI cannot support properly. To represent a wide range of quantities and units in digital systems, these properties should be handled better.  

What is the M-layer?
====================

A quantity is traditionally expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, to interpret expressions, people can use other contextual information as well. 

Digital systems are not as good as people at handling ambiguity, so the M-layer addresses the need for unambiguous and legitimate conversion of digital data. It does this by taking into account: 

    * the type of scale being used (relates to conversion operations)
    * the nature what is being expressed (mass, temperature, angle, etc.)
    
The first point is handled by combining units with scale types to extend the traditional notion of a unit, or reference. These new entities overcome the ambiguity caused, for example, by allowing degrees Celsius to express both temperature and temperature difference, because the type of scale is different in each case. They are called M-layer 'scales'.

The second point is handled by explicitly registering different kinds of quantity. We call this new component the 'aspect'. The meaning of 'aspect' is similar to, but broader than, 'kind of quantity' as used in relation to SI units.

The M-layer can express data with three components. For some datum ``q``, there is: 

    * a value, ``{q}``; 
    * a scale, ``|[q]|``.  
    * an aspect, ``<q>``; 

Here is a simple example involving mass. The script creates an expression of 12 kg and then converts it to an expression in Imperial pounds. ::

    from m_layer import *
    
    ml_mass = Aspect( (
                'ml-mass', 
                321881801928222308627062904049725548287
            ) )

    ml_kg = Scale( (
                'ml-si-kilogram-ratio', 
                12782167041499057092439851237297548539
            ) )
    ml_lb = Scale( (
                'ml-imp-pound-ratio', 
                188380796861507506602975683857494523991
            ) )
    
    def display(xp):
        print(xp)       # String format
        print(repr(xp)) # Representation format
        print()

    x = Expression(12,ml_kg,ml_mass)
    display(x)

    y = x.convert(ml_lb)
    display(y)

The objects ``x`` and ``y`` are different digital expressions of the same physical quantity. The values of ``x`` and ``y`` are different, as are their scales, but the aspect is the same. 

The function ``display()`` is used to produce this output::

    12.00000 kg
    Expression(12.00000,kilogram,mass)

    26.45520 lb
    Expression(26.45520,pound,mass,)
   
M-layer identifiers 
-------------------
   
The M-layer maintains a register of information about aspects, scales, and conversions. Client software uses objects that can index M-layer records containing more details. 

The lines near the top of the script above declare convenient Python names for local aspects and scales (``ml_kg``, etc.). The tuples that initialise ``Aspect`` and ``Scale`` classes, on the right, are M-layer identifiers. Each tuple has two elements: a compound name, and a universal unique identifier (UUID) in integer format. The name is intended to help people to recognise different objects but need not be unique.  


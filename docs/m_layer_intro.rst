.. _intro_m_layer: 

############
Introduction
############

.. contents::
   :local:

The m-layer-concept project
===========================

This is a proof-of-concept project to demonstrate use of the M-layer for representations of units of measurement and other forms of annotation of measurement data. The M-layer itself is a formalism that extends the ideas used in traditional unit formats, to address problems of ambiguity. It has been developed for digital systems and is intended to foster reuse and interoperability of measurement data.

The need for alternatives to traditional notations can be seen by looking at a few of the difficulties that arise when using the *International System of Units* (SI).

Many SI unit names may be associated with a particular type of quantity (like the kilogram and the metre, which are associated with mass and length, respectively). So, we are used to thinking that the name of a unit will identify the quantity. However, that is not always correct. The same unit may sometimes express quite different quantities. The most obvious example being the SI unit 'one' (aspect ratio, reflectance, refractive index, etc., may all be expressed in terms of the unit one, but are quite different quantities).

There are also difficulties with the units for temperature in the SI. You can legitimately express a temperature in kelvin or degrees Celsius. However, conversion between kelvin and degrees Celsius requires two operations: addition and multiplication. No other SI units behave this way under conversion. Furthermore, a temperature difference can be expressed in the same units, kelvin or degrees Celsius. Yet conversion of temperature differences between kelvin and degrees Celsius *only* involves multiplication (by a conversion factor). So, the method of conversion is different for a temperature and a temperature difference, but the quantity cannot be identified from the units alone.  

A different difficulty occurs with plane angles. The special name of the SI unit for angle is radian, but the range of values is not specified. Sometimes the range of values extends from :math:`-\pi` to :math:`+\pi`, and sometimes from :math:`0` to :math:`2\pi`, while in other cases there are no limits. This circular, or cyclic, structure of data is quite different from any other SI unit.

These are just a few exceptional cases for the SI, but they illustrate properties of measurement data that cannot be supported by the SI format. The M-layer addresses these difficulties, and, in doing so, provides support for a wider range of measurement data.  

What is the M-layer?
====================

A quantity is traditionally expressed by pairing a number with the name, or symbol, for a unit, like 10 kg. However, people use contextual information to interpret such expressions. Digital systems are not as good as people at handling ambiguity, so the M-layer takes into account: 

    * the type of scale being used (relates to conversion operations)
    * the nature of what is being expressed (mass, temperature, angle, etc.)
    
The first point is addressed by extending the traditional idea of a unit (or reference). In the M-layer, an entity called a *scale* associates a unit (or reference) with a type of scale. Scales remove the sort of ambiguity caused, for example, by using the degree Celsius to express both temperature and temperature difference.

The second point is addressed by explicitly capturing the kind of quantity in expressions. This introduces an extra component to expressions called *aspect*. 
   
M-layer identifiers 
-------------------
   
An M-layer maintains records about aspects and scales in a register of information. Client software deals with digital objects that are references to these M-layer records. 

In the example below, convenient Python names are assigned to refer to ``Aspect`` and ``Scale`` objects (``kg``, etc.) that encapsulate unique M-layer identifiers. The tuple that initialises these objects has two elements: a name, and a universal unique identifier (UUID) in integer format.   

Example
-------
The code generates an expression for 12 kg and converts it to the Imperial unit pounds. 

The function ``display()`` outputs the short (``str``) and long (``repr``) Python string representations.

First, local names are assigned to aspect and scale objects (``mass``, ``kg``, and ``lb``). 

The expression ``x`` combines the value 12 with the ``kg`` scale and the ``mass`` aspect. The expression is then converted to Imperial pounds. ::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()

    >>> mass = Aspect( ('ml_mass',321881801928222308627062904049725548287) )
    >>> kg = Scale( ('ml_si_kilogram_ratio',12782167041499057092439851237297548539) )
    >>> lb = Scale( ('ml_imp_pound_ratio',188380796861507506602975683857494523991) )
    
    >>> x = expr(12,kg,mass)
    >>> display(x)
    12 kg
    Expression(12,kg,mass)
    <BLANKLINE>
    >>> display(x.convert(lb))
    26.4552 lb
    Expression(26.4552,lb,mass)
    <BLANKLINE>
    
It is worth noting that aspect is not a mandatory component. Aspect is available to remove problems of ambiguity in certain cases and to extend the interoperability of measurement data; but, the example above can also be handled in this way:: 

    >>> y = expr(12,kg)
    >>> display(y)
    12 kg
    Expression(12,kg)
    <BLANKLINE>
    >>> display(y.convert(lb))
    26.4552 lb
    Expression(26.4552,lb)
    <BLANKLINE>
    
A scale alone may is sufficient to express the magnitude (as with standard SI formats). 
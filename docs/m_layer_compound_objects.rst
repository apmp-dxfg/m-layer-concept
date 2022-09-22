.. _concept_m_compound_objects: 

==================================
Arithmetic with scales and aspects
==================================

.. contents::
   :local:

There is a widely-held belief that units of measurement can be generated simply by multiplying other units together. This is a misunderstanding. Notwithstanding, unit composition is a useful way to express measured quantities, and is supported in the m-layer-concept software. 

.. note::

    Another widely-held belief is that quantity calculus applies to measurement data expressed in any format. That too is a misunderstanding. M-layer client-side software does support multiplication of aspects. However, this is an exploratory feature that does not yet have a recognised application. 

The problem with unit arithmetic 
================================

Unit multiplication is sensible if the units themselves are considered conversion factor variables. For example, a speed expressed as 50 km/h, may be converted to 13.89 m/s by knowing that kg = 1000 m and h = 3600 s. The unit names, km/h and m/s, actually encode the dimensions of speed, L.T-1. They describe a formula for unit conversion. However, the problem that software has to deal with is situations when the dimensions of a compound unit can be associated with several different explicit units (e.g., the fact that kg m2 s-2 may be considered equivalent to N m -- for torque -- or J -- for work). User intervention is needed to specify the correct unit. 

Compound scales 
===============

Speed
~~~~~

Speed provides a simple example of how m-layer-concept software works with compound units. 

We first declare scales for length and time ::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()

    >>> m = Scale( ('ml_si_metre_ratio', 17771593641054934856197983478245767638) )
    >>> s = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )
    
A compound unit for speed can be used in an expression ::

    >>> m_s = m/s 
    >>> print( m_s ) 
    m/(s)
    >>> v = expr(1.5, m/s )
    >>> print( v )
    1.5 m/(s)
    
Other compound units for speed could be created ::

    >>> ft = Scale( ('ml_foot_ratio', 150280610960339969789551668292960104920) )
    >>> minute = Scale( ('ml_si_minute_ratio', 219754916679293138667106941253484129447 ) )
    <BLANKLINE>
    >>> ft_min = ft/minute 
    >>> print( ft_min ) 
    ft/(min)
    
Conversion between expressions is possible (the arithmetic scale expressions must have exactly the same form) ::

    >>> print( v.convert( ft_min ) )
    295.2756 (ft/(min))
    
Note, the compound scale objects above were not resolved a scale for speed. However, a compound scale expression can be converted to a corresponding scale. There is an m-layer-concept scale for speed, so it is possible to convert the compound unit expression to a single unit expression ::

    >>> m_per_s = Scale( ("ml_si_m.s-1_ratio",263223643595076551490114979345460778542) )
    <BLANKLINE>
    >>> print( repr(v) )
    Expression(1.5,m/(s))
    >>> print( v.convert(m_per_s) )
    1.5 m.s-1
    
Energy or moment of force
~~~~~~~~~~~~~~~~~~~~~~~~~

The SI defines the special name joule for the unit of energy and recommends the compound name newton metre for the unit of moment of force. Nevertheless, the systematic compound unit name kilogram metre squared per second squared (kg.m2.s-2) in a valid alternative in each case. 

Scales for kilogram, metre and second are available, so it is possible to form a compound scale for kg.m2.s-2 and use it to express data ::

    >>> kg = Scale( ('ml_si_kilogram_ratio', 12782167041499057092439851237297548539) )
    >>> m = Scale( ('ml_si_metre_ratio', 17771593641054934856197983478245767638) )
    >>> s = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )

    >>> kg_mm_ss = kg*m**2/s**2
    >>> print(kg_mm_ss)
    kg.m^2/(s^2)
    >>> w = expr(10.1,kg_mm_ss)
    >>> print( w )
    10.1 kg.m^2/(s^2)

However, this format does not distinguish between energy and moment of force. The compound scale cannot infer the correct aspect, so a cast is needed. By declaring the aspects ::

    >>> energy = Aspect( ("ml_energy", 12139911566084412692636353460656684046) )
    >>> moment = Aspect( ("ml_force_moment", 313648474034040825357489751369673453388) )
    
and the scales ::

    >>> J = Scale( ("ml_si_joule_ratio",165050666678496469850612022016789737781) )
    >>> N_m = Scale( ("ml_si_N.m_ratio",180123565723874772354088506298557924442) )

it is possible to change from the systematic representation to one that is quantity-specific ::

    >>> print(w.cast(ScaleAspect(J,energy)))
    10.1 J
    
or ::

    >>> print(w.cast(ScaleAspect(N_m,moment)))
    10.1 N m
    
What is the m-layer-concept doing?
==================================

The m-layer-concept code works with compound-scale expressions, because M-layer register does not hold compound scales. Individual scales in one compound-scale expression can be matched, one by one, with scales in another expression. This requires the two expressions to have exactly the same arithmetic form.

Conversion from a compound-scale expression to a single M-layer scale is not always possible. The m-layer-concept requires all scales in an expression to be associated with a unit system, so they are ratio scales and the associated references each have dimensions in that system. Using this information, the compound-scale dimensions can be evaluated. Then the compound scale can be converted to a corresponding systematic scale, if defined in the register.   

This process is subject to the usual difficulties associated with dimensional representations for units: there may be more than one scale defined with given dimensions. This situation can be handled by using a casting operation to specify the correct scale.
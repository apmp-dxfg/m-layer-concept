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

Speed provides a simple example of how m-layer-concept software works with compound units. 

We first declare scales for length and time ::

    >>> m = Scale( ('ml_si_metre_ratio', 17771593641054934856197983478245767638) )
    >>> s = Scale( ('ml_si_second_ratio', 276296348539283398608930897564542275037) )
    
A compound unit for speed can be used in an expression ::

    >>> m_s = m/s 
    >>> print( m_s ) 
    m/(s)
    >>> v = expr(1.5, m/s )
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
    
Note, the compound scale objects above were not resolved a scale for speed. However, a compound scale expression can be converted to a corresponding scale. There is an m-layer-concept scale for speed, so it is possible to cast the compound unit expression to a single unit expression ::

    >>> m_per_s = Scale( ("ml_si_m.s-1_ratio",263223643595076551490114979345460778542) )
    <BLANKLINE>
    >>> print( repr(v) )
    Expression(1.5,m/(s))
    >>> print( v.convert(m_per_s) )
    Expression(1.5,m.s-1)
    
What is the m-layer-concept doing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The M-layer register does not hold compound scales, but m-layer-concept code uses the compound-scale expressions. Individual scales in one compound-scale expression can be matched, one by one, with scales in another expression. This requires the two expressions to have exactly the same arithmetic form.

Conversion from a compound-scale expression to a single M-layer scale is not always possible. The m-layer-concept requires all scales in an expression to be associated with a unit system, so they are ratio scales and the associated references each have dimensions in that system. Using this information, the compound-scale dimensions can be evaluated. Then the compound scale can be converted to a corresponding systematic scale, if defined in the register.   

This process is subject to the usual difficulties associated with dimensional representations for units: there may be more than one scale defined with given dimensions. This situation can be handled by using a casting operation to specify the correct scale.
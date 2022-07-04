.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature data
================

Temperature offers some interesting examples of difficulties with unambiguous expressions of measured data.


Absolute temperature
--------------------

Firstly, there is the distinction between ratio scales and interval scales. The M-layer will allow conversion of an expression to another scale of the same type without knowing the aspect. 
So, conversion between Fahrenheit and degree Celsius can be carried out::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()
    
    >>> celsius_interval = Scale( ('ml-si-celsius-interval', 245795086332095731716589481707012001072) )
    >>> fahrenheit = Scale( ('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767) )
    
    >>> t = expr(72,fahrenheit)
    >>> display(t)
    72 degree F
    Expression(72,fahrenheit)
    <BLANKLINE>
    >>> t_C = t.convert(celsius_interval)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,celsius)
    <BLANKLINE>

However, a casting operation to a different type of scale must be able to identify, or infer, an aspect for the initial expression.
The M-layer will not allow an expression to be cast without information about the aspect. For example, ::

    >>> kelvin = Scale( ('ml-si-kelvin-ratio', 302952256288207449238881076502466548054) )

    >>> t_K = cast(t_C,kelvin)
    Traceback (most recent call last):
    ...
    RuntimeError: Expression(22.22222222222222,celsius) has no declared aspect, so it cannot be cast

Information about the aspect can be specified when initially creating an expression, or injected during later conversions, as shown below. However, once specified, conversion opertions cannot change the aspect. Only casting may change a specific aspect in the initial expression to a different one in the final expression. :: 

    >>> T = Aspect( ('ml-temperature', 316901515895475271730171605211001099255) )
    
    >>> t_C = t.convert(celsius_interval,T)     # Inject the aspect 'T'
    >>> t_K = cast(t_C,kelvin)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,kelvin,temperature)
    <BLANKLINE>
    
Temperature difference  
----------------------

The nuance between units for temperature and temperature difference is manageable with the M-layer. For example, a temperature difference expressed in degree Celsius is not convertible to Fahrenheit, because the type of scale is different::

    >>> celsius_ratio = Scale( ('ml-si-celsius-ratio', 278784445377172064355281533676474538407) )

    >>> t_diff_C = expr(10,celsius_ratio)
    >>> display(t_diff_C)
    10 degree C
    Expression(10,celsius)
    <BLANKLINE>
    >>> t_diff_C.convert(fahrenheit)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-celsius-ratio', 278784445377172064355281533676474538407)) to Scale(('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767))

It is, however, convertible to kelvin::

    >>> display( t_diff_C.convert(kelvin) )
    10 K
    Expression(10,kelvin)
    <BLANKLINE>
    
It is important to note that these expressions have left the aspect undefined, so the illegal conversion is detected requesting a change of scale type during conversion. The following conversion would be allowed, because the aspect was not specified earlier ::

    >>> display( t_diff_C.convert(kelvin,T) )
    10 K
    Expression(10,kelvin,temperature)
    <BLANKLINE>
    
Explicit use of aspects  will avoid ambiguity and is recommended. If an aspect had been specified initially, the illegal conversion above could have been detected, as shown below. 

    >>> dT = Aspect( ('ml-temperature-difference', 212368324110263031011700652725345220325) )

    >>> t_diff_C = expr(10,celsius_ratio,dT)
    >>> display(t_diff_C)
    10 degree C
    Expression(10,celsius,temperature-difference)
    <BLANKLINE>
    >>> display( t_diff_C.convert(kelvin,T) )
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: [Aspect('ml-temperature-difference', 212368324110263031011700652725345220325), Aspect('ml-temperature', 316901515895475271730171605211001099255)]
    
Working with scale-aspect pairs
-------------------------------

Often pairs of scales and aspects that provide a convenient way of expressing data in a particular context can be identified. The M-layer provides a class to encapsulate scale-aspect pairs :class:`~scale_aspect.ScaleAspect`. Here, the cases shown above are handled with scale-aspect pairs::

    >>> celsius_dT = ScaleAspect( celsius_ratio, dT )
    >>> celsius_T = ScaleAspect( celsius_interval, T )
    >>> fahrenheit_T = ScaleAspect( fahrenheit, T )
    >>> kelvin_T = ScaleAspect( kelvin, T )
    >>> kelvin_dT = ScaleAspect( kelvin, dT )
    
    >>> t = expr(72,fahrenheit_T)
    >>> display(t)
    72 degree F
    Expression(72,fahrenheit,temperature)
    <BLANKLINE>
    >>> t_C = t.convert(celsius_T)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,celsius,temperature)
    <BLANKLINE>

    >>> t_K = cast(t_C,kelvin_T)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,kelvin,temperature)
    <BLANKLINE>

    >>> t_diff_C.convert(fahrenheit_T)
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: [Aspect('ml-temperature-difference', 212368324110263031011700652725345220325), Aspect('ml-temperature', 316901515895475271730171605211001099255)]
    
.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature
===========

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

However, a conversion to a different type of scale must be able to identify, or infer, the aspect of the initial expression.
The M-layer will not allow an expression to be converted without this information. For example, ::

    >>> kelvin = Scale( ('ml-si-kelvin-ratio', 302952256288207449238881076502466548054) )

    >>> t_K = convert(t_C,kelvin)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-celsius-interval', 245795086332095731716589481707012001072)) to Scale(('ml-si-kelvin-ratio', 302952256288207449238881076502466548054))

Information about the aspect can be specified when initially creating an expression, or injected during conversion, as shown below. However, once specified, conversion operations cannot change the aspect. Only casting may change a specific aspect in the initial expression to a different one in the final expression. :: 

    >>> T = Aspect( ('ml-temperature', 316901515895475271730171605211001099255) )
    
    >>> t_C = t.convert(celsius_interval,T)     # Inject the aspect 'T'
    >>> t_K = convert(t_C,kelvin)
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
    
Scale-aspect pairs
------------------

Often, paired scales and aspects provide a convenient way of expressing data in a particular context. The M-layer has the :class:`~scale_aspect.ScaleAspect` class to encapsulate scale-aspect pairs. The following code uses scale-aspect pairs to handle the cases shown above::

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

    >>> t_K = convert(t_C,kelvin_T)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,kelvin,temperature)
    <BLANKLINE>

    >>> t_diff_C.convert(fahrenheit_T)
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: [Aspect('ml-temperature-difference', 212368324110263031011700652725345220325), Aspect('ml-temperature', 316901515895475271730171605211001099255)]
  
Plane angle
===========
  
Plane angle is an interesting case because values are often expressed with bounded and cyclic, or circular values. This means that conversion between expressions of plane angle is quite different from other types of scale.

Scales for plane angle
----------------------

Radian is the special name for the SI unit of plane angle (plane angle is actually a quantity of dimension one in the SI, so the unit one is also allowed). The degree may also be used with the SI. Expressions need not place bounds on the value. However, digital systems frequently impose circular or cyclic limits on values.  Either the lower bound is zero and the upper bound corresponds to one full rotation (:math:`2 \pi` radians or :math:`+360` degrees), or the lower bound corresponds to half a full rotation clockwise (:math:`-\pi` radians or :math:`-180` degrees) and the upper bound to half a full rotation counter-clockwise (:math:`+\pi` radians or :math:`+180` degrees). 

The M-layer has a particular scale type for bounded cyclic scales. So, M-layer scales can be defined for the different cases::

    >>> plane_angle = Aspect( ('ml-plane-angle', 95173225557230344956477808929590724690) )
    
    >>> radian_ratio = Scale( ('ml-si-radian-ratio', 273301153578020696303516833405033923738) )
    >>> radian_bounded_two_pi = Scale( ('ml-si-radian-bounded-two-pi', 300556212736422769570885306883285535638) )
    >>> ml_si_radian_bounded_pi = Scale( ('ml-si-radian-bounded-pi', 181367268705518406168243034119604185497) )
    
    >>> degree_ratio = Scale( ('ml-imp-degree-ratio', 124567088583703716502057160299542649451) )
    >>> degree_bounded_180 = Scale( ('ml-imp-degree-bounded-180', 273805538217618733078298377573965188309) )
    >>> degree_bounded_360 = Scale( ('ml-imp-degree-bounded-360', 125066222841962802760576607996391537405) )
    
An angle can be converted between bounded scales::

    >>> a = expr(-90,degree_bounded_180)
    >>> display(a)
    -90 deg
    Expression(-90,degree)
    <BLANKLINE>
    >>> display( convert(a,degree_bounded_360) )
    270 deg
    Expression(270,degree)
    <BLANKLINE>
    
To change between bounded and unbounded scales in an expression may result in loss of information, so an explicit cast is required which in turn means the initial expression 
needs to specify an aspect. 

    >>> a = expr(-90,degree_bounded_180,plane_angle)
    >>> display( cast(a,radian_ratio) )
    -1.5707963267948966 rad
    Expression(-1.5707963267948966,radian,plane-angle)
    <BLANKLINE> 
  
Spectroscopic data
==================  
Although there are different kinds of optical spectroscopy, in many cases data can be thought of as the response of a sample to stimulus at a specific energy (photon energy). Data will typically be presented with the energy of incident photons along the abscissa (x-axis) and response along the ordinate (y-axis).

For abscissa data, energy may be expressed in different units, such as electronvolts (:math:`\text{eV}`),  nanometers (:math:`\text{nm}`), wavenumber (:math:`\text{cm}^{-1}`) and terahertz (:math:`\text{THz}`). These units are normally associated with different aspects (energy, length, inverse length, and frequency, respectively). However, they are used because of the simple relationships between these quantities for photons (:math:`E = h\, \nu`, :math:`E = h\, c \, \tilde{\nu}`, etc, where :math:`E` is photon energy, :math:`h` is Planck's constant, :math:`c` is the speed of light, :math:`\nu` is frequency, and :math:`\tilde{\nu}` is wavenumber). 

It is possible to express abscissa data without ambiguity by specifying the aspect as photon energy::

    >>> photon_energy = Aspect( ('ml-photon-energy', 291306321925738991196807372973812640971) )
    >>> energy = Aspect( ('ml-energy', 12139911566084412692636353460656684046) ) 
    
    >>> electronvolt = Scale( ('ml-electronvolt-ratio', 121864523473489992307630707008460819401) )
    >>> terahertz = Scale( ('ml-si-terahertz-ratio', 271382954339420591832277422907953823861) )
    >>> per_centimetre = Scale( ('ml-si-per-centimetre-ratio', 333995508470114516586033303775415043902) )
    >>> nanometre = Scale( ('ml-si-nanometre-ratio', 257091757625055920788370123828667027186) )
    
Abscissa data may then be expressed and converted correctly::

    >>> x = expr(1,electronvolt,photon_energy)
    >>> display(x)
    1 eV
    Expression(1,electronvolt,photon energy)
    <BLANKLINE>
    >>> display( x.convert(terahertz) ) 
    241.79892420849183 THz
    Expression(241.79892420849183,terahertz,photon energy)
    <BLANKLINE>
    >>> display( x.convert(per_centimetre) )
    8065.543937349211 1/cm
    Expression(8065.543937349211,per centimetre,photon energy)
    <BLANKLINE>

The wavelength is inversely related to energy (:math:`\lambda = h\,c / E`), so a cast, rather than a conversion, is required::

    >>> display(x.cast(nanometre)) 
    1239.8419843320025 nm
    Expression(1239.8419843320025,nanometre,photon energy)
    <BLANKLINE>
    
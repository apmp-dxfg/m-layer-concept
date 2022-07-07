.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature
===========

There are several interesting examples of difficulties with unambiguous expressions of measured data provided by temperature.


Absolute temperature
--------------------

Firstly, there is the distinction between ratio scales and interval scales. 

M-layer conversion of an expression will not change the aspect, but conversion may change the type of scale.  For example, conversion between Fahrenheit and degree Celsius can be carried out::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()
    
    >>> celsius_interval = Scale( ('ml-si-celsius-interval', 245795086332095731716589481707012001072) )
    >>> fahrenheit_interval = Scale( ('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767) )
    
    >>> t = expr(72,fahrenheit_interval)
    >>> display(t)
    72 degree F
    Expression(72,fahrenheit)
    <BLANKLINE>
    >>> t_C = t.convert(celsius_interval)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,celsius)
    <BLANKLINE>

Conversion to a different type of scale must take account of the aspect of the initial expression.
The M-layer will not allow an expression to be converted without this information. For example, ::

    >>> kelvin = Scale( ('ml-si-kelvin-ratio', 302952256288207449238881076502466548054) )

    >>> t_K = convert(t_C,kelvin)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-celsius-interval', 245795086332095731716589481707012001072)) to Scale(('ml-si-kelvin-ratio', 302952256288207449238881076502466548054))

Information about the aspect can be specified when initially when creating an expression, or injected during later conversion, as shown below. Once specified, conversion operations cannot change the aspect (only casting may change the aspect of an expression). :: 

    >>> T = Aspect( ('ml-temperature', 316901515895475271730171605211001099255) )
    
    >>> t_C = t.convert(celsius_interval,T)     # Inject the aspect 'T'
    >>> t_K = convert(t_C,kelvin)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,kelvin,temperature)
    <BLANKLINE>
    
Temperature difference  
----------------------

The subtle distinction between temperature and temperature difference is manageable with the M-layer. Firstly, a temperature difference expressed in degrees Celsius is not convertible to temperature in degrees Fahrenheit, because that conversion is not registered as legitimate::

    >>> celsius_ratio = Scale( ('ml-si-celsius-ratio', 278784445377172064355281533676474538407) )

    >>> t_diff_C = expr(10,celsius_ratio)
    >>> display(t_diff_C)
    10 degree C
    Expression(10,celsius)
    <BLANKLINE>
    >>> t_diff_C.convert(fahrenheit_interval)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-celsius-ratio', 278784445377172064355281533676474538407)) to Scale(('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767))

On the other hand, degrees Celsius can be converted to kelvin::

    >>> display( t_diff_C.convert(kelvin) )
    10 K
    Expression(10,kelvin)
    <BLANKLINE>
    
It is important to note that these expressions did not define the aspect, which allows the following (probably unintended) conversion to occur::

    >>> display( t_diff_C.convert(kelvin,T) )
    10 K
    Expression(10,kelvin,temperature)
    <BLANKLINE>
    
To avoid such ambiguity, explicit use of aspects is recommended. If an aspect had been specified, the conversion above could have raised an exception:: 

    >>> dT = Aspect( ('ml-temperature-difference', 212368324110263031011700652725345220325) )

    >>> t_diff_C = expr(10,celsius_ratio,dT)
    >>> display(t_diff_C)
    10 degree C
    Expression(10,celsius,temperature-difference)
    <BLANKLINE>
    >>> display( t_diff_C.convert(kelvin,T) ) # Cannot convert to a different aspect
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: [Aspect('ml-temperature-difference', 212368324110263031011700652725345220325), Aspect('ml-temperature', 316901515895475271730171605211001099255)]
    
Scale-aspect pairs
------------------

Pairing scales with aspects provides a convenient way of expressing data. The M-layer class :class:`~scale_aspect.ScaleAspect` encapsulates scale-aspect pairs for this purpose. The following code uses scale-aspect pairs to handle the cases shown above::

    >>> celsius_dT = ScaleAspect( celsius_ratio, dT )
    >>> celsius_T = ScaleAspect( celsius_interval, T )
    >>> fahrenheit_T = ScaleAspect( fahrenheit_interval, T )
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

    >>> t_diff_C.convert(fahrenheit_T)  # The difference in aspect is detected 
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: [Aspect('ml-temperature-difference', 212368324110263031011700652725345220325), Aspect('ml-temperature', 316901515895475271730171605211001099255)]
  
Plane angle
===========
  
Plane angle is interesting because values are often expressed using bounded cyclic, or circular, values. This means that conversion between expressions of plane angle is quite different from other types of scale.

Scales for plane angle
----------------------

Radian is the special name for the SI unit of plane angle (plane angle is a quantity of dimension one in the SI, so the unit one is also allowed). The unit degree may also be used with the SI. Expressions need not place bounds on the value. However, digital systems frequently impose circular or cyclic limits on values.  Either the lower bound is zero and the upper bound corresponds to one full rotation (:math:`2 \pi` radians or :math:`+360` degrees), or the lower bound corresponds to half a full rotation clockwise (:math:`-\pi` radians or :math:`-180` degrees) and the upper bound to half a full rotation counter-clockwise (:math:`+\pi` radians or :math:`+180` degrees). 

The M-layer has a particular scale type for these bounded cyclic scales. So, M-layer scales can be defined for the different cases::

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
    
An explicit cast is require to changing between bounded and unbounded scales because some loss of information may result. This, in turn, means the expression 
needs to specify an aspect. 

    >>> a = expr(-90,degree_bounded_180,plane_angle)
    >>> display( cast(a,radian_ratio) )
    -1.5707963267948966 rad
    Expression(-1.5707963267948966,radian,plane-angle)
    <BLANKLINE> 
  
Spectroscopic data
==================  
There are many different kinds of optical spectroscopy, but often data can be thought of in the same way: as the response of a sample to stimulus at a specific energy (photon energy). The energy of incident photons is typically presented along the abscissa (x-axis) and the response along the ordinate (y-axis).

Energy data may be expressed in different units, such as electronvolts (:math:`\text{eV}`),  nanometres (:math:`\text{nm}`), wavenumber (:math:`\text{cm}^{-1}`) and terahertz (:math:`\text{THz}`). These units would normally be associated with different aspects (energy, length, inverse length, and frequency, respectively). However, the simple relationships between these quantities for photons makes them a convenient choice for spectroscopists (:math:`E = h\, \nu`, :math:`E = h\, c \, \tilde{\nu}`, etc., where :math:`E` is photon energy, :math:`h` is Planck's constant, :math:`c` is the speed of light, :math:`\nu` is frequency, and :math:`\tilde{\nu}` is wavenumber). 

Photon energy
-------------

Abscissa data can be expressed without ambiguity by specifying the aspect as photon energy::

    >>> photon_energy = Aspect( ('ml-photon-energy', 291306321925738991196807372973812640971) )
    >>> energy = Aspect( ('ml-energy', 12139911566084412692636353460656684046) ) 
    
    >>> electronvolt = Scale( ('ml-electronvolt-ratio', 121864523473489992307630707008460819401) )
    >>> terahertz = Scale( ('ml-si-terahertz-ratio', 271382954339420591832277422907953823861) )
    >>> per_centimetre = Scale( ('ml-si-per-centimetre-ratio', 333995508470114516586033303775415043902) )
    >>> nanometre = Scale( ('ml-si-nanometre-ratio', 257091757625055920788370123828667027186) )
    
The data may then be converted safely::

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

The wavelength is inversely related to energy (:math:`\lambda = h\,c / E`), so the M-layer handles this as a cast, rather than a conversion::

    >>> display(x.cast(nanometre)) 
    1239.8419843320025 nm
    Expression(1239.8419843320025,nanometre,photon energy)
    <BLANKLINE>
    
Response data
-------------

Often response data will be a ratio of the same kind of quantity, such as a reflectance (ratio of reflected to incident flux) or transmittance (ratio of transmitted to incident flux). Such ratios are dimensionless ('dimension one') and would be expressed in terms of the SI unit one. It would not be possible to distinguish between them on the basis of unit alone.

This situation is handled in the M-layer by declaring a different aspect for each type of ratio. These can be combined with the unit one in scale-aspect pairs::

    >>> transmittance = ScaleAspect(
    ...     Scale( ('ml-si-one', 200437119122738863945813053269398165973) ),
    ...     Aspect( ('ml-transmittance', 106338157389217634821305827494648287004) )
    ... )
    >>> reflectance = ScaleAspect(
    ...     Scale( ('ml-si-one', 200437119122738863945813053269398165973) ),
    ...     Aspect( ('ml-reflectance', 77619173328682587252206794509402414758) )
    ... )
    >>> x = expr(0.95,transmittance)
    >>> display(x)
    0.95
    Expression(0.95,one,transmittance)
    <BLANKLINE>
    >>> y = expr(0.1,reflectance)
    >>> display(y)
    0.1
    Expression(0.1,one,reflectance)
    <BLANKLINE>
    
These expressions are distinct. Their scales are the same (both one), but the aspects are different::
    
    >>> x.scale == y.scale
    True
    >>> x.aspect == y.aspect 
    False
    >>> x.scale_aspect == y.scale_aspect 
    False
    
Special unit names
==================
The SI defines special names for some units. However, unit names expressed in terms of SI base units remain valid alternatives. This can lead to ambiguity.

A simple example is provided by the special unit names hertz and becquerel used for frequency and (radio) activity, respectively. Regardless of whether measurement data is expressed in hertz or becquerel it can legitimately be converted to :math:`s^{-1}`. However, once in :math:`s^{-1}` it is not clear which of the two special unit names would apply. 

The M-layer can manage this asymmetry. ::

    >>> per_second = Scale( ('ml-si-per-second-ratio', 323506565708733284157918472061580302494) )
    >>> becquerel = Scale( ('ml-si-becquerel-ratio', 327022986202149438703681911339752143822) )
    
    >>> x = expr(96,becquerel)
    >>> display(x)
    96 Bq
    Expression(96,becquerel)
    <BLANKLINE>
    >>> y = convert(x,per_second)
    >>> display( y )
    96 1/s
    Expression(96,per-second)
    <BLANKLINE>

Here, conversion from the special name becquerel to the generic unit per-second is permitted. However, conversion in the opposite sense is not::
   
    >>> convert(y,becquerel)    # The aspect is unspecified
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-per-second-ratio', 323506565708733284157918472061580302494)) to Scale(('ml-si-becquerel-ratio', 327022986202149438703681911339752143822))

A conversion back to becquerel requires the aspect to be identified::

    >>> activity = Aspect( ('ml-activity', 20106649997056189817632954430448298015) )
    >>> display( convert(y,becquerel,activity) ) 
    96 Bq
    Expression(96,becquerel,activity)
    <BLANKLINE>

Similarly, if the aspect is declared initially the following lines show that a round-trip from hertz to per-second and back to hertz is permitted for frequency, while an attempt to go from hertz to becquerel via per-second is blocked::

    >>> frequency = Aspect( ('ml-frequency', 153247472008167864427404739264717558529) )
    >>> hertz = Scale( ('ml-si-hertz-ratio', 307647520921278207356294979342476646905) )
    >>> x = expr(110,hertz,frequency)
    >>> display(x)
    110 Hz
    Expression(110,hertz,frequency)
    <BLANKLINE>    
    >>> y = convert(x,per_second)
    >>> display(y)
    110 1/s
    Expression(110,per-second,frequency)
    <BLANKLINE>
    >>> display( convert(y,hertz) )
    110 Hz
    Expression(110,hertz,frequency)
    <BLANKLINE>
    >>> convert(y,becquerel)    # Illegitimate conversion is detected
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale(('ml-si-per-second-ratio', 323506565708733284157918472061580302494)) to Scale(('ml-si-becquerel-ratio', 327022986202149438703681911339752143822)) for Aspect('ml-frequency', 153247472008167864427404739264717558529)    
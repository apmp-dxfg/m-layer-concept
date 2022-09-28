.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature
===========

Expressions of temperature data provide examples of some of the difficulties that can arise. Temperature is interesting because there are actually two related closely quantities, which share the same units: absolute (thermodynamic) temperature and differences between absolute temperatures (temperature difference). There are familiar scales for expressing temperature, like the degree Celsius and Fahrenheit, but the degree Celsius is also allowed to express temperature difference in the SI.


Absolute temperature
--------------------
First, we set up the environment ::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()

and create objects for scales ::

    >>> celsius_interval = Scale( ('ml_si_celsius_interval', 245795086332095731716589481707012001072) )
    >>> fahrenheit = Scale( ('ml_imp_fahrenheit_interval', 22817745368296240233220712518826840767) )
    >>> kelvin = Scale( ('ml_si_kelvin_ratio', 302952256288207449238881076502466548054) )
    
We can express a temperature and convert between expressions in Fahrenheit and Celsius ::

    >>> t_F = expr(72,fahrenheit)
    >>> display(t_F)
    72 degree F
    Expression(72,degree F)

    >>> t_C = t_F.convert(celsius_interval)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,degree C)

We can also convert to kelvin (this scale type change is a promotion from interval to ratio, which is legitimate) ::

    >>> t_K = t_C.convert(kelvin)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,K)
    
Note, these operations did not involve use of an M-layer aspect yet. However, the M-layer will not allow conversion from kelvin to Celsius, unless the aspect is known to be temperature ::

    >>> t_K.convert(celsius_interval)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_kelvin_ratio', 302952256288207449238881076502466548054] ) to Scale( ['ml_si_celsius_interval', 245795086332095731716589481707012001072] )

This fails because the initial scale (`kelvin`) is a ratio scale and the target scale (`celsius_interval`) is an interval scale. As a general rule, conversion from a ratio scale to an interval scale may impact on the invariant properties of data. In this case, the data expressed in kelvin could be temperature or temperature difference, which is important because different conversion rules apply.

There are several ways to deal with this situation. Given the object ``t_K``, above, we can coerce the expression to accept an aspect, after which a second cast is needed to change the type of scale ::

    >>> T = Aspect( ('ml_thermodynamic_temperature', 227327310217856015944698060802418784871) )

    >>> t_K = t_K.cast(kelvin,T)
    >>> t_C = t_K.cast(celsius_interval,T)  
    >>> display(t_C)
    22.22222222222223 degree C
    Expression(22.22222222222223,degree C,thermodynamic temperature)

Alternatively, the aspect could be specified in the initial expression ::

    >>> t_F = expr(72,fahrenheit,T)
    >>> t_C = t_F.convert(celsius_interval)
    >>> t_K = t_C.convert(kelvin)
    >>> display( t_K.cast(celsius_interval) )
    22.22222222222223 degree C
    Expression(22.22222222222223,degree C,thermodynamic temperature)
    
Once an aspect is specified, it is retained in any related expression obtained by conversion. 

Pairing scales with aspects provides a more complete and safer way of expressing data. So, the M-layer class :class:`~lib.ScaleAspect` is provided for this purpose.

Here, we might have proceeded as follows ::

    >>> fahrenheit_temperature = ScaleAspect(fahrenheit,T)
    >>> celsius_temperature = ScaleAspect(celsius_interval,T)
    >>> kelvin_temperature = ScaleAspect(kelvin,T)   

    >>> t_F = expr(72,fahrenheit_temperature)
    >>> t_C = t_F.convert(celsius_temperature)
    >>> t_K = t_C.convert(kelvin_temperature)
    >>> display( t_K.cast(celsius_temperature) ) 
    22.22222222222223 degree C
    Expression(22.22222222222223,degree C,thermodynamic temperature)

    
Temperature difference  
----------------------

Here, we see that a temperature difference can be expressed in degrees Celsius (without specifying an aspect) and converted to kelvin ::

    >>> celsius_ratio = Scale( ('ml_si_celsius_ratio', 278784445377172064355281533676474538407) )

    >>> td_C = expr(10,celsius_ratio)
    >>> display(td_C)
    10 degree C
    Expression(10,degree C)

    >>> display( td_C.convert(kelvin) )
    10 K
    Expression(10,K)

However, conversion to Fahrenheit is not possible, ::

    >>> td_C.convert(fahrenheit)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_celsius_ratio', 278784445377172064355281533676474538407] ) to Scale( ['ml_imp_fahrenheit_interval', 22817745368296240233220712518826840767] )
    
Nor is it possible to convert to Celsius temperature ::

    >>> td_C.convert(celsius_interval)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_celsius_ratio', 278784445377172064355281533676474538407] ) to Scale( ['ml_si_celsius_interval', 245795086332095731716589481707012001072] )

These restrictions arise because the M-layer has not defined conversion operations between the different scales. Aspect was not used to make the distinction in this case. As shown above, an expression in terms of the kelvin scale (a ratio scale) cannot be converted to an expression in terms of the scale for Celsius temperature (an interval scale), without explicit coercion (casting). 

The representation can be made clearer by including the temperature difference aspect.  ::

    >>> dT = Aspect( ('ml_temperature_difference', 212368324110263031011700652725345220325) )
    >>> celsius_temperature_differenc = ScaleAspect( celsius_ratio, dT )
    >>> kelvin_temperature_differenc = ScaleAspect( kelvin, dT )

allowing the temperature difference to be expressed clearly and converted to kelvin again. ::

    >>> td_C = expr(10,celsius_temperature_differenc)
    >>> display(td_C)
    10 degree C
    Expression(10,degree C,temperature_difference)

    >>> display( td_C.convert(kelvin_temperature_differenc) )
    10 K
    Expression(10,K,temperature_difference)
    
  
Plane angle
===========
  
Plane angle data may be expressed using values that have special numeric properties: they may be bounded cyclic (circular) numbers. For instance, a value of 361 degrees may be represented instead as 1 degree. This means that conversion between expressions of angle may be quite different from other types of scale.

Scales for plane angle
----------------------

Radian is the special name given to the SI unit of plane angle (plane angle is a quantity of dimension one in the SI, so the unit one is also allowed). The degree may also be used with other SI units. Expressions involving plane angle need not place bounds on the value (the SI Brochure does not even consider this possibility). So, the general ratio scales are available ::

    >>> ml_plane_angle = Aspect( ('ml_plane_angle', 95173225557230344956477808929590724690) )

    >>> ml_imp_degree_ratio = Scale( ('ml_imp_degree_ratio', 124567088583703716502057160299542649451) )
    >>> ml_si_radian_ratio = Scale( ('ml_si_radian_ratio', 273301153578020696303516833405033923738) )

We can express and convert data as before ::

    >>> a = expr(90,ml_imp_degree_ratio)
    >>> display(a)
    90 deg
    Expression(90,deg)

    >>> display( a.convert(ml_si_radian_ratio) )
    1.5707963267948966 rad
    Expression(1.5707963267948966,rad)

However, representations frequently impose circular or cyclic limits.  In such cases, either the lower bound is zero and the upper bound corresponds to one full rotation (:math:`2 \pi` radians or :math:`+360` degrees), or the lower bound corresponds to half a full rotation clockwise (:math:`-\pi` radians or :math:`-180` degrees) and the upper bound to half a full rotation counter-clockwise (:math:`+\pi` radians or :math:`+180` degrees). 

The M-layer has a particular scale type for bounded cyclic ranges. So, scales can be defined for different cases::
    
    >>> ml_si_radian_bounded_two_pi = Scale( ('ml_si_radian_bounded_two_pi', 300556212736422769570885306883285535638) )
    >>> ml_si_radian_bounded_pi = Scale( ('ml_si_radian_bounded_pi', 181367268705518406168243034119604185497) )

    >>> ml_imp_degree_bounded_180 = Scale( ('ml_imp_degree_bounded_180', 273805538217618733078298377573965188309) )
    >>> ml_imp_degree_bounded_360 = Scale( ('ml_imp_degree_bounded_360', 125066222841962802760576607996391537405) )
    
An angle can be converted between various bounded scales without need for an aspect ::

    >>> a = expr(-90,ml_imp_degree_bounded_180)
    >>> display(a)
    -90 deg
    Expression(-90,deg)

    >>> display( a.convert(ml_si_radian_bounded_pi) )
    -1.5707963267948966 rad
    Expression(-1.5707963267948966,rad)

    >>> display( a.convert(ml_imp_degree_bounded_360) )
    270.0 deg
    Expression(270.0,deg)

    >>> display( a.convert(ml_si_radian_bounded_two_pi) )
    4.71238898038469 rad
    Expression(4.71238898038469,rad)
    
Conversion to an unbounded scale is possible too,  ::

    >>> b = a.convert(ml_si_radian_ratio) 
    >>> display( b )
    -1.5707963267948966 rad
    Expression(-1.5707963267948966,rad)
    
However, to change from unbounded to a bounded scale a cast is needed, because some loss of information may result :: 

    >>> display( b.cast(ml_imp_degree_bounded_360,ml_plane_angle) ) 
    270.0 deg
    Expression(270.0,deg,plane-angle)
  
Spectroscopic data
==================  
There are different kinds of optical spectroscopy, but in many cases data can be thought of as a response to stimulus at some specific energy (photon energy). The energy is typically presented along the abscissa (x-axis) and the response along the ordinate (y-axis).

However, energy data may be expressed in different units, such as electronvolts (:math:`\text{eV}`),  nanometres (:math:`\text{nm}`), wavenumber (:math:`\text{cm}^{-1}`) and terahertz (:math:`\text{THz}`). These units would normally be associated with quite different quantities (energy, length, inverse length, and frequency, respectively). For photons, the relationships between these quantities makes them a convenient choice for spectroscopists (:math:`E = h\, \nu`, :math:`E = h\, c \, \tilde{\nu}`, etc., where :math:`E` is photon energy, :math:`h` is Planck's constant, :math:`c` is the speed of light, :math:`\nu` is frequency, and :math:`\tilde{\nu}` is wavenumber). 

Photon energy
-------------

Abscissa data can be expressed without ambiguity by specifying photon energy as the aspect and combining this with different scales ::

    >>> photon_energy = Aspect( ('ml_photon_energy', 291306321925738991196807372973812640971) )
    >>> energy = Aspect( ('ml_energy', 12139911566084412692636353460656684046) ) 
    
    >>> electronvolt = Scale( ('ml_electronvolt_ratio', 121864523473489992307630707008460819401) )
    >>> terahertz = Scale( ('ml_si_THz_ratio', 271382954339420591832277422907953823861) )
    >>> per_centimetre = Scale( ('ml_si_cm-1_ratio', 333995508470114516586033303775415043902) )
    >>> nanometre = Scale( ('ml_si_nm_ratio', 257091757625055920788370123828667027186) )
    
When data has been expressed in terms of photon energy, it may then be converted safely::

    >>> x = expr(1,electronvolt,photon_energy)
    >>> display(x)
    1 eV
    Expression(1,eV,photon energy)

    >>> display( x.convert(terahertz) ) 
    241.79892420849183 THz
    Expression(241.79892420849183,THz,photon energy)

    >>> display( x.convert(per_centimetre) )
    8065.543937349211 1/cm
    Expression(8065.543937349211,1/cm,photon energy)

Wavelength units are handled differently, because wavelength is inversely related to energy (:math:`\lambda = h\,c / E`). We handle this change of unit as a cast, rather than a conversion, because the conversion operation is non-linear ::

    >>> display(x.cast(nanometre)) 
    1239.8419843320025 nm
    Expression(1239.8419843320025,nm,photon energy)
    
Response data
-------------

Often response data will be a ratio of some quantity. For instance, reflectance (ratio of reflected to incident flux) or transmittance (ratio of transmitted to incident flux). These  ratios are dimensionless ('dimension one'), so it is not possible to distinguish between them on the basis of units alone.

This situation is handled by ratio quantity types as aspects, which can then be combined with the unit one as scale-aspect pairs::

    >>> transmittance = ScaleAspect(
    ...     Scale( ('ml_si_one', 200437119122738863945813053269398165973) ),
    ...     Aspect( ('ml_transmittance', 106338157389217634821305827494648287004) )
    ... )
    >>> reflectance = ScaleAspect(
    ...     Scale( ('ml_si_one', 200437119122738863945813053269398165973) ),
    ...     Aspect( ('ml_reflectance', 77619173328682587252206794509402414758) )
    ... )
    >>> x = expr(0.95,transmittance)
    >>> display(x)
    0.95
    Expression(0.95,1,transmittance)

    >>> y = expr(0.1,reflectance)
    >>> display(y)
    0.1
    Expression(0.1,1,reflectance)

    
In this form, the expressions are distinct. Their scales may be the same (both are one), but the aspects are different::
    
    >>> x.scale_aspect == y.scale_aspect 
    False
    
Special unit names
==================
The SI defines special names for some units. However, compound unit names, expressed in terms of SI base units, remain valid alternatives. This can lead to ambiguity.

A simple example is provided by the special unit names hertz and becquerel used for frequency and activity, respectively. Regardless of whether measurement data is expressed in hertz or becquerel it can legitimately be converted to :math:`s^{-1}`. However, once expressed in :math:`s^{-1}` it is not clear which of the two special unit names would apply. 

The M-layer can manage this asymmetry. ::

    >>> per_second = Scale( ('ml_si_s-1_ratio', 323506565708733284157918472061580302494) )
    >>> becquerel = Scale( ('ml_si_becquerel_ratio', 327022986202149438703681911339752143822) )
    
    >>> x = expr(96,becquerel)
    >>> display(x)
    96 Bq
    Expression(96,Bq)

    >>> y = convert(x,per_second)
    >>> display( y )
    96 1/s
    Expression(96,1/s)


Conversion from the special name becquerel to the generic unit per-second is permitted. However, conversion in the opposite sense is not::
   
    >>> convert(y,becquerel)    # The aspect is unspecified
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_s-1_ratio', 323506565708733284157918472061580302494] ) to Scale( ['ml_si_becquerel_ratio', 327022986202149438703681911339752143822] )

Conversion back to becquerel requires the aspect to be specified::

    >>> activity = Aspect( ('ml_activity', 20106649997056189817632954430448298015) )
    >>> display( cast(y,becquerel,activity) ) 
    96 Bq
    Expression(96,Bq,activity)

Similarly, if the aspect is declared as frequency initially, a round-trip from hertz to per-second and back to hertz is permitted. However, an attempt to convert from hertz to becquerel via per-second is blocked::

    >>> frequency = Aspect( ('ml_frequency', 153247472008167864427404739264717558529) )
    >>> hertz = Scale( ('ml_si_hertz_ratio', 307647520921278207356294979342476646905) )
    >>> x = expr(110,hertz,frequency)
    >>> display(x)
    110 Hz
    Expression(110,Hz,frequency)

    >>> y = convert(x,per_second)
    >>> display(y)
    110 1/s
    Expression(110,1/s,frequency)

    >>> display( convert(y,hertz) )
    110 Hz
    Expression(110,Hz,frequency)

    >>> convert(y,becquerel)    # Illegitimate conversion is detected
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_s-1_ratio', 323506565708733284157918472061580302494] ) to Scale( ['ml_si_becquerel_ratio', 327022986202149438703681911339752143822] ) for Aspect( ['ml_frequency', 153247472008167864427404739264717558529] )    
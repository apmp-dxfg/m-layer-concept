.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature
===========

Several interesting examples of difficulties with unambiguous expressions of measured data are provided by temperature.


Absolute temperature
--------------------

Firstly, there is the distinction between ratio scales and interval scales. 

M-layer conversion may occur between different scales of the same type without the need to specify the aspect.  For example, conversion is defined between Fahrenheit and degree Celsius without specifying temperature. ::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()
    
    >>> celsius_interval = Scale( ('ml_si_celsius_interval', 245795086332095731716589481707012001072) )
    >>> fahrenheit_interval = Scale( ('ml_imp_fahrenheit_interval', 22817745368296240233220712518826840767) )
    
    >>> t = expr(72,fahrenheit_interval)
    >>> display(t)
    72 degree F
    Expression(72,degree F)
    <BLANKLINE>
    >>> t_C = t.convert(celsius_interval)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,degree C)
    <BLANKLINE>

M-layer conversion may also occur between different scales of different types provided the conversion is to higher level of scale type 
For example, ::

    >>> kelvin = Scale( ('ml_si_kelvin_ratio', 302952256288207449238881076502466548054) )
    >>> t_K = convert(t_C,kelvin)

Information about the aspect can be specified initially, when creating an expression. 
Once specified, conversion operations cannot change the aspect. :: 

    >>> T = Aspect( ("ml_thermodynamic_temperature", 227327310217856015944698060802418784871) )         
    
    >>> t_F = expr(72,fahrenheit_interval,T)     
    >>> t_C = convert(t_F,celsius_interval)     
    >>> t_K = convert(t_C,kelvin)    
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,K,thermodynamic temperature)
    <BLANKLINE>
    
Temperature difference  
----------------------

The distinction between temperature and temperature difference is now more manageable. Firstly, an expression in degrees Celsius may not be converted to degrees Fahrenheit, because the type of scale is different::

    >>> celsius_ratio = Scale( ('ml_si_celsius_ratio', 278784445377172064355281533676474538407) )

    >>> t_diff_C = expr(10,celsius_ratio)
    >>> display(t_diff_C)
    10 degree C
    Expression(10,degree C)
    <BLANKLINE>
    >>> t_diff_C.convert(fahrenheit_interval)
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_celsius_ratio', 278784445377172064355281533676474538407] ) to Scale( ['ml_imp_fahrenheit_interval', 22817745368296240233220712518826840767] )

However, degrees Celsius can be converted to kelvin (the scales are of the same type)::

    >>> display( t_diff_C.convert(kelvin) )
    10 K
    Expression(10,K)
    <BLANKLINE>
    
    
Scale-aspect pairs
------------------

Pairing scales with aspects provides a convenient and safe way of expressing data. So, explicit use of aspects is recommended.  The M-layer class :class:`~lib.ScaleAspect` encapsulates scale-aspect pairs for this purpose. The following code uses scale-aspect pairs to handle the cases shown above::

    >>> dT = dT = Aspect( ('ml_temperature_difference', 212368324110263031011700652725345220325) )
    
    >>> celsius_dT = ScaleAspect( celsius_ratio, dT )
    >>> celsius_T = ScaleAspect( celsius_interval, T )
    >>> fahrenheit_T = ScaleAspect( fahrenheit_interval, T )
    >>> kelvin_T = ScaleAspect( kelvin, T )
    >>> kelvin_dT = ScaleAspect( kelvin, dT )
    
    >>> t = expr(72,fahrenheit_T)
    >>> display(t)
    72 degree F
    Expression(72,degree F,thermodynamic temperature)
    <BLANKLINE>
    >>> t_C = t.convert(celsius_T)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,degree C,thermodynamic temperature)
    <BLANKLINE>

    >>> t_K = convert(t_C,kelvin_T)
    >>> display(t_K)
    295.3722222222222 K
    Expression(295.3722222222222,K,thermodynamic temperature)
    <BLANKLINE>

    >>> t_diff_C = expr(10,celsius_dT)
    >>> t_diff_C.convert(fahrenheit_T)  # The difference in aspect is detected 
    Traceback (most recent call last):
    ...
    RuntimeError: incompatible aspects: Aspect( ['ml_temperature_difference', 212368324110263031011700652725345220325] ) and Aspect( ['ml_thermodynamic_temperature', 227327310217856015944698060802418784871] )
  
Plane angle
===========
  
Plane angle values may be expressed using bounded cyclic, or circular, values. This means that conversion between expressions of angle is quite different from other types of scale.

Scales for plane angle
----------------------

Radian is the special name given to the SI unit of plane angle (plane angle is a quantity of dimension one in the SI, so the unit one is also allowed). The unit degree may also be used with the SI. Expressions involving plane angle need not place bounds on the value. However, digital systems frequently do impose circular or cyclic limits.  In that case, either the lower bound is zero and the upper bound corresponds to one full rotation (:math:`2 \pi` radians or :math:`+360` degrees), or the lower bound corresponds to half a full rotation clockwise (:math:`-\pi` radians or :math:`-180` degrees) and the upper bound to half a full rotation counter-clockwise (:math:`+\pi` radians or :math:`+180` degrees). 

The M-layer uses a particular scale type to represent these bounded cyclic ranges. M-layer scales can be defined for the different cases::

    >>> plane_angle = Aspect( ('ml_plane_angle', 95173225557230344956477808929590724690) )
    
    >>> radian_ratio = Scale( ('ml_si_radian_ratio', 273301153578020696303516833405033923738) )
    >>> radian_bounded_two_pi = Scale( ('ml_si_radian_bounded_two_pi', 300556212736422769570885306883285535638) )
    >>> radian_bounded_pi = Scale( ('ml_si_radian_bounded_pi', 181367268705518406168243034119604185497) )
    
    >>> degree_ratio = Scale( ('ml_imp_degree_ratio', 124567088583703716502057160299542649451) )
    >>> degree_bounded_180 = Scale( ('ml_imp_degree_bounded_180', 273805538217618733078298377573965188309) )
    >>> degree_bounded_360 = Scale( ('ml_imp_degree_bounded_360', 125066222841962802760576607996391537405) )
    
An angle can be converted between bounded scales::

    >>> a = expr(-90,degree_bounded_180)
    >>> display(a)
    -90 deg
    Expression(-90,deg)
    <BLANKLINE>
    >>> display( convert(a,degree_bounded_360) )
    270.0 deg
    Expression(270.0,deg)
    <BLANKLINE>
    
and casting to an unbounded scale is possible too, but the aspect must be given ::

    >>> b = cast(a,radian_ratio,plane_angle)
    >>> display( b )
    -1.5707963267948966 rad
    Expression(-1.5707963267948966,rad,plane-angle)
    <BLANKLINE>
    
An explicit cast is required to change from unbounded to bounded scales, because some loss of information may result :: 

    >>> display( cast(b,degree_bounded_180) )
    -90.0 deg
    Expression(-90.0,deg,plane-angle)
    <BLANKLINE>
  
Spectroscopic data
==================  
There are many different kinds of optical spectroscopy, but often data can be thought of as the response of a sample to stimulus at a specific energy (photon energy). The energy is typically presented along the abscissa (x-axis) and the response along the ordinate (y-axis).

However, energy data may be expressed in different units, such as electronvolts (:math:`\text{eV}`),  nanometres (:math:`\text{nm}`), wavenumber (:math:`\text{cm}^{-1}`) and terahertz (:math:`\text{THz}`). These units would normally be associated with quite different quantities (energy, length, inverse length, and frequency, respectively). However, the relationships between these quantities for photons makes them a convenient choice for spectroscopists (:math:`E = h\, \nu`, :math:`E = h\, c \, \tilde{\nu}`, etc., where :math:`E` is photon energy, :math:`h` is Planck's constant, :math:`c` is the speed of light, :math:`\nu` is frequency, and :math:`\tilde{\nu}` is wavenumber). 

Photon energy
-------------

Abscissa data can be expressed without ambiguity by specifying photon energy as the aspect ::

    >>> photon_energy = Aspect( ('ml_photon_energy', 291306321925738991196807372973812640971) )
    >>> energy = Aspect( ('ml_energy', 12139911566084412692636353460656684046) ) 
    
    >>> electronvolt = Scale( ('ml_electronvolt_ratio', 121864523473489992307630707008460819401) )
    >>> terahertz = Scale( ('ml_si_THz_ratio', 271382954339420591832277422907953823861) )
    >>> per_centimetre = Scale( ('ml_si_cm-1_ratio', 333995508470114516586033303775415043902) )
    >>> nanometre = Scale( ('ml_si_nm_ratio', 257091757625055920788370123828667027186) )
    
The data may then be converted safely::

    >>> x = expr(1,electronvolt,photon_energy)
    >>> display(x)
    1 eV
    Expression(1,eV,photon energy)
    <BLANKLINE>
    >>> display( x.convert(terahertz) ) 
    241.79892420849183 THz
    Expression(241.79892420849183,THz,photon energy)
    <BLANKLINE>
    >>> display( x.convert(per_centimetre) )
    8065.543937349211 1/cm
    Expression(8065.543937349211,1/cm,photon energy)
    <BLANKLINE>

The wavelength is inversely related to energy (:math:`\lambda = h\,c / E`), so the M-layer must handle this as a cast, rather than a conversion::

    >>> display(x.cast(nanometre)) 
    1239.8419843320025 nm
    Expression(1239.8419843320025,nm,photon energy)
    <BLANKLINE>
    
Response data
-------------

Often the response data will be in the form of a ratio of the same kind of quantity, such as a reflectance (ratio of reflected to incident flux) or transmittance (ratio of transmitted to incident flux). Such ratios are dimensionless ('dimension one'), so it would not be possible to distinguish between them on the basis of unit alone.

This situation is handled in the M-layer by declaring the type of ratio as an aspect. These aspects can be combined with the unit one in scale-aspect pairs::

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
    <BLANKLINE>
    >>> y = expr(0.1,reflectance)
    >>> display(y)
    0.1
    Expression(0.1,1,reflectance)
    <BLANKLINE>
    
These expressions are distinct. Their scales are the same (both one), but the aspects are different::
    
    >>> x.scale_aspect == y.scale_aspect 
    False
    
Special unit names
==================
The SI defines special names for some units. However, compound unit names, expressed in terms of SI base units, remain valid alternatives. This can lead to ambiguity.

A simple example is provided by the special unit names hertz and becquerel used for frequency and (radio) activity, respectively. Regardless of whether measurement data is expressed in hertz or becquerel it can legitimately be converted to :math:`s^{-1}`. However, once expressed in :math:`s^{-1}` it is not clear which of the two special unit names would apply. 

The M-layer can manage this asymmetry. ::

    >>> per_second = Scale( ('ml_si_s-1_ratio', 323506565708733284157918472061580302494) )
    >>> becquerel = Scale( ('ml_si_becquerel_ratio', 327022986202149438703681911339752143822) )
    
    >>> x = expr(96,becquerel)
    >>> display(x)
    96 Bq
    Expression(96,Bq)
    <BLANKLINE>
    >>> y = convert(x,per_second)
    >>> display( y )
    96 1/s
    Expression(96,1/s)
    <BLANKLINE>

Here, conversion from the special name becquerel to the generic unit per-second is permitted. However, conversion in the opposite sense is not::
   
    >>> convert(y,becquerel)    # The aspect is unspecified
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_s-1_ratio', 323506565708733284157918472061580302494] ) to Scale( ['ml_si_becquerel_ratio', 327022986202149438703681911339752143822] )

The conversion back to becquerel requires the aspect to be specified::

    >>> activity = Aspect( ('ml_activity', 20106649997056189817632954430448298015) )
    >>> display( cast(y,becquerel,activity) ) 
    96 Bq
    Expression(96,Bq,activity)
    <BLANKLINE>

Similarly, if the aspect is declared as frequency initially, the following lines show that a round-trip from hertz to per-second and back to hertz is permitted, while an attempt to convert from hertz to becquerel via per-second is blocked::

    >>> frequency = Aspect( ('ml_frequency', 153247472008167864427404739264717558529) )
    >>> hertz = Scale( ('ml_si_hertz_ratio', 307647520921278207356294979342476646905) )
    >>> x = expr(110,hertz,frequency)
    >>> display(x)
    110 Hz
    Expression(110,Hz,frequency)
    <BLANKLINE>    
    >>> y = convert(x,per_second)
    >>> display(y)
    110 1/s
    Expression(110,1/s,frequency)
    <BLANKLINE>
    >>> display( convert(y,hertz) )
    110 Hz
    Expression(110,Hz,frequency)
    <BLANKLINE>
    >>> convert(y,becquerel)    # Illegitimate conversion is detected
    Traceback (most recent call last):
    ...
    RuntimeError: no conversion from Scale( ['ml_si_s-1_ratio', 323506565708733284157918472061580302494] ) to Scale( ['ml_si_becquerel_ratio', 327022986202149438703681911339752143822] ) for Aspect( ['ml_frequency', 153247472008167864427404739264717558529] )    
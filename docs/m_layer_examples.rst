.. _examples_m_layer: 

########
Examples
########

.. contents::
   :local:

Temperature
===========

Absolute (thermodynamic) temperature and temperature differences can be expressed in the SI using kelvin or in degrees Celsius. However, unit conversion depends on which quantity is expressed. There are other familiar scales for expressing temperature, like the degree Fahrenheit.


Temperature
-----------
First, we set up an environment to display the example data and we create scale objects to express temperature in degrees Celsius and degrees Fahrenheit  ::

    >>> from m_layer import *
    
    >>> def display(xp):
    ...    print(xp)       # String format
    ...    print(repr(xp)) # Representation format
    ...    print()

    >>> celsius = Scale( ('ml_si_Cel_interval', 245795086332095731716589481707012001072) )
    >>> fahrenheit = Scale( ('ml_imp_fahrenheit_interval', 22817745368296240233220712518826840767) )
    
We can express a temperature and convert between expressions in Fahrenheit and Celsius ::

    >>> t_F = expr(72,fahrenheit)
    >>> display(t_F)
    72 degree F
    Expression(72,degree F)
    
    >>> t_C = t_F.convert(celsius)
    >>> display(t_C)
    22.22222222222222 degree C
    Expression(22.22222222222222,degree C)
    
Conversion to kelvin is possible ::

    >>> kelvin = Scale( ('ml_si_K_ratio', 302952256288207449238881076502466548054) )
    >>> t_K = t_C.convert(kelvin)

However, conversion from kelvin back to degrees Celsius is more complicated, because it depends on whether we are converting a temperature or a temperature difference. Nothing in the data can resolve this ambiguity, so a casting operation is required::

    >>> display( t_K.cast(celsius) )
    22.22222222222223 degree C
    Expression(22.22222222222223,degree C)
    
The M-layer also defines a special kelvin scale to express kelvin temperatures but not temperature differences ::

    >>> kelvin_z = Scale( ('ml_si_K_ratio_z', 275392817634043449043764890579233469585) )

Using this scale, casting to a temperature in degrees Celsius is possible (converting units from kelvin to degrees Celsius still requires casting, because there is a change of scale type). ::

    >>> t_K_z = t_C.convert( kelvin_z ) 
    >>> display( t_K_z.cast(celsius) )
    22.22222222222223 degree C
    Expression(22.22222222222223,degree C)
    
When data are expressed with this scale, casting to a temperature is not allowed ::
    
    >>> celsius_ratio = Scale( ('ml_si_Cel_ratio', 26419982651148365554713345789323816873) )
    >>> t_K_z.cast(celsius_ratio)
    Traceback (most recent call last):
    ...
    RuntimeError: cannot cast K to degree C
        
Temperature difference  
----------------------

A temperature difference can be expressed in degrees Celsius and converted to kelvin ::

    >>> td_C = expr(10,celsius_ratio)
    >>> display(td_C)
    10 degree C
    Expression(10,degree C)

    >>> display( td_C.convert(kelvin) )
    10 K
    Expression(10,K)

However, conversion to Fahrenheit temperature is not possible (a scale for temperature difference in degrees Fahrenheit is required), ::

    >>> td_C.convert(fahrenheit)
    Traceback (most recent call last):
    ...
    RuntimeError: cannot convert degree C to degree F
    
Nor is it possible to convert to Celsius temperature ::

    >>> td_C.convert(celsius)
    Traceback (most recent call last):
    ...
    RuntimeError: cannot convert degree C to degree C

Plane angle
===========
  
Plane angle data may be expressed using values that have special numeric properties: they may be bounded cyclic (circular) numbers. For instance, a value of 361 degrees may be represented instead as 1 degree. This means that conversion between expressions of angle may be quite different from other types of scale.

Scales for plane angle
----------------------

Radian is the special name given to the SI unit of plane angle (plane angle is a quantity of dimension one in the SI, so the unit one is also allowed). The degree may also be used with other SI units. Expressions involving plane angle need not place bounds on the value (the SI Brochure does not even consider this possibility). So, the general ratio scales are available ::

    >>> ml_plane_angle = Aspect( ('ml_plane_angle', 95173225557230344956477808929590724690) )

    >>> ml_imp_degree_ratio = Scale( ('ml_imp_degree_ratio', 124567088583703716502057160299542649451) )
    >>> ml_si_radian_ratio = Scale( ('ml_si_rad_ratio', 273301153578020696303516833405033923738) )

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
    
    >>> ml_si_radian_bounded_two_pi = Scale( ('ml_si_rad_bounded_two_pi', 300556212736422769570885306883285535638) )
    >>> ml_si_radian_bounded_pi = Scale( ('ml_si_rad_bounded_pi', 181367268705518406168243034119604185497) )

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
    Expression(270.0,deg,plane angle)
  
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
    ...     Scale( ('ml_si_one_ratio', 200437119122738863945813053269398165973) ),
    ...     Aspect( ('ml_transmittance', 106338157389217634821305827494648287004) )
    ... )
    >>> reflectance = ScaleAspect(
    ...     Scale( ('ml_si_one_ratio', 200437119122738863945813053269398165973) ),
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
    >>> becquerel = Scale( ('ml_si_Bq_ratio', 327022986202149438703681911339752143822) )
    
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
    RuntimeError: cannot convert 1/s to Bq

Conversion back to becquerel requires the aspect to be specified::

    >>> activity = Aspect( ('ml_activity', 20106649997056189817632954430448298015) )
    >>> display( cast(y,becquerel,activity) ) 
    96 Bq
    Expression(96,Bq,activity)

Similarly, if the aspect is declared as frequency initially, a round-trip from hertz to per-second and back to hertz is permitted. However, an attempt to convert from hertz to becquerel via per-second is blocked::

    >>> frequency = Aspect( ('ml_frequency', 153247472008167864427404739264717558529) )
    >>> hertz = Scale( ('ml_si_Hz_ratio', 307647520921278207356294979342476646905) )
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
    RuntimeError: cannot convert (1/s, frequency) to (Bq, frequency)    
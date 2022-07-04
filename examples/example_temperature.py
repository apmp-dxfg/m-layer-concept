from m_layer import *

def display(xp):
    print(xp)
    print(repr(xp))
    print()

T = Aspect( ('ml-temperature', 316901515895475271730171605211001099255) )
dT = Aspect( ('ml-temperature-difference', 212368324110263031011700652725345220325) )
ITS_90 = Aspect( ('ml-ITS-90', 333567868916523888067500483865254994090) )

kelvin = Scale( ('ml-si-kelvin-ratio', 302952256288207449238881076502466548054) )
celsius_ratio = Scale( ('ml-si-celsius-ratio', 278784445377172064355281533676474538407) )
celsius_interval = Scale( ('ml-si-celsius-interval', 245795086332095731716589481707012001072) )
fahrenheit = Scale( ('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767) )

t = expr(72,fahrenheit)
display(t)

t_C = t.convert(celsius_interval)
display(t_C)

# t_K = t_C.cast(ml_si_kelvin_ratio,ml_temperature)
# t_K = cast(t_C,kelvin)  # unspecified => same aspect
# display(t_K)

t_diff_C = expr(10,celsius_ratio)
display(t_diff_C)
t_diff_C.convert(kelvin,T)
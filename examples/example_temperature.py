from m_layer import *

ml_temperature = ('ml-temperature', 316901515895475271730171605211001099255)

ml_si_kelvin_ratio = ('ml-si-kelvin-ratio', 302952256288207449238881076502466548054)
ml_si_celsius_interval = ('ml-si-celsius-interval', 245795086332095731716589481707012001072)
ml_imp_fahrenheit_interval = ('ml-imp-fahrenheit-interval', 22817745368296240233220712518826840767)

def display(xp):
    print(xp)
    print(repr(xp))
    print()

# t = XP(72,ml_imp_fahrenheit_interval,ml_temperature)
t = XP(72,ml_imp_fahrenheit_interval)
display(t)

t_C = t.convert(ml_si_celsius_interval)
display(t_C)

t_K = t_C.cast(ml_temperature, ml_si_kelvin_ratio)
display(t_K)

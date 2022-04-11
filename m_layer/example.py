from m_layer.aspect_value import *

from m_layer import aspect
from m_layer import si_unit 
from m_layer import imperial_unit 

def display(av):
    print(av)
    print( "{}: {} {}".format( av.aspect(), av.value, av.ref() ) )
    print()

x = AV(aspect.mass,12,si_unit.kg)
display(x)

y = convert(x,imperial_unit.pound)
display(y)

t = AV(aspect.temperature,72,imperial_unit.degree_F)
display(t)

t_C = convert(t,si_unit.deg_C_interval)
display(t_C)
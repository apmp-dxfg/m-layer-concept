from m_layer import *

from m_layer import aspect
from m_layer import si_unit 
from m_layer import imperial_unit 

def display(av):
    print(av)
    print(repr(av))
    print()

t = AV(aspect.temperature,72,imperial_unit.degree_F)
display(t)

t_C = convert(t,si_unit.deg_C_interval)
display(t_C)


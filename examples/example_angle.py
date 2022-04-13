from m_layer import *

from m_layer import aspect
from m_layer import si_unit 
from m_layer import imperial_unit 

def display(av):
    print(av)
    print(repr(av))
    print()

a = AV(aspect.plane_angle,-90,imperial_unit.degree_180)
display(a)

a_360 = convert(a,si_unit.rad_2pi)
display(a_360)

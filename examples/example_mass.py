from m_layer import *

from m_layer import aspect
from m_layer import si_unit 
from m_layer import imperial_unit 

def display(av):
    print(av)
    print(repr(av))
    print()

x = AV(aspect.mass,12,si_unit.kg)
display(x)

y = convert(x,imperial_unit.pound)
display(y)


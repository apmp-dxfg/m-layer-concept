from m_layer import *

def display(av):
    print(av)
    print(repr(av))
    print()

x = AV(aspect.mass,12,si_unit.kg)
display(x)

y = x.convert(imperial_unit.pound)
display(y)


from m_layer import *

ml_plane_angle = ('ml-plane-angle', 95173225557230344956477808929590724690)

# ml_imp_degree_ratio = ('ml-imp-degree-ratio', 124567088583703716502057160299542649451)
# ml_si_radian_ratio = ('ml-si-radian-ratio', 273301153578020696303516833405033923738)
# ml_si_radian_bounded_pi = ('ml-si-radian-bounded-pi', 181367268705518406168243034119604185497)
ml_si_radian_bounded_two_pi = ('ml-si-radian-bounded-two-pi', 300556212736422769570885306883285535638)
# ml_imp_degree_bounded_360 = ('ml-imp-degree-bounded-360', 125066222841962802760576607996391537405)
ml_imp_degree_bounded_180 = ('ml-imp-degree-bounded-180', 273805538217618733078298377573965188309)

def display(av):
    print(av)
    print(repr(av))
    print()

a = AV(ml_plane_angle,-90,ml_imp_degree_bounded_180)
display(a)

a_360 = a.convert(ml_si_radian_bounded_two_pi)
display(a_360)


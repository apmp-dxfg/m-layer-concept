from m_layer import *

def display(av):
    print(av)
    print(repr(av))
    print()

ml_mass = ('ml-mass', 321881801928222308627062904049725548287)

ml_si_kilogram_ratio = ('ml-si-kilogram-ratio', 12782167041499057092439851237297548539)
ml_imp_pound_ratio = ('ml-imp-pound-ratio', 188380796861507506602975683857494523991)

x = AV(ml_mass,12,ml_si_kilogram_ratio)
display(x)

y = x.convert(ml_imp_pound_ratio)
display(y)


from m_layer import *

def display(xp):
    print(xp)
    print(repr(xp))
    print()

ml_mass = Aspect( ('ml-mass', 321881801928222308627062904049725548287) )

ml_si_kilogram_ratio = Scale( ('ml-si-kilogram-ratio', 12782167041499057092439851237297548539) )
ml_imp_pound_ratio = Scale( ('ml-imp-pound-ratio', 188380796861507506602975683857494523991) )

# x = XP(12,ml_si_kilogram_ratio,ml_mass)
x = expr(12,ml_si_kilogram_ratio)
display(x)

y = x.convert(ml_imp_pound_ratio)
display(y)


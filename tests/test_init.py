import unittest

from m_layer import * 

ml_mass = ('ml-mass', 321881801928222308627062904049725548287)

ml_si_kilogram_ratio = ('ml-si-kilogram-ratio', 12782167041499057092439851237297548539)
ml_imp_pound_ratio = ('ml-imp-pound-ratio', 188380796861507506602975683857494523991)

#----------------------------------------------------------------------------
class TestInit(unittest.TestCase):

    def test(self):
        # construction
        x = XP(ml_mass,12,ml_si_kilogram_ratio)
            
#============================================================================
if __name__ == '__main__':
    unittest.main()
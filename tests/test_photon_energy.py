import unittest

#-----------------------------------------------------
from m_layer import * 

ml_photon_energy = Aspect( ('ml-photon-energy', 291306321925738991196807372973812640971) )

ml_si_joule_ratio = Scale( ('ml-si-joule-ratio', 165050666678496469850612022016789737781) )
ml_electronvolt_ratio = Scale( ('ml-electronvolt-ratio', 121864523473489992307630707008460819401) )
ml_si_terahertz_ratio = Scale( ('ml-si-terahertz-ratio', 271382954339420591832277422907953823861) )
ml_si_per_centimetre_ratio = Scale( ('ml-si-per-centimetre-ratio', 333995508470114516586033303775415043902) )
ml_si_nanometre_ratio = Scale( ('ml-si-nanometre-ratio', 257091757625055920788370123828667027186) )


#----------------------------------------------------------------------------
class TestPhotonEnergy(unittest.TestCase):

    def test_conversions(self):
        # Test values from Table "Numerical Energy Conversion Factors"
        # in "Handbook of High-Resolution Spectroscopy" Vol. 1 Chapter 5,
        # M. Quack, and F. Merkt, Eds. Wiley Chichester, 2011. 
        # 
        x = expr(1,ml_electronvolt_ratio,ml_photon_energy)
        
        t = value( x.convert(ml_si_terahertz_ratio) )
        self.assertAlmostEqual(t,2.417989E2,4)
  
        t = value( x.convert(ml_si_per_centimetre_ratio) )
        self.assertAlmostEqual(t,8065.545,2)
  
        t = value( x.cast(ml_si_nanometre_ratio) )
        self.assertAlmostEqual(t,1239.841,2)

#============================================================================
if __name__ == '__main__':
    unittest.main()
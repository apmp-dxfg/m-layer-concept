import unittest

from m_layer import * 

from m_layer import aspect
from m_layer import si_unit 

#----------------------------------------------------------------------------
class TestInit(unittest.TestCase):

    def test(self):
        # construction
        x = AV(aspect.mass,12,si_unit.kg)
            
#============================================================================
if __name__ == '__main__':
    unittest.main()
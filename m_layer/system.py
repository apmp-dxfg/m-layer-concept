"""
A unit system identifies a set of base quantities and corresponding 
base units (M-layer references).  
"""
from collections import namedtuple 

from m_layer.context import default_context as cxt

# ---------------------------------------------------------------------------
class System(object):

    __slots__ = (
        '_uid',
        '_name',
        '_basis'
    )

    def __init__(self,uid):
    
        self._uid = uid        
        self._name = cxt.system_reg[uid]['name']
        
        # The basis is a sequence of M-layer reference uids
        basis = [ tuple(s_i) for s_i in cxt.system_reg[uid]['basis'] ] 
        names = [ cxt.reference_reg[ uid_i ]['locale']['default']['symbol'] 
            for uid_i in basis
        ]
        # A namedtuple will keep the order of base units and allow 
        # the reference uids to be indexed or accessed by attribute  
        # using the reference symbol
        self._basis = namedtuple(self._name,names)._make(basis)
                    
    @property
    def uid(self):
        return self._uid
        
    @property 
    def name(self):
        return self._name 
        
    @property 
    def basis(self):
        return self._basis 
        
    def __repr__(self):
        return "System( {!s} )".format(self.uid)
   
    def __str__(self):
        return "{}".format(self.name)
   
    def __eq__(self,other):
        return (
            isinstance(other,System)
        and
            self.uid == other.uid
        )
        
# ===========================================================================
if __name__ == '__main__':

    si = System( ('si-system', 88156805987886421108624908988601219537) )
    print(si.basis.kg)
    print(si.basis[0:3])
   


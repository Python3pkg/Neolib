""":mod:`Inventory` -- Provides an interface for a Neopets inventory

.. module:: Inventory
   :synopsis: Provides an interface for a Neopets inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

class Inventory(object):
    """Represents a Neopets inventory
    
    This class is designed to be sub-classed by other
    classes that represent a Neopets inventory. Such
    examples include user inventory, safety deposit
    box, and shop inventory. The main purpose of this
    class is to provide a common interface for all
    inventories.
    """
    
    def __getitem__(self, key):
        return self.items[key]
        
    def __setitem__(self, key, value):
        self.items[key] = value
        
    def __delitem__(self, key):
        self.items.pop(key)
        
    def __contains__(self, key):
        if key in self.items:
            return True
        else:
            return False
            
    def __iter__(self):
        for item in self.items:
            yield self.items[item]
            
    def __len__(self):
        return len(self.items)
            
    def empty(self):
        return bool(len(self.items))


class Inventory(object):
    # Defines whether the inventory is empty or not
    empty = False
            
    # The rest of these methods simply allow this class and child classes to be treated as a dictionary 
    
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
        return self.empty
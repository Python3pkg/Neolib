from neolib.exceptions import invalidUser
from neolib.inventory.SDBInventory import SDBInventory
import logging

class SDB:
    
    usr = None
    inventory = None
    forms = None
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        
    def load(self):
        self.inventory = SDBInventory(self.usr)
        self.forms = self.inventory.forms
        
    def update(self):
        for x in range(1, self.inventory.pages + 1):
            if self._hasPageChanged(x):
                form = self._updateForm(x)
                form.usePin = True
                pg = form.submit()
                
                # Success redirects to SDB page
                if "Your Safety Deposit Box" in pg.content:
                    return True
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if SDB inventory was updated.", {'pg': pg})
                    return False
        
    def _itemsOnPage(self, pg):
        ret = []
        for item in self.inventory:
            if item.pg == pg:
                ret.append(item)
        return ret
        
    def _hasPageChanged(self, pg):
        for item in self._itemsOnPage(pg):
            if item.remove != 0:
                return True
        
        return False
        
    def _updateForm(self, pg):
        form = self.forms[pg]
        for item in self._itemsOnPage(pg):
            form['back_to_inv[' + item.id + ']'] = int(item.remove)
            
        return form

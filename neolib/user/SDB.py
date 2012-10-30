""":mod:`SDB` -- Provides an interface for accessing a user's safety deposit box

.. module:: SDB
   :synopsis: Provides an interface for accessing a user's safety deposit box
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidUser
from neolib.inventory.SDBInventory import SDBInventory
import logging

class SDB:
    
    """Provides an interface for accessing a user's safety deposit box
    
    Provides functionality for loading and updating a user's safety
    deposit box. Automatically detects the number of pages in the
    SDB, loads each page and combines all items into one dictionary.
    
    
    Attributes
       usr (User) -- User that owns the SDB
       inventory (dict[Item]) -- SDB inventory
       forms (list[HTTPForm]) -- List of all HTTP forms on each page
        
    Example
       >>> usr.sdb.load()
       >>> user.sdb.inventory['someitem'].remove = 1
       >>> user.sdb.update()
       True
    """
    
    usr = None
    inventory = None
    forms = None
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        
    def load(self):
        """ Loads the user's SDB inventory
           
        Raises
           parseException
        """
        self.inventory = SDBInventory(self.usr)
        self.forms = self.inventory.forms
        
    def update(self):
        """ Upates the user's SDB inventory
        
        Loops through all items on a page and checks for an item
        that has changed. A changed item is identified as the remove
        attribute being set to anything greater than 0. It will then
        update each page accordingly with the changed items.
           
        Returns
           bool - True if successful, False otherwise
        """
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

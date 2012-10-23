""":mod:`MainShopInventory` -- Provides a common interface for manipulating Neopets items

.. module:: MainShopInventory
   :synopsis: Provides a common interface for manipulating Neopets items
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import parseException
import logging

class Item:
    
    """Represents a main shop inventory
    
    Sub-classes the Inventory class to provide an interface for a main shop.
    Automatically 
    populates itself with the inventory items upon initialization.
       
    Initialization
       MainShopInventory(usr, shopID)
       
       Loads the main shop inventory
       
       Parameters
          usr (User) -- User to load the shop with
          shopID (str) -- The main shop ID
          
       Raises
          parseException
        
    Example
       >>> shop = MainShop(usr, "1")
       >>> for item in shop.inventory:
       ...     print item.name
       Green Apple
       ...
    """
    
    usr = None
    
    id = None
    name = None
    img = None
    desc = None
    price = None
    type = None
    weight = None
    rarity = None
    estVal = None
    location = None
    stock = None
    
    pg = None
    remove = 0
    owner = None
    
    SHOP = "stockshop"
    SDB = "safetydeposit"
    GALLERY = "stockgallery"
    TRASH = "drop"
    DONATE = "donate"
    
    _messages = {"stockshop": "You have added",
                "safetydeposit": "You have added",
                "stockgallery": "You have added",
                "drop": "page should close automatically",
                "donate": "page should close automatically"}
    
    def __init__(self, itemName):
        self.name = itemName
        
    def populate(self, usr = None, itemID = None):
        if not self.id and not itemID:
            return False
            
        if not self.usr and not user:
            return False
        
        # Object's ID is used by default over any provided ID        
        if self.id: itemID = self.id
            
        # Same with the user
        if self.usr: usr = self.usr
        
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(itemID), vars = {'Referer': 'http://www.neopets.com/objects.phtml?type=inventory'})
        
        # Verify valid ID
        if "not in your inventory" in pg.content:
            logging.getLogger("neolib.item").exception("Invalid ID given, could not populate. ID: " + itemID)
            return False
        
        try:
            self.img = pg.table.img['src']
            self.name = pg.table.find_all("td")[1].text.split(" : ")[1].replace("Owner", "")
            self.desc = pg.find_all("div", align="center")[1].i.text
            
            stats = pg.table.next_sibling.table.find_all("td")
            
            self.type = stats[1].text
            self.weight = stats[3].text
            self.rarity = stats[5].text
            self.estVal = stats[7].text
        except Exception:
            logging.getLogger("neolib.item").exception("Failed to parse item details.", {'pg': pg})
            raise parseException
        
        return True
        
    def sendTo(self, loc, usr=None):
        if not loc in self._messages:
            return False
        if not self.usr and not usr:
            return False
        if self.usr: usr = self.usr
        
        # Request the item page first to look human
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(self.id))
        
        form = pg.getForm(usr, name="item_form")
        form['action'] = loc
        
        pg = form.submit()
        return self._messages[loc] in pg.content
        
    def __repr__(self):
        return "<item \"" + self.name + "\">"

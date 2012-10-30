""":mod:`MainShopInventory` -- Provides a common interface for manipulating Neopets items

.. module:: MainShopInventory
   :synopsis: Provides a common interface for manipulating Neopets items
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import parseException
import logging

class Item:
    
    """Provides a common interface for manipulating Neopets items
    
    Contains attributes that are common among most Neopets items and has
    functionality for grabbing item information and doing simple inventory
    movement tasks. 
    
    Attributes
       usr (User) -- User associated with this item
       id (str) -- Item id
       name (str) -- Item name
       img (str) -- Item image remote URL
       desc (str) -- Item description
       price (int/str) -- Item price in NPs
       type (str) -- Item type
       weight (str) -- Item weight
       rarity (str) -- Item rarity level
       estVal (str) -- Item's estimated value according to Neopets
       location (str) -- Item location
       stock (str) -- Item stock if there's more than one in an inventory
       pg (str) -- Page item is on if multiple pages exist in an inventory
       remove (int) -- Indicates how many of this item to remove
       owner (str) -- Item owner's username
    
    Initialization
       Item(itemName)
       
       Initializes the class with the given item name
       
       Parameters
          itemName (str) -- The item name
        
    Example
       >>> itm = Item("Green Apple")
       >>> print itm.name
       'Green Apple'
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
        """ Attempts to populate an item's information with it's ID, returns result
        
        Note that the item id must already be set or otherwise supplied and that the item
        must exist in the associated user's inventory. 
           
        Parameters:
           usr (User) -- User who has the item
           itemID (str) -- The item's object ID
           
        Returns
           bool - True if successful, false otherwise
           
        Raises
           parseException
        """
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
        """ Transfer's an item from user's inventory to another inventory, returns result
           
        Parameters:
           loc (str) -- Location to send the item to (see Item.SHOP, Item.SDB, etc.)
           usr (User) -- User who has the item
           
        Returns
           bool - True if successful, false otherwise
        """
        if not loc in self._messages:
            return False
        if not self.usr and not usr:
            return False
        if self.usr: usr = self.usr
        
        # Request the item page first to look human
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(self.id))
        
        form = pg.form(name="item_form")
        form['action'] = loc
        
        pg = form.submit()
        return self._messages[loc] in pg.content
        
    def __repr__(self):
        return "<item \"" + self.name + "\">"

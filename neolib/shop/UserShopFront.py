""":mod:`UserShopFront` -- Provides an interface for accessing a user shop front

.. module:: UserShopFront
   :synopsis: Provides an interface for accessing a user shop front
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidShop
from neolib.exceptions import parseException
from neolib.inventory.UserShopFrontInventory import UserShopFrontInventory
from neolib.item.Item import Item
import logging

class UserShopFront:
    
    """Provides an interface for accessing a user shop front
    
    Provides functionality for loading a user's shop front end including
    the major details like name and welcome message, and the current
    shop inventory.
    
    Attributes
       usr (User) -- User that owns the shop
       owner (str) -- Shop Owner
       name (str) -- Shop name
       desc (str) -- Shop Description
       welcomeMsg(str) -- Shop welcome message
       objID (str) -- Item ID in shop
       price (str) -- Price of item in the shop
       inventory (dict[UserShopFrontItem]) -- Shop inventory
        
    Example
       >>> shop = UserShopFront(usr, "someowner")
       >>> shop.load()
       >>> shop.inventory['someitem'].buy()
       True
    """
    
    usr = None
    
    owner = ""
    name = ""
    desc = ""
    welcomeMsg = ""
    objID = ""
    price = ""
    
    inventory = None
    
    def __init__(self, usr, owner, objID = "", price = ""):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        self.owner = owner
        self.objID = objID
        self.price = price
        
    def load(self):
        """ Loads the shop details and current inventory
           
        Raises
           parseException
        """
        pg = self.usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + self.owner)
        
        # Checks for valid shop
        if "doesn't have a shop" in pg.content:
            raise invalidShop
        elif "not a valid shop" in pg.content:
            raise invalidShop
        elif "no items for sale" in pg.content:
            return
            
        try:
            panel = pg.find(text = " (owned by ").parent
            
            self.name = panel.b.text
            self.desc = panel.p.text
            self.welcomeMsg = panel.img.text
        except Exception:
            logging.getLogger("neolib.shop").exception("Unable to parse shop front content.", {'pg': pg})
            raise parseException
        
        self.inventory = UserShopFrontInventory(self.usr, self.owner, self.objID, self.price, pg)

""":mod:`MainShop` -- Provides an interface for loading a main shop

.. module:: MainShop
   :synopsis: Provides an interface for loading a main shop
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.inventory.MainShopInventory import MainShopInventory

class MainShop:
    
    """Provides an interface for loading a main shop
    
    Attributes
       usr (User) -- Associated user
       id (str) -- Shop ID
       name (str) -- Shop name
       
    Initialization
       MainShop(usr, shopID)
       
       Initializes the class with the user and shop ID
       a new quest and load the quest details.
       
       Parameters
          usr (User) -- User to use when loading the inventory and buying items
          shopID (str) -- Shop ID
        
    Example
       >>> ms = MainShop(usr, "1")
       >>> for item in ms.inventory:
       ...     print item.name
       Lupe Soup
       Red Bitten Apple
       ...
    """
    
    usr = None
    id = None
    name = None
    
    inventory = None
    
    def __init__(self, usr, shopID):
        self.usr = usr
        self.id = shopID
        
    def load(self):
        """ Loads the shop name and inventory
        """
        pg = self.usr.getPage("http://www.neopets.com/objects.phtml?type=shop&obj_type=" + self.id)
        
        self.name = pg.find("td", "contentModuleHeader").text.strip()
        self.inventory = MainShopInventory(self.usr, self.id)

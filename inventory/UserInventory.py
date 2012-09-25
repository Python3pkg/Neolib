""":mod:`UserInventory` -- Contains the UserInventory class

.. module:: UserInventory
   :synopsis: Contains the UserInventory class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import parseException
from neolib.exceptions import invalidUser
from neolib.inventory.Inventory import Inventory
from neolib.item.Item import Item
import logging

class UserInventory(Inventory):
     
     """Represents a user's inventory
    
    Sub-classes the Inventory class to provide an interface for a user's
    inventory. Will automatically populate itself with all items
    in a user's inventory upon initialization.
       
    Initialization
       UserInventory(usr)
       
       Loads a user's inventory
       
       Queries the user's inventory, parses each item, and adds 
       each item to the inventory. Note this class should not be 
       used directly, but rather usr.inventory should be used to 
       access a user's inventory.
       
       Parameters
          usr (User) - The user to load the inventory for
          
       Raises
          invalidUser
          parseException
        
    Example
       >>> usr.loadInventory
       >>> for item in usr.inventory:
       ...     print item.name
       Blue Kougra Plushie
       Lu Codestone
       ...
    """
     
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.items = {}
        pg = usr.getPage("http://www.neopets.com/objects.phtml?type=inventory")
        
        # Indicates an empty inventory
        if pg.content.find("You aren't carrying anything") != -1:
            return
        
        try:
            for row in pg.find_all("td", "contentModuleContent")[1].table.find_all("tr"):
                for item in row.find_all("td"):
                    name = item.text
                    
                    # Some item names contain extra information encapsulated in paranthesis
                    if name.find("(") != -1:
                        name = name.split("(")[0]
                    
                    tmpItem = Item(name)
                    tmpItem.id = item.a['onclick'].split("(")[1].replace(");", "")
                    tmpItem.img = item.img['src']
                    tmpItem.desc = item.img['alt']
                    tmpItem.usr = usr
                    
                    self.items[name] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user inventory.")
            logging.getLogger("neolib.html").info("Unable to parse user inventory.", {'pg': pg})
            raise parseException

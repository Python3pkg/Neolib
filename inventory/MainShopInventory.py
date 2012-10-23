""":mod:`MainShopInventory` -- Provides an interface for a main shop inventory

.. module:: MainShopInventory
   :synopsis: Provides an interface for a main shop inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.inventory.Inventory import Inventory
from neolib.item.MainShopItem import MainShopItem
import re
import logging

class MainShopInventory(Inventory):
    
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

    def __init__(self, usr, shopID):
        if not usr:
            raise invalidUser
            
        self.items = {}
        self._loadItems(usr, shopID)
        
    def _loadItems(self, usr, shopID):
        pg = usr.getPage("http://www.neopets.com/objects.phtml?type=shop&obj_type=" + shopID)
        
        try:
            for row in pg.find_all("td", "contentModuleContent")[1].find_all("tr"):
                for item in row.find_all("td"):
                    tmpItem = MainShopItem(item.b.text)
                    
                    tmpItem.id, tmpItem.stockid, tmpItem.brr = re.findall("j_info_id=(.*?)&stock_id=(.*?)&brr=(.*?)'", item.a['onclick'])[0]
                    tmpItem.stock = item.text.split(" in stock")[0].replace(tmpItem.name, "")
                    tmpItem.price = item.text.split("Cost: ")[1].replace(" NP", "")
                    tmpItem.usr = usr
                    
                    self.items[tmpItem.name] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Failed to parse main shop inventory", {'pg': pg})
            raise parseException

""":mod:`UserShopFrontInventory` -- Provides an interface for user shop front inventory

.. module:: UserShopFrontInventory
   :synopsis: Provides an interface for user shop front inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidShop
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.UserShopFrontItem import UserShopFrontItem
from neolib.inventory.Inventory import Inventory
import logging


class UserShopFrontInventory(Inventory):
    
    """Represents a user's shop front inventory
    
    Sub-classes the Inventory class to provide an interface for a user's
    shop front inventory. Will automatically populate itself with all items
    in a user's shop front inventory upon initialization.
       
    Initialization
       UserShopFrontInventor(usr, owner = "", objID = "", price = ""):
       
       Loads a user's shop front inventory
       
       Queries a user's shop front, parses all the items in the shop,
       and adds each item to the inventory. Note this class should not
       be used directly, but rather "UserShopFront" should be used.
       
       Parameters
          usr (User) - The user to load the shop page with
          owner (str) - The owner of the shop to load
          objID (str) - The object ID of an item being sought in the shop
          price (str) - The price of an item being sought in the shop
          
       Raises
          invalidUser
          invalidShop
          parseException
        
    Example
       >>> sh = UserShopFront(usr, "someusername")
       >>> sh.loadInventory()
       >>> for item in sh.inventory:
       ...     print item.name
       Blue Kougra Plushie
       Lu Codestone
       ...
    """
    
    def __init__(self, usr, owner = "", objID = "", price = "", pg = None):
        if not usr:
            raise invalidUser
        
        self.items = {}
        self._loadInventory(usr, owner, objID, price, pg)
    
    def _loadInventory(self, usr, owner, objID = "", price = "", pg = None):
        if objID and not price:
            raise invalidShop
        if not pg:
            if objID:
                pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner + "&buy_obj_info_id=" + objID + "&buy_cost_neopoints=" + price)
            else:     
                pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner)
        
        # Checks for empty or invalid shop
        if "doesn't have a shop" in pg.content:
            raise invalidShop
        elif "not a valid shop" in pg.content:
            raise invalidShop
        elif "has changed price" in pg.content:
            raise invalidShop
        elif "no items for sale" in pg.content:
            return
        
        try:
            # If we were searching for an item, and it's not been bought, parse it first
            if objID and not "Item not found!" in pg.content:
                self._parseMainItem(pg, usr, owner)
                    
                # Required to properly parse the rest of the inventory
                panel = pg.find("td", {'width': '120'}).parent.parent.find_next("table")
            else:
                panel = pg.find("td", {'width': '120'}).parent.parent
                          
            for row in panel.find_all("tr"):
                for item in row.find_all("td"):
                    tmpItem = UserShopFrontItem(item.b.text)
                    
                    tmpItem.owner = owner
                    tmpItem.usr = usr
                    tmpItem.buyURL = item.a['href']
                    tmpItem.desc = item.img['title']
                    tmpItem.img = item.img['src']
                    tmpItem.price = item.text.split("Cost : ")[1]
                    tmpItem.stock = item.text.split(" in stock")[0].replace(tmpItem.name, "")
                        
                    self.items[item.b.text] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user shop front inventory.", {'pg': pg})
            raise parseException
            
    def _parseMainItem(self, pg, usr, owner):
        panel = pg.find("td", {'width': '120'}).parent.parent
        
        item = panel.find_all("tr")[0].find_all("td")[0]
        
        tmpItem = UserShopFrontItem(item.b.text)
        
        tmpItem.owner = owner
        tmpItem.usr = usr
        tmpItem.buyURL = item.a['href']
        tmpItem.desc = item.img['title']
        tmpItem.img = item.img['src']
        tmpItem.price = item.text.split("Cost : ")[1]
        tmpItem.stock = item.text.split(" in stock")[0][-1:]
        
        self.items[item.b.text] = tmpItem

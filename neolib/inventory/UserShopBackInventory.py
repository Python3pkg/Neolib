""":mod:`UserShopBackInventory` -- Provides an interface for user shop inventory

.. module:: UserShopBackInventory
   :synopsis: Provides an interface for user shop inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidShop
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.UserShopBackItem import UserShopBackItem
from neolib.inventory.Inventory import Inventory
import logging


class UserShopBackInventory(Inventory):
    
    """Represents the back end of a user's shop inventory
    
    Sub-classes the Inventory class to provide an interface for the
    back end of a user's personal shop.
    
    Attributes:
       pages (int) - Number of shop stock pages
       
    Initialization
       UserShopBackInventory(usr)
       
       Loads the back end of a user's shop inventory
       
       Queries the user's shop stock page and determines the number
       of pages the shop stock has, then proceeds to query each page,
       parse all the items, and add each item to the inventory. Note
       this class should not be used directly, but rather the 
       "UserShopBack" class should be used.
       
       Parameters
          usr (User) - The user to load the shop inventory for
          
       Raises
          invalidUser
          parseException
        
    Example
       >>> usr.loadShop()
       >>> for item in usr.shop.inventory:
       ...     print item.name
       Blue Kougra Plushie
       Lu Codestone
       ...
    """
    
    pages = 0
    forms = {}
    
    def __init__(self, usr, pg = None):
        if not usr:
            raise invalidUser
        
        self.items = {}
        self._loadInventory(usr, pg)
        
    def _loadInventory(self, usr, pg = None):
        if not pg:
            pg = usr.getPage("http://www.neopets.com/market.phtml?type=your")
        
        self.forms[1] = pg.form(action="process_market.phtml")
        pages = None
        # Checks if multiple pages exist
        if "[1-30]" in pg.content:
            pages = pg.find("a", text = "[1-30]").parent.find_all("a")
            
            # The first link is a "Sort by ID" link, the second one is the first page
            pages.pop(0)
            pages.pop(0)
            
        try:
            self.__loadItems(usr, pg, 1) # Load first page
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user shop back inventory.", {'pg': pg})
            raise parseException
        
        if pages:
            self.pages = len(pages) + 1 # Account for first page
            
            # Start from second page
            i = 2
            for page in pages:
                pg = usr.getPage("http://www.neopets.com/" + page['href'])
                self.forms[i] = pg.form(action="process_market.phtml")
                
                try:
                    self.__loadItems(usr, pg, i)
                except Exception:
                    logging.getLogger("neolib.inventory").exception("Unable to parse user shop back inventory.", {'pg': pg})
                    raise parseException
                i += 1
        else:
            self.pages = 1
            
    def __loadItems(self, usr, pg, pgno):
        form = pg.find(action = "process_market.phtml")
        
        # Finds all item rows, popping the first and last rows which contain unecessary amplifying information
        rows = form.find_all("tr")
        rows.pop(0)
        rows.pop(-1)
        
        for item in rows:
            info = item.find_all("td")
            
            tmpItem = UserShopBackItem(info[0].text)
            
            tmpItem.img = info[1].img['src']
            tmpItem.stock = info[2].text
            tmpItem.type = info[3].text
            tmpItem.price = info[4].input['value']
            tmpItem.oldPrice = tmpItem.price
            tmpItem.pos = int(info[4].input['name'].split("_")[1])
            tmpItem.desc = info[5].text
            tmpItem.id = info[6].find("select")['name'].split("[")[1].replace("]", "")
            
            tmpItem.pg = pgno
            tmpItem.usr = usr
            
            # May be multiple types of one item. I.E Secret Laboratory Map
            if not info[0].text in self.items:
                self.items[info[0].text] = tmpItem
            else:
                # Create a list with all item instances
                self.items[info[0].text] = [self.items[info[0].text], tmpItem]

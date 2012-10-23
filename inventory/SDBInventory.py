""":mod:`SDBInventory` -- Provides an interface for SDB inventory

.. module:: SDBInventory
   :synopsis: Provides an interface for SDB inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.Item import Item
from neolib.inventory.Inventory import Inventory
import logging


class SDBInventory(Inventory):
    
    """Represents a user's safety deposit box inventory
    
    Sub-classes the Inventory class to provide an interface for a user's
    Safety Deposit Box. Will automatically populate itself with all items
    (including those across multiple pages) in a user's Safety Deposit
    Box upon initialization.
    
    Attributes
       pages (int) - The number of pages the SDB has
       
    Initialization
       SDBInventory(usr)
       
       Loads SDB inventory
       
       Queries the user's Safety Deposit Box, determines the number of
       pages in the SDB, and then proceeds to request each page and 
       parse all items from the page and add each item to the inventory.
       Note this class should not be used directly, but rather "SDB"
       should be used to access a user's SDB.
       
       Parameters
          usr (User) - The user to load the SDB for
          
       Raises
          invalidUser
          parseException
        
    Example
       >>> usr.loadSDB()
       >>> for item in usr.SDB.inventory:
       ...     print item.name
       Blue Kougra Plushie
       Lu Codestone
       ...
    """
    
    pages = 0
    forms = {}
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml")
        self.forms[1] = pg.getForm(usr, name="boxform")
        self.items = {}
        
        pages = None
        # Check if multiple pages exist
        if "<option value='30'>" in pg.content:
            pages = pg.find_all("select")[1].find_all("option")
            
            # Knock off the first page
            pages.pop(0)
        else:
            self.pages = 1
            
        try:
            self._loadInventory(usr, pg, 1)
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.", {'pg': pg})
            raise parseException
            
        if pages:
            self.pages = len(pages) + 1 # Account for first page
            
            # Start from the second page
            i = 2
            for page in pages:
                pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml?offset=" + page['value'])
                self.forms[i] = pg.getForm(usr, name="boxform")
                
                # Ensure there's items on the page
                if "End of results reached" in pg.content:
                    continue
                
                try:
                    self._loadInventory(usr, pg, i)
                except Exception:
                    logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.", {'pg': pg})
                    raise parseException
                i += 1
                
    def _loadInventory(self, usr, pg, pgno):
        rows = pg.find("form", action = "process_safetydeposit.phtml?checksub=scan").find_all("tr")
        rows.pop(-1) # Last row contains no item
        
        for item in rows:
            stats = item.find_all("td")
            
            itemName = stats[1].b.text
            
            if itemName.find("(") != -1:
                itemName = itemName.split("(")[0]
                
            tmpItem = Item(itemName)
            
            tmpItem.img = stats[0].img['src']
            tmpItem.desc = stats[2].text
            tmpItem.type = stats[3].text
            tmpItem.stock = stats[4].text
            tmpItem.id = stats[5].input['name'].split("[")[1].replace("]", "")
            
            tmpItem.pg = pgno
            tmpItem.usr = usr
            
            self.items[itemName] = tmpItem
            
            
        

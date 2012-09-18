from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.Item import Item
from neolib.inventory.Inventory import Inventory
import logging


class SDBInventory(Inventory):
    
    pages = 0
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml")
        self.items = {}
        
        pages = None
        # Check if multiple pages exist
        if pg.content.find("<option value='30'>") != -1:
            pages = pg.find_all("select")[1].find_all("option")
            
            # Knock off the first page
            pages.pop(0)
            
        try:
            self._loadInventory(usr, pg, 1)
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.")
            logging.getLogger("neolib.html").info("Unable to parse SDB inventory.", {'pg': pg})
            raise parseException
            
        if pages:
            self.pages = len(pages) + 1 # Account for first page
            
            # Start from the second page
            i = 2
            for page in pages:
                pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml?offset=" + page['value'])
                
                # Ensure there's items on the page
                if pg.content.find("End of results reached") != -1:
                    continue
                
                try:
                    self._loadInventory(usr, pg, i)
                except Exception:
                    logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.")
                    logging.getLogger("neolib.html").info("Unable to parse SDB inventory.", {'pg': pg})
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
            
            
        

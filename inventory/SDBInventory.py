from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.Item import Item
from neolib.inventory.Inventory import Inventory
import logging


class SDBInventory(Inventory):
    
    # The number of pages the BACK inventory has
    pages = 0
    
    def __init__(self, usr):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
            
        # Load the page
        pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml")
            
        # Initialize items dictionary
        self.items = {}
        
        pages = None
        # Check if multiple pages exist
        if pg.content.find("<option value='30'>") != -1:
            # Figure out how many pages
            pages = pg.getParser().find_all("select")[1].find_all("option")
            
            # Knock off the first page
            pages.pop(0)
            
        # Load the first page
        try:
            self._loadItems(usr, pg, 1)
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.")
            logging.getLogger("neolib.html").info("Unable to parse SDB inventory.", {'pg': pg})
            raise parseException
            
        # Load any additional pages
        if pages:
            # Have to account for the first page
            self.pages = len(pages) + 1
            
            # Ensure to start from the second page, since the first was already accounted for
            i = 2
            for page in pages:
                # Load the page
                pg = usr.getPage("http://www.neopets.com/safetydeposit.phtml?offset=" + page['value'])
                
                # Ensure there's items on the page
                if pg.content.find("End of results reached") != -1:
                    continue
                
                try:
                    self._loadItems(usr, pg, i)
                except Exception:
                    logging.getLogger("neolib.inventory").exception("Unable to parse SDB inventory.")
                    logging.getLogger("neolib.html").info("Unable to parse SDB inventory.", {'pg': pg})
                    raise parseException
                i += 1
                
    def _loadItems(self, usr, pg, pgno):
        # Parse all item rows
        rows = pg.getParser().find("form", action = "process_safetydeposit.phtml?checksub=scan").find_all("tr")
        rows.pop(-1)
        
        # Loop through all items
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
            
            
        
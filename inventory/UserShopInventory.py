from neolib.exceptions import invalidShop
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.exceptions import invalidType
from neolib.item.UserShopFrontItem import UserShopFrontItem
from neolib.item.UserShopBackItem import UserShopBackItem
from neolib.inventory.Inventory import Inventory
import logging

class UserShopInventory(Inventory):
    
    FRONT = "FRONT"
    BACK = "BACK"
    
    # The type of inventory, either FRONT or BACK
    type = ""
    
    # The number of pages the BACK inventory has
    pages = 0
    
    def __init__(self, usr, type, owner = "", objID = "", price = ""):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
        
        # Initialize items dictionary
        self.items = {}
        
        # Set the inventory type
        self.type = type
        
        # Determine how to load the inventory. If unable to, throw an exception
        if type == self.FRONT:
            self.loadFront(usr, owner, objID, price)
        elif type == self.BACK:
            self.loadBack(usr)
        else:
            raise invalidType
            
    def loadFront(self, usr, owner, objID = "", price = ""):
        # Check if we're looking for a specific item
        if objID:
            # Ensure we got a price too
            if not price:
                raise invalidShop
                
            pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner + "&buy_obj_info_id=" + objID + "&buy_cost_neopoints=" + price)
        else:     
            pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner)
        
        # Ensure it was a valid shop and not empty
        if pg.content.find("doesn't have a shop") != -1:
            raise invalidShop
        elif pg.content.find("not a valid shop") != -1:
            raise invalidShop
        elif pg.content.find("has changed price") != -1:
            raise invalidShop
        elif pg.content.find("no items for sale") != -1:
            # Set this inventory to empty
            self.empty = True
            return
        
        # Begin parsing the contents
        try:
            # If we were searching for an item, and it's not been bought, parse it first
            if objID and pg.content.find("Item not found!") == -1:
                panel = pg.find(text = " (owned by ").parent
                item = panel.find_all("tr")[0].find_all("td")[0]
                
                # This inventory type stores items in a UserShopFrontItem instance
                tmpItem = UserShopFrontItem(item.b.text)
                
                # Set all item attributes
                tmpItem.owner = owner
                tmpItem.usr = usr
                tmpItem.buyURL = item.a['href']
                tmpItem.desc = item.img['title']
                tmpItem.img = item.img['src']
                tmpItem.price = item.text.split("Cost : ")[1]
                tmpItem.stock = item.text.split(" in stock")[0][-1:]
                    
                # Add the item to the items dictionary
                self.items[item.b.text] = tmpItem
                    
                # Set the next panel to the correct value
                panel = pg.find(text = " (owned by ").parent.find_all("table")[1]
            else:
                panel = pg.find(text = " (owned by ").parent.table
                
            # Loop through all rows of items            
            for row in panel.find_all("tr"):
                # Loop through all items in a row
                for item in row.find_all("td"):
                    # This inventory type stores items in a UserShopFrontItem instance
                    tmpItem = UserShopFrontItem(item.b.text)
                    
                    # Set all item attributes
                    tmpItem.owner = owner
                    tmpItem.usr = usr
                    tmpItem.buyURL = item.a['href']
                    tmpItem.desc = item.img['title']
                    tmpItem.img = item.img['src']
                    tmpItem.price = item.text.split("Cost : ")[1]
                    tmpItem.stock = item.text.split(" in stock")[0][-1:]
                        
                    # Add the item to the items dictionary
                    self.items[item.b.text] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user shop front inventory.")
            logging.getLogger("neolib.html").info("Unable to parse user shop front inventory.", {'pg': pg})
            raise parseException
            
    def loadBack(self, usr):
        # Load the page
        pg = usr.getPage("http://www.neopets.com/market.phtml?type=your")
        
        pages = None
        # Check if multiple pages exist
        if pg.content.find("[1-30]") != -1:
            # Figure out how many pages
            pages = pg.find("a", text = "[1-30]").parent.find_all("a")
            
            # The first link is a "Sort by ID" link, the second one is the first page
            pages.pop(0)
            pages.pop(0)
            
        # Load the first page
        try:
            self._loadBackItems(usr, pg, 1)
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user shop back inventory.")
            logging.getLogger("neolib.html").info("Unable to parse user shop back inventory.", {'pg': pg})
            raise parseException
        
        # Load any additional pages
        if pages:
            # Have to account for the first page
            self.pages = len(pages) + 1
            
            # Ensure to start from the second page, since the first was already accounted for
            i = 2
            for page in pages:
                # Load the page
                pg = usr.getPage("http://www.neopets.com/" + page['href'])
                try:
                    self._loadBackItems(usr, pg, i)
                except Exception:
                    logging.getLogger("neolib.inventory").exception("Unable to parse user shop back inventory.")
                    logging.getLogger("neolib.html").info("Unable to parse user shop back inventory.", {'pg': pg})
                    raise parseException
                i += 1
        else:
            self.pages = 1
                
    def _loadBackItems(self, usr, pg, pgno):
        # Find the items form
        form = pg.find(action = "process_market.phtml")
        
        # Find all item rows, popping the first and last rows which contain unecessary amplifying information
        rows = form.find_all("tr")
        rows.pop(0)
        rows.pop(-1)
        
        # Loop through each item
        for item in rows:
            # Parse all the item information
            info = item.find_all("td")
            
            # This inventory type stores items in a UserShopBackItem instance
            tmpItem = UserShopBackItem(info[0].text)
            
            # Set all the item attributes
            tmpItem.img = info[1].img['src']
            tmpItem.stock = info[2].text
            tmpItem.type = info[3].text
            tmpItem.price = info[4].input['value']
            tmpItem.pos = int(info[4].input['name'].split("_")[1])
            tmpItem.desc = info[5].text
            tmpItem.id = info[6].find("select")['name'].split("[")[1].replace("]", "")
            
            
            tmpItem.pg = pgno
            tmpItem.oldPrice = tmpItem.price
            tmpItem.usr = usr
            
            # May be multiple types of one item. I.E Secret Laboratory Map
            if not info[0].text in self.items:
                self.items[info[0].text] = tmpItem
            else:
                # Create a list with both item instances
                self.items[info[0].text] = [self.items[info[0].text], tmpItem]
        
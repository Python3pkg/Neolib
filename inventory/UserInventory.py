from neolib.exceptions import parseException
from neolib.exceptions import invalidUser
from neolib.inventory.Inventory import Inventory
from neolib.item.Item import Item
import logging

class UserInventory(Inventory):
     
    def __init__(self, usr):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
            
        # Initialize items dictionary
        self.items = {}
        
        # Fetch the user's inventory
        pg = usr.getPage("http://www.neopets.com/objects.phtml?type=inventory")
        
        # Check if the inventory is empty
        if pg.content.find("You aren't carrying anything") != -1:
            # Set this inventory instance to empty
            self.empty = True
            return
        
        try:
            # Loop through all rows of items
            for row in pg.find_all("td", "contentModuleContent")[1].table.find_all("tr"):
                # Loop through all items in a row
                for item in row.find_all("td"):
                    name = item.text
                    
                    # Some item names contain extra information encapsulated in paranthesis
                    if name.find("(") != -1:
                        name = name.split("(")[0]
                    
                    # Set all the item attributes
                    tmpItem = Item(name)
                    tmpItem.id = item.a['onclick'].split("(")[1].replace(");", "")
                    tmpItem.img = item.img['src']
                    tmpItem.desc = item.img['alt']
                    
                    # Set the items user instance
                    tmpItem.usr = usr
                    
                    # Add the item to the items dictionary
                    self.items[name] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user inventory.")
            logging.getLogger("neolib.html").info("Unable to parse user inventory.", {'pg': pg})
            raise parseException
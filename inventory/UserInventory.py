from neolib.http.Page import Page
from neolib.item.Item import Item
from neolib.exceptions import emptyInventory
import logging

class UserInventory():
    items = None
    itemCount = 0
     
    def __init__(self, usr):
        # Fetch the user's inventory
        pg = usr.getPage("http://www.neopets.com/objects.phtml?type=inventory")
        
        # Check if the inventory is empty
        if pg.content.find("You aren't carrying anything") != -1:
            logging.getLogger("neolib.inventory").info("User had an empty inventory.")
            raise emptyInventory
        
        s = pg.getParser()
        self.items = {}
        
        # Loop through all rows of items
        for row in s.find_all("td", "contentModuleContent")[1].table.find_all("tr"):
            # Loop through all items
            for item in row.find_all("td"):
                name = item.br.text.split("(")[0]
                
                tmpItem = Item(name)
                tmpItem.id = item.a['onclick'].split("(")[1].replace(");", "")
                tmpItem.img = item.img['src']
                tmpItem.desc = item.img['alt']
                
                tmpItem.owner = usr
                
                self.items[name.lower()] = tmpItem
        
        # Set the item count
        self.itemCount = len(self.items)

    def hasItem(self, itemName):
        # Search the stored items for the item name and return the result
        return itemName.lower() in self.items
        
    def getItem(self, itemName):
        # Verify the item exists
        if itemName.lower() in self.items:
            # Return the item
            return self.items[itemName.lower()]
        else:
            return False
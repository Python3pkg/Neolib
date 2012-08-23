from neolib.RegLib import RegLib
from neolib.http.Page import Page
from neolib.item.Item import Item
import logging

class UserInventory():
    items = None
    itemCount = 0
    
    def __init__(self, user):
        # Fetch the user's inventory
        pg = user.getPage("http://www.neopets.com/objects.phtml?type=inventory")
        
        # Process the items 
        try:
            mats = RegLib.getMat("inventory", "userInventory", pg.pageContent)
        
            self.items = {}
            self.itemList = []
            
            # Loop through each item and create an Item instance and append it to self.items
            for mat in mats:
                tmpItem = Item(mat[3]) # mat[3] = item name
                tmpItem.id = mat[0]
                tmpItem.img = mat[1]
                tmpItem.desc = mat[2]
            
                # Set the owner of this item as the given user
                tmpItem.owner = user
            
                # Add the item, stored as {'Item name (lowercase)': 'Item object'}
                self.items[mat[3].lower()] = tmpItem
        
        except Exception:
            logging.getLogger("neolib").exception("Could not parse items out of source: " + pg.pageContent)
            return
        
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
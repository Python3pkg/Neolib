from neolib.exceptions import parseException
from neolib.shop.ShopWizard import ShopWizard
import logging

class Item:
    
    # The User instance that owns the item
    usr = None
    
    
    # Item ID
    id = None
    
    # Item name
    name = None
    
    # Item image URL
    img = None
    
    # Item description
    desc = None
    
    # Item price
    price = None
    
    
    # Item type
    type = None
    
    # Item weight
    weight = None
    
    # Item rarity level
    rarity = None
    
    # Item's estimated value
    estVal = None
    
    # Item's location (URL)
    location = None
    
    # Item's stock
    stock = None
    
    
    # The item's page number in an inventory
    pg = None
    
    # Defines how much stock to remove from item in inventory
    remove = 0
    
    # Item's owner (name)
    owner = None
    
    def __init__(self, itemName):
        # Set item name
        self.name = itemName
        
    def populate(self, usr = None, itemID = None):
        # Ensure an ID exists
        if not self.id and not itemID:
            return False
            
        # Verify we have a user to use
        if not self.usr and not user:
            return False
        
        # The object's ID is used by default over any provided ID        
        if self.id: itemID = self.id
            
        # Same with the user
        if self.usr: usr = self.usr
        
        # Fetch the item's information page
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(itemID), vars = {'Referer': 'http://www.neopets.com/objects.phtml?type=inventory'})
        
        # Ensure the ID is valid
        if pg.content.find("not in your inventory") != -1:
            logging.getLogger("neolib.item").exception("Invalid ID given, could not populate. ID: " + itemID)
            return False
        
        try:
            # Pull the data
            p = pg.getParser()
            
            # Set the item's attributes
            self.img = p.table.img['src']
            self.name = p.table.find_all("td")[1].text.split(" : ")[1].replace("Owner", "")
            self.desc = p.find_all("div", align="center")[1].i.text
            
            stats = p.table.next_sibling.table.find_all("td")
            
            self.type = stats[1].text
            self.weight = stats[3].text
            self.rarity = stats[5].text
            self.estVal = stats[7].text
        except Exception:
            logging.getLogger("neolib.item").exception("Failed to parse item details.")
            logging.getLogger("neolib.html").info("Failed to parse item details.", {'pg': pg})
            raise parseException
        
        return True
    
    def getPrice(self, searches, method = "AVERAGE", deduct = 0):
        # Pass the parameters off to the ShopWziard.priceItem() method to obtain a price
        price = ShopWizard.priceItem(self.usr, self.name, searches, method, deduct)
        
        # If False was returned, most likely an UB item, so it should not be given a price greater than 0
        if not price:
            self.price = 0
            return False
        else:
            self.price = price
            return self.price
    
    def putSDB(self, user = None):
        # Verify we have a user to use
        if not self.usr and not user:
            return False
        
        # The object's user is used by default over any given user        
        if self.usr: user = self.usr
        
        # Process the request
        html = self.processAction(user, "safetydeposit")
        
        # Verify it worked
        if html.find("You have added") != -1:
            return True
        else:
            return False
        
    def donate(self, user = None):
        if not self.usr and not user:
            return False
            
        if self.usr: user = self.usr
        
        html = self.processAction(user, "donate")
        
        if html.find("page should close automatically") != -1:
            return True
        else:
            return False
        
    def discard(self, user = None):
        if not self.usr and not user:
            return False
            
        if self.usr: user = self.usr
            
        html = self.processAction(user, "drop")
        
        if html.find("page should close automatically") != -1:
            return True
        else:
            return False
        
    def stock(self, user = None):
        if not self.usr and not user:
            return False
            
        if self.usr: user = self.usr
        
        html = self.processAction(user, "stockshop")
        
        if html.find("You have added") != -1:
            return True
        else:
            return False
        
    def putGallery(self, user = None):
        if not self.usr and not user:
            return False
            
        if self.usr: user = self.usr
            
        html = self.processAction(user, "stockgallery")
        
        if html.find("You have added") != -1:
            return True
        else:
            return False
    
    def removeItem(self, stock):
        # Setting to True will cause the next UserShop.updateShop() call to remove the item
        self.remove = stock
    
    def processAction(self, user, action):
        # Neopets expects a specific referrer when sending this post data
        ref = "http://www.neopets.com/iteminfo.phtml?obj_id=" + str(self.id)
        pg = user.getPage("http://www.neopets.com/useobject.phtml", {'obj_id': str(self.id), 'action': action}, {"Referer": ref})
        return pg.content
        

from neolib.http.Page import Page
from neolib.RegexLib import RegexLib
import logging

class Item:
    
    id = None
    name = None
    img = None
    desc = None
    
    type = None
    weight = None
    rarity = None
    estVal = None
    
    estPrice = None
    
    owner = None
    
    def __init__(self, itemName):
        # Set item name
        self.name = itemName
        
    def populate(self, user = None, itemID = None):
        # Ensure an ID exists
        if not self.id and not itemID:
            return False
            
        # Verify we have a user to use
        if not self.owner and not user:
            return False
        
        # The object's ID is used by default over any provided ID        
        if self.id: itemID = self.id
        
        # Fetch the item's information page
        url = "http://www.neopets.com/iteminfo.phtml?obj_id=" + str(itemID)
        pg = user.getPage(url)
        
        # Pull the data
        try:
            data = RegexLib.getMat("item", "itemData", pg.pageContent)
            
            # Populate the attributes
            self.type = data[0][0]
            self.weight = data[0][1]
            self.rarity = data[0][2]
            self.estVal = data[0][3]
        except Exception:
            logging.getLogger("neolib.item").exception("Error parsing item information from source. Item ID: " + itemID + ". Page Source" + pg.pageContent)
            return False
        
        return True
    
    def putSDB(self, user = None):
        # Verify we have a user to use
        if not self.owner and not user:
            return False
        
        # The object's user is used by default over any given user        
        if self.owner: user = self.owner
        
        # Process the request
        html = self.processAction(user, "safetydeposit")
        
        # Verify it worked
        if html.find("You have added") != -1:
            return True
        else:
            return False
        
    def donate(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
        
        html = self.processAction(user, "donate")
        
        if html.find("page should close automatically") != -1:
            return True
        else:
            return False
        
    def discard(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
            
        html = self.processAction(user, "drop")
        
        if html.find("page should close automatically") != -1:
            return True
        else:
            return False
        
    def stock(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
        
        html = self.processAction(user, "stockshop")
        
        if html.find("You have added") != -1:
            return True
        else:
            return False
        
    def putGallery(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
            
        html = self.processAction(user, "stockgallery")
        
        if html.find("You have added") != -1:
            return True
        else:
            return False
        
    def give(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
            
        # Future usage
        temp = ""
        
    def auction(self, user = None):
        if not self.owner and not user:
            return False
            
        if self.owner: user = self.owner
            
        # Future usage
        temp = ""
    
    def processAction(self, user, action):
        # Neopets expects a specific referrer when sending this post data
        ref = "http://www.neopets.com/iteminfo.phtml?obj_id=" + str(self.id)
        pg = user.getPage("http://www.neopets.com/useobject.phtml", {'obj_id': str(self.id), 'action': action}, {"Referer": ref})
        return pg.pageContent
        

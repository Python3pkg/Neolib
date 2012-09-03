from neolib.http.Page import Page
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
    
    location = None
    price = None
    stock = None
    
    owner = None
    
    def __init__(self, itemName):
        # Set item name
        self.name = itemName
        
    def populate(self, usr = None, itemID = None):
        # Ensure an ID exists
        if not self.id and not itemID:
            return False
            
        # Verify we have a user to use
        if not self.owner and not user:
            return False
        
        # The object's ID is used by default over any provided ID        
        if self.id: itemID = self.id
            
        # Same with the user
        if self.owner: usr = self.owner
        
        # Fetch the item's information page
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(itemID), vars = {'Referer': 'http://www.neopets.com/objects.phtml?type=inventory'})
        
        # Ensure the ID is valid
        if pg.content.find("not in your inventory") != -1:
            logging.getLogger("neolib.item").exception("Invalid ID given, could not populate. ID: " + itemID)
            return False
        
        # Pull the data
        p = pg.getParser()
        
        self.img = p.table.img['src']
        self.name = p.table.find_all("td")[1].text.split(" : ")[1].replace("Owner", "")
        self.desc = p.find_all("div", align="center")[1].i.text
        
        stats = p.table.next_sibling.table.find_all("td")
        
        self.type = stats[1].text
        self.weight = stats[3].text
        self.rarity = stats[5].text
        self.estVal = stats[7].text
        
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
        

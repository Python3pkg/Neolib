from neolib.exceptions import parseException
#from neolib.shop.ShopWizard import ShopWizard
import logging

class Item:
    usr = None
    
    
    id = None
    name = None
    img = None
    desc = None
    price = None
    type = None
    weight = None
    rarity = None
    estVal = None
    location = None
    stock = None
    
    pg = None
    remove = 0
    owner = None
    
    def __init__(self, itemName):
        self.name = itemName
        
    def populate(self, usr = None, itemID = None):
        if not self.id and not itemID:
            return False
            
        if not self.usr and not user:
            return False
        
        # Object's ID is used by default over any provided ID        
        if self.id: itemID = self.id
            
        # Same with the user
        if self.usr: usr = self.usr
        
        pg = usr.getPage("http://www.neopets.com/iteminfo.phtml?obj_id=" + str(itemID), vars = {'Referer': 'http://www.neopets.com/objects.phtml?type=inventory'})
        
        # Verify valid ID
        if "not in your inventory" in pg.content:
            logging.getLogger("neolib.item").exception("Invalid ID given, could not populate. ID: " + itemID)
            return False
        
        try:
            self.img = pg.table.img['src']
            self.name = pg.table.find_all("td")[1].text.split(" : ")[1].replace("Owner", "")
            self.desc = pg.find_all("div", align="center")[1].i.text
            
            stats = pg.table.next_sibling.table.find_all("td")
            
            self.type = stats[1].text
            self.weight = stats[3].text
            self.rarity = stats[5].text
            self.estVal = stats[7].text
        except Exception:
            logging.getLogger("neolib.item").exception("Failed to parse item details.")
            logging.getLogger("neolib.html").info("Failed to parse item details.", {'pg': pg})
            raise parseException
        
        return True
    
    #def getPrice(self, searches, method = "AVERAGE", deduct = 0):
    #    # Pass the parameters off to the ShopWziard.priceItem() method to obtain a price
    #    price = ShopWizard.priceItem(self.usr, self.name, searches, method, deduct)
    #    
    #    # If False was returned, most likely an UB item, so it should not be given a price greater than 0
    #    if not price:
    #        self.price = 0
    #        return False
    #    else:
    #        self.price = price
    #        return self.price
    
    def putSDB(self, user = None):
        if not self.usr and not user:
            return False
        
        # The object's user is used by default over any given user        
        if self.usr: user = self.usr
        
        html = self.processAction(user, "safetydeposit")
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
        self.remove = stock
    
    def processAction(self, user, action):
        # Neopets expects a specific referrer when sending this post data
        ref = "http://www.neopets.com/iteminfo.phtml?obj_id=" + str(self.id)
        pg = user.getPage("http://www.neopets.com/useobject.phtml", {'obj_id': str(self.id), 'action': action}, {"Referer": ref})
        return pg.content
        
    def __repr__(self):
        return "<item \"" + self.name + "\">"

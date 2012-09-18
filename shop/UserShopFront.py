from neolib.exceptions import invalidShop
from neolib.exceptions import parseException
from neolib.inventory.UserShopFrontInventory import UserShopFrontInventory
from neolib.item.Item import Item
import logging

class UserShopFront:
    
    usr = None
    
    owner = ""
    name = ""
    desc = ""
    welcomeMsg = ""
    objID = ""
    price = ""
    
    inventory = None
    
    def __init__(self, usr, owner, objID = "", price = ""):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        self.owner = owner
        self.objID = objID
        self.price = price
        
    def loadInventory(self):
        self.inventory = UserShopFrontInventory(self.usr, self.owner, self.objID, self.price)
        
    def populate(self):
        pg = self.usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + self.owner)
        
        # Checks for valid shop
        if pg.content.find("doesn't have a shop") != -1:
            raise invalidShop
        elif pg.content.find("not a valid shop") != -1:
            raise invalidShop
        elif pg.content.find("no items for sale") != -1:
            self.empty = True
            return
            
        try:
            panel = pg.find(text = " (owned by ").parent
            
            self.name = panel.b.text
            self.desc = panel.p.text
            self.welcomeMsg = panel.img.text
        except Exception:
            logging.getLogger("neolib.shop").exception("Unable to parse shop front content.")
            logging.getLogger("neolib.html").info("Unable to parse shop front content.", {'pg': pg})
            raise parseException

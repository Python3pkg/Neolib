from neolib.exceptions import invalidShop
from neolib.exceptions import parseException
from neolib.inventory.UserShopInventory import UserShopInventory
from neolib.item.Item import Item
import logging

class UserShopFront:
    
    # User accessing the shop
    usr = None
    
    # Shop owner's name
    owner = ""
    
    # Shop name
    name = ""
    
    # Shop description
    desc = ""
    
    # Shop welcome message
    welcomeMsg = ""
    
    # The object ID of the item searched for
    objID = ""
    
    # The price of the item searched for
    price = ""
    
    # Shop inventory
    inventory = None
    
    def __init__(self, usr, owner, objID = "", price = ""):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
        
        # Set usr and owner
        self.usr = usr
        self.owner = owner
        
        # Set optionals
        self.objID = objID
        self.price = price
        
    def loadInventory(self):
        # Create a new instance of UserShopInventory, which loads the inventory on initialization
        self.inventory = UserShopInventory(self.usr, "FRONT", self.owner, self.objID, self.price)
        
    def populate(self):
        # Load the shop page
        pg = self.usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + self.owner)
        
        # Ensure it was a valid shop and not empty
        if pg.content.find("doesn't have a shop") != -1:
            raise invalidShop
        elif pg.content.find("not a valid shop") != -1:
            raise invalidShop
        elif pg.content.find("no items for sale") != -1:
            self.empty = True
            return
            
        # Parse out shop details
        try:
            panel = pg.getParser().find(text = " (owned by ").parent
            
            self.name = panel.b.text
            self.desc = panel.p.text
            self.welcomeMsg = panel.img.text
        except Exception:
            logging.getLogger("neolib.shop").exception("Unable to parse shop front content.")
            logging.getLogger("neolib.html").info("Unable to parse shop front content.", {'pg': pg})
            raise parseException
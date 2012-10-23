from neolib.inventory.MainShopInventory import MainShopInventory

class MainShop:
    usr = None
    id = None
    name = None
    
    inventory = None
    
    def __init__(self, usr, shopID):
        self.usr = usr
        self.id = shopID
        
    def load(self):
        pg = usr.getPage("http://www.neopets.com/objects.phtml?type=shop&obj_type=" + shopID)
        
        self.name = pg.find("td", "contentModuleHeader").text.strip()
        self.inventory = MainShopInventory(self.usr, self.id)

from neolib.item.Item import Item
from neolib.shop.ShopWizard import ShopWizard

class UserShopBackItem(Item):
    
    # The item's numerical position in the inventory
    pos = None
    
    # The item's associated page
    pg = None
    
    # The item's old price
    oldPrice = None
    
    # Defines whether to remove an item from the shop
    remove = False
    
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
            
    def removeFromShop(self):
        # Setting to True will cause the next UserShop.updateShop() call to remove the item
        self.remove = True
        
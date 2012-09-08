from neolib.item.Item import Item
import logging

class UserShopFrontItem(Item):
    
    # The URL to purchase the item
    buyURL = None
    
    def buy(self):
        # Buy the item
        pg = self.usr.getPage("http://www.neopets.com/" + self.buyURL, vars = {'Referer': 'http://www.neopets.com/browseshop.phtml?owner=' + self.owner})
        
        # Ensure it was actually bought
        if pg.header.vars['Location'].find("browseshop.phtml") != -1:
            # A redirect confirms we bought it
            return True
        elif pg.content.find("does not exist in this shop") != -1:
            # Someone else already bought it
            return False
        else:
            logging.getLogger("neolib.item").exception("Unknown message when attempting to buy user shop item.")
            logging.getLogger("neolib.html").info("Unknown message when attempting to buy user shop item.", {'pg': pg})
            return False
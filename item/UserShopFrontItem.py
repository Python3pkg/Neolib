from neolib.item.Item import Item
import logging

class UserShopFrontItem(Item):
    
    buyURL = None
    
    def buy(self):
        # Buy the item
        pg = self.usr.getPage("http://www.neopets.com/" + self.buyURL, vars = {'Referer': 'http://www.neopets.com/browseshop.phtml?owner=' + self.owner})
        
        # If it was successful a redirect to the shop is sent
        if pg.content.find("(owned by") != -1:
                return True
        elif pg.content.find("does not exist in this shop") != -1:
                return False
        else:
            logging.getLogger("neolib.item").exception("Unknown message when attempting to buy user shop item.")
            logging.getLogger("neolib.html").info("Unknown message when attempting to buy user shop item.", {'pg': pg})
            return False

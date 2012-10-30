""":mod:`MainShopInventory` -- Represents an item in a user shop

.. module:: MainShopInventory
   :synopsis: Represents an item in a user shop
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.item.Item import Item
import logging

class UserShopFrontItem(Item):
    
    """Represents an item in a user shop
    
    Contains functionality for buying a user shop item
    
    Attributes
       buURL (str) -- The remote URL used to buy this item
    
    Initialization
       See Item
        
    Example
       >>> itm = UserShopFrontItem("Green Apple")
       >>> itm.usr = usr
       >>> itm.buyURL = someurl
       >>> itm.buy()
       True
    """
    
    buyURL = None
    
    def buy(self):
        """ Attempts to purchase a user shop item, returns result
        
        Uses the associated user and buyURL to attempt to purchase the user shop item. Returns
        whether or not the item was successfully bought. 
           
        Returns
           bool - True if successful, false otherwise
        """
        # Buy the item
        pg = self.usr.getPage("http://www.neopets.com/" + self.buyURL, vars = {'Referer': 'http://www.neopets.com/browseshop.phtml?owner=' + self.owner})
        
        # If it was successful a redirect to the shop is sent
        if "(owned by" in pg.content:
                return True
        elif "does not exist in this shop" in pg.content:
                return False
        else:
            logging.getLogger("neolib.item").exception("Unknown message when attempting to buy user shop item.", {'pg': pg})
            return False

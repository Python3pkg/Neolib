from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.inventory.UserShopInventory import UserShopInventory
import logging

class UserShop:
    
    # User who owns the shop
    usr = None
    
    # Instance of UserShopInventory
    inventory = None
    
    def __init__(self, usr):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
            
        # Set the user    
        self.usr = usr
            
    
    @property
    def till(self):
        # Navigate to the till page
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        
        # Parse and return the till
        try:
            return pg.getParser().find_all(text = "Shop Till")[1].parent.next_sibling.b.text.replace(" NP", "").replace(",", "")
        except Exception:
            logging.getLogger("neolib.shop").exception("Could not grab shop till.")
            logging.getLogger("neolib.html").info("Could not grab shop till.", {'pg': pg})
            raise parseException
            
    def grabTill(self, nps):
        # Ensure a non-zero value
        if not int(nps):
            return False
            
        # Navigate to till page
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        
        # Grab the till
        pg = self.usr.getPage("http://www.neopets.com/process_market.phtml", {'type': 'withdraw', 'amount': str(nps)})
        
        # Ensure it was successful
        if "Location" in pg.header.vars:
            if pg.header.vars['Location'].find("market.phtml?type=till") != -1:
                return True
            else:
                logging.getLogger("neolib.shop").exception("Could not grab shop till.")
                logging.getLogger("neolib.html").info("Could not grab shop till.", {'pg': pg})
                return False
        else:
            logging.getLogger("neolib.shop").exception("Could not grab shop till.")
            logging.getLogger("neolib.html").info("Could not grab shop till.", {'pg': pg})
            return False
    
    def loadInventory(self):
        # Create a new instance of UserShopInventory, which loads the inventory on initialization
        self.inventory = UserShopInventory(self.usr, "BACK")
        
    def updateShop(self):
        # Build the initial post data
        postData = {'type': 'update_prices', 'order_by': 'id', 'view': ''}
        
        # Need to deal with each page individually
        for x in range(1, self.inventory.pages + 1):
            # Check if an any item on this page has changed
            if self._hasPageChanged(x):
                # Add additional post data
                postData.update(self._constructPagePostData(x))
                
                # Update the page
                ref = "http://www.neopets.com/market.phtml?type=your&lim=" + str(x * 30)
                pg = self.usr.getPage("http://www.neopets.com/process_market.phtml", postData, {'Referer': ref})
                logging.getLogger("neolib.html").info("This is it", {'pg': pg})
                # Ensure it was successful
                if "Location" in pg.header.vars:
                    if pg.header.vars['Location'].find("market.phtml") != -1:
                        return True
                    else:
                        logging.getLogger("neolib.shop").exception("Could not verify if prices were updated on user shop.")
                        logging.getLogger("neolib.html").info("Could not verify if prices were updated on user shop.", {'pg': pg})
                        return False
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if prices were updated on user shop.")
                    logging.getLogger("neolib.html").info("Could not verify if prices were updated on user shop.", {'pg': pg})
                    return False
            
    def _itemsOnPage(self, pg):
        ret = []
        # Loop through all items, match against the page number, and return a list with all matches appended to it
        for item in self.inventory:
            
            # Account for multiple item types
            if isinstance(item, list):
                for subItem in item:
                    if subItem.pg == pg:
                        ret.append(subItem)
                continue
            
            if item.pg == pg:
                ret.append(item)
        return ret
        
    def _hasPageChanged(self, pg):
        # Loop through all items and compare price to oldPrice to determine any changes on the page
        for item in self._itemsOnPage(pg):
            
            if item.price != item.oldPrice:
                return True
        
        return False
        
    def _constructPagePostData(self, pg):
        postData = {}
        # Loop through all items on a given page
        for item in self._itemsOnPage(pg):
            # Construct post data for updating the shop page information
            postData["obj_id_" + str(item.pos)] = item.id
            postData['oldcost_' + str(item.pos)] = item.oldPrice
            postData['cost_' + str(item.pos)] = str(item.price)
            postData['back_to_inv[' + item.id + ']'] = int(item.remove)
            
        return postData
from neolib.exceptions import invalidUser
from neolib.inventory.SDBInventory import SDBInventory
import logging

class SDB:
    
    # User who owns the SDB
    usr = None
    
    # Instance of SDBInventory
    inventory = None
    
    def __init__(self, usr):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
            
        # Set the user    
        self.usr = usr
        
    def loadInventory(self):
        # Create a new instance of SDBInventory, which loads the inventory on initialization
        self.inventory = SDBInventory(self.usr)
        
    def updateSDB(self):
        # Build the initial post data
        postData = {'obj_name': '', 'category': '0'}
        
        # Need to deal with each page individually
        for x in range(1, self.inventory.pages + 1):
            # Check if an any item on this page has changed
            if self._hasPageChanged(x):
                # Add additional post data
                postData.update(self._constructPagePostData(x))
                postData['offset'] = str((x -1) * 30)
                
                # Update the page
                ref = "http://www.neopets.com/safetydeposit.phtml?category=0&obj_name=&offset=" + str((x -1) * 30)
                pg = self.usr.getPage("http://www.neopets.com/process_safetydeposit.phtml?checksub=scan", postData, {'Referer': ref}, True)
                
                # Ensure it was successful
                if "Location" in pg.header.vars:
                    if pg.header.vars['Location'].find("safetydeposit.phtml") != -1:
                        return True
                    else:
                        logging.getLogger("neolib.shop").exception("Could not verify if SDB inventory was updated.")
                        logging.getLogger("neolib.html").info("Could not verify if SDB inventory was updated.", {'pg': pg})
                        return False
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if SDB inventory was updated.")
                    logging.getLogger("neolib.html").info("Could not verify if SDB inventory was updated.", {'pg': pg})
                    return False
        
    def _itemsOnPage(self, pg):
        ret = []
        # Loop through all items, match against the page number, and return a list with all matches appended to it
        for item in self.inventory:
            if item.pg == pg:
                ret.append(item)
        return ret
        
    def _hasPageChanged(self, pg):
        # Loop through all items and check if the item has been set to be removed
        for item in self._itemsOnPage(pg):

            if item.remove == True:
                return True
        
        return False
        
    def _constructPagePostData(self, pg):
        postData = {}
        # Loop through all items on a given page
        for item in self._itemsOnPage(pg):
            # Construct post data for updating the shop page information
            postData['back_to_inv[' + item.id + ']'] = int(item.remove)
            
        return postData
from neolib.exceptions import invalidUser
from neolib.inventory.SDBInventory import SDBInventory
import logging

class SDB:
    
    usr = None
    inventory = None
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        
    def load(self):
        self.inventory = SDBInventory(self.usr)
        
    def updateSDB(self):
        postData = {'obj_name': '', 'category': '0'}
        
        for x in range(1, self.inventory.pages + 1):
            if self._hasPageChanged(x):
                postData.update(self._constructPagePostData(x))
                postData['offset'] = str((x -1) * 30)
                
                ref = "http://www.neopets.com/safetydeposit.phtml?category=0&obj_name=&offset=" + str((x -1) * 30)
                pg = self.usr.getPage("http://www.neopets.com/process_safetydeposit.phtml?checksub=scan", postData, {'Referer': ref}, True)
                
                # Success redirects to SDB page
                if "Your Safety Deposit Box" in pg.content:
                    return True
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if SDB inventory was updated.")
                    logging.getLogger("neolib.html").info("Could not verify if SDB inventory was updated.", {'pg': pg})
                    return False
        
    def _itemsOnPage(self, pg):
        ret = []
        for item in self.inventory:
            if item.pg == pg:
                ret.append(item)
        return ret
        
    def _hasPageChanged(self, pg):
        for item in self._itemsOnPage(pg):
            if item.remove == True:
                return True
        
        return False
        
    def _constructPagePostData(self, pg):
        postData = {}
        for item in self._itemsOnPage(pg):
            postData['back_to_inv[' + item.id + ']'] = int(item.remove)
            
        return postData

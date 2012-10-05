from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.inventory.UserShopBackInventory import UserShopBackInventory
import logging

class UserShop:
    
    usr = None
    name = None
    size = None
    
    keeperName = None
    keeperMessage = None
    keeperImg = None
    
    stock = None
    max = None
    
    history = None
    
    inventory = None
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        self.populate()
            
    @property
    def till(self):
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        
        try:
            return pg.find_all(text = "Shop Till")[1].parent.next_sibling.b.text.replace(" NP", "").replace(",", "")
        except Exception:
            logging.getLogger("neolib.shop").exception("Could not grab shop till.")
            logging.getLogger("neolib.html").info("Could not grab shop till.", {'pg': pg})
            raise parseException
            
    def grabTill(self, nps):
        if not int(nps):
            return False
            
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        pg = self.usr.getPage("http://www.neopets.com/process_market.phtml", {'type': 'withdraw', 'amount': str(nps)}, usePin = True)
        
        # If successful redirects to till page
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
        self.inventory = UserShopBackInventory(self.usr)
    
    def populate(self):
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=your")
        
        try:
            self.name = pg.find_all(text = "Shop Till")[1].parent.parent.parent.previous_sibling.previous_sibling.text
            self.size = pg.find_all(text = "Shop Till")[1].parent.parent.parent.previous_sibling.split("(size ")[1].replace(")", "")
            
            panel = pg.find("img", {"name": "keeperimage"}).parent
            
            self.keeperName = panel.b.text.split(" says ")[0]
            self.keeperMessage = panel.b.text.split(" says ")[1]
            self.keeperImg = panel.img['src']
            self.stock = panel.find_all("b")[1].text
            self.max = panel.find_all("b")[2].text
        except Exception:
            logging.getLogger("neolib.shop").exception("Could not parse shop details.")
            logging.getLogger("neolib.html").info("Could not parse shop details.", {'pg': pg})
            raise parseException
            
    def loadSalesHistory(self):
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=sales")\
        
        try:
            rows = pg.find("b", text = "Date").parent.parent.parent.find_all("tr")
            
            # First and last row do not contain entries
            rows.pop(0)
            rows.pop(-1)
            
            self.history = []
            for row in rows:
                parts = row.find_all("td")
                dets = {}
                
                dets['date'] = parts[0].text
                dets['item'] = parts[1].text
                dets['buyer'] = parts[2].text
                dets['price'] = parts[3].text
                
                self.history.append(dets)
                
            # Reverse the list to put it in order by date
            self.history.reverse()
        except Exception:
            logging.getLogger("neolib.shop").exception("Could not parse sales history.")
            logging.getLogger("neolib.html").info("Could not parse sales history.", {'pg': pg})
            raise parseException
            
    def updateShop(self):
        postData = {'type': 'update_prices', 'order_by': 'id', 'view': ''}
        
        for x in range(1, self.inventory.pages + 1):
            if self._hasPageChanged(x):
                postData.update(self._constructPagePostData(x))
                
                ref = "http://www.neopets.com/market.phtml?type=your&lim=" + str(x * 30)
                pg = self.usr.getPage("http://www.neopets.com/process_market.phtml", postData, {'Referer': ref}, True)
                
                # If successful redirects to shop
                if pg.content.find("The Marketplace") != -1:
                    return True
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if prices were updated on user shop.")
                    logging.getLogger("neolib.html").info("Could not verify if prices were updated on user shop.", {'pg': pg})
                    return False
            
    def _itemsOnPage(self, pg):
        ret = []
        for item in self.inventory:
            if isinstance(item, list):
                for subItem in item:
                    if subItem.pg == pg:
                        ret.append(subItem)
                continue
            
            if item.pg == pg:
                ret.append(item)
        return ret
        
    def _hasPageChanged(self, pg):
        for item in self._itemsOnPage(pg):
            if item.price != item.oldPrice:
                return True
                
            if item.remove > 0:
                return True
        
        return False
        
    def _constructPagePostData(self, pg):
        postData = {}
        for item in self._itemsOnPage(pg):
            postData["obj_id_" + str(item.pos)] = item.id
            postData['oldcost_' + str(item.pos)] = item.oldPrice
            postData['cost_' + str(item.pos)] = str(item.price)
            postData['back_to_inv[' + item.id + ']'] = int(item.remove)
            
        return postData

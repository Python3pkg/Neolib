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
    forms = None
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
            
    @property
    def till(self):
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        
        try:
            return pg.find_all(text = "Shop Till")[1].parent.next_sibling.b.text.replace(" NP", "").replace(",", "")
        except Exception:
            logging.getLogger("neolib.shop").exception("Could not grab shop till.", {'pg': pg})
            raise parseException
            
    def grabTill(self, nps):
        if not int(nps):
            return False
            
        pg = self.usr.getPage("http://www.neopets.com/market.phtml?type=till")
        form = pg.getForm(self.usr, action="process_market.phtml")
        
        form['amount'] = str(nps)
        form.usePin = True
        pg = form.submit()
        
        # If successful redirects to till page
        if "You currently have" in pg.content:
            return True
        else:
            logging.getLogger("neolib.shop").exception("Could not grab shop till.", {'pg': pg})
            return False
    
    def load(self):
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
            logging.getLogger("neolib.shop").exception("Could not parse shop details.", {'pg': pg})
            raise parseException
        
        self.inventory = UserShopBackInventory(self.usr, pg)
        self.forms = self.inventory.forms
            
    def loadHistory(self):
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
            logging.getLogger("neolib.shop").exception("Could not parse sales history.", {'pg': pg})
            raise parseException
            
    def update(self):
        for x in range(1, self.inventory.pages + 1):
            if self._hasPageChanged(x):
                form = self._updateForm(x)
                pg = form.submit()
                
                # If successful redirects to shop
                if "The Marketplace" in pg.content:
                    return True
                else:
                    logging.getLogger("neolib.shop").exception("Could not verify if prices were updated on user shop.", {'pg': pg})
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
        
    def _updateForm(self, pg):
        if 'remove_all' in self.forms[pg]: del self.forms[pg]['remove_all']
        for item in self._itemsOnPage(pg):
            self.forms[pg]['cost_' + str(item.pos)] = str(item.price)
            self.forms[pg]['back_to_inv[' + item.id + ']'] = int(item.remove)
        return self.forms[pg]

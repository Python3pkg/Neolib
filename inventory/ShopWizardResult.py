from neolib.exceptions import parseException
from neolib.inventory.Inventory import Inventory
from neolib.shop.UserShopFront import UserShopFront
from neolib.item.Item import Item
import logging

class ShopWizardResult(Inventory):
    
    usr = None
    
    def __init__(self, pg, usr):
        self.usr = usr
        
        try:
            items = pg.find("td", "contentModuleHeaderAlt").parent.parent.find_all("tr")
            items.pop(0)
            
            self.items = []
            for item in items:
                tmpItem = Item(item.find_all("td")[1].text)
                
                tmpItem.owner = item.td.a.text
                tmpItem.location = item.td.a['href']
                tmpItem.stock = item.find_all("td")[2].text
                tmpItem.price = item.find_all("td")[3].text.replace(" NP", "").replace(",", "")
                tmpItem.id = tmpItem.location.split("buy_obj_info_id=")[1].split("&")[0]
                
                self.items.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.shop").exception("Unable to parse shop wizard results.")
            logging.getLogger("neolib.html").info("Unable to parse shop wizard results.", {'pg': pg})
            raise parseException

    def buy(self, index):
        item = self.items[index]
        us = UserShopFront(self.usr, item.owner, item.id, str(item.price))
        us.load()
        
        if not item.name in us.inventory:
            return False
        
        if not us.inventory[item.name].buy():
            return False
                
        return True
        

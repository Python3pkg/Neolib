from neolib.exceptions import invalidShop
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.item.UserShopFrontItem import UserShopFrontItem
from neolib.inventory.Inventory import Inventory
import logging


class UserShopFrontInventory(Inventory):
    
    def __init__(self, usr, owner = "", objID = "", price = ""):
        if not usr:
            raise invalidUser
        
        self.items = {}
        self._loadInventory(usr, owner, objID, price)
    
    def _loadInventory(self, usr, owner, objID = "", price = ""):
        if objID and not price:
            raise invalidShop
                
        if objID:
            pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner + "&buy_obj_info_id=" + objID + "&buy_cost_neopoints=" + price)
        else:     
            pg = usr.getPage("http://www.neopets.com/browseshop.phtml?owner=" + owner)
        
        # Checks for empty or invalid shop
        if pg.content.find("doesn't have a shop") != -1:
            raise invalidShop
        elif pg.content.find("not a valid shop") != -1:
            raise invalidShop
        elif pg.content.find("has changed price") != -1:
            raise invalidShop
        elif pg.content.find("no items for sale") != -1:
            return
        
        try:
            # If we were searching for an item, and it's not been bought, parse it first
            if objID and pg.content.find("Item not found!") == -1:
                self._parseMainItem(pg, usr, owner)
                    
                # Required to properly parse the rest of the inventory
                panel = pg.find("td", {'width': '120'}).parent.parent.find_next("table")
            else:
                panel = pg.find("td", {'width': '120'}).parent.parent
                          
            for row in panel.find_all("tr"):
                for item in row.find_all("td"):
                    tmpItem = UserShopFrontItem(item.b.text)
                    
                    tmpItem.owner = owner
                    tmpItem.usr = usr
                    tmpItem.buyURL = item.a['href']
                    tmpItem.desc = item.img['title']
                    tmpItem.img = item.img['src']
                    tmpItem.price = item.text.split("Cost : ")[1]
                    tmpItem.stock = item.text.split(" in stock")[0][-1:]
                        
                    self.items[item.b.text] = tmpItem
        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user shop front inventory.")
            logging.getLogger("neolib.html").info("Unable to parse user shop front inventory.", {'pg': pg})
            raise parseException
            
    def _parseMainItem(self, pg, usr, owner):
        panel = pg.find("td", {'width': '120'}).parent.parent
        
        item = panel.find_all("tr")[0].find_all("td")[0]
        
        tmpItem = UserShopFrontItem(item.b.text)
        
        tmpItem.owner = owner
        tmpItem.usr = usr
        tmpItem.buyURL = item.a['href']
        tmpItem.desc = item.img['title']
        tmpItem.img = item.img['src']
        tmpItem.price = item.text.split("Cost : ")[1]
        tmpItem.stock = item.text.split(" in stock")[0][-1:]
        
        self.items[item.b.text] = tmpItem

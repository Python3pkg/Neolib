from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.exceptions import UBItemException
from neolib.exceptions import questLimitException
from neolib.shop.ShopWizard import ShopWizard
from neolib.shop.UserShopFront import UserShopFront
from neolib.item.Item import Item
import time
import logging

class KitchenQuest:
    
    usr = None
    recipe = ""
    time = None
    items = None
    npSpent = 0
    prize = ""
    
    failedItem = ""
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        pg = usr.getPage("http://www.neopets.com/island/kitchen.phtml")
        
        if "Sorry, too late" in pg.content:
            pg = usr.getPage("http://www.neopets.com/island/kitchen.phtml")
        
        if "there is a limit of" in pg.content:
            raise questLimitException
        
        if "still need some ingredients from you" in pg.content:
            self._parseActiveQuest(pg)
            
            usr.loadInventory()
            for item in self.items:
                if item.name in usr.inventory:
                    del(self.items[self.items.index(item)])
            return
            
        try:
            self.recipe = pg.find("td", "content").find("input", {'name': 'food_desc'})['value']
        except Exception:
            logging.getLogger("neolib.quest").exception("Failed to parse quest recipe")
            logging.getLogger("neolib.html").info("Failed to parse quest recipe", {'pg': pg})
            raise parseException
            
        pg = usr.getPage("http://www.neopets.com/island/kitchen2.phtml", {'food_desc': self.recipe})
        
        try:
            hour = pg.find("td", "content").find_all("b")[2].text
            min = pg.find("td", "content").find_all("b")[3].text
            
            self.time = (hour, min)
            
            self.items = []
            for item in pg.find("td", "content").table.find_all("td"):
                tmpItem = Item(item.b.text)
                tmpItem.img = item.img['src']
                
                self.items.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.quest").exception("Failed to parse quest details")
            logging.getLogger("neolib.html").info("Failed to parse quest details", {'pg': pg})
            raise parseException

    def updateQuest(self):
        pg = self.usr.getPage("http://www.neopets.com/island/kitchen.phtml")
        self._parseActiveQuest(pg)
        
    def getPrice(self, searches):
        totalPrice = 0
        
        for item in self.items:
            res = ShopWizard.priceItem(self.usr, item.name, searches, ShopWizard.RETLOW)
            
            if not res:
                self.failedItem = item.name
                return False
            
            item.price, item.owner, item.id = res
            totalPrice += item.price
            
        self.npSpent = totalPrice
        return True
        
    def buyQuestItems(self):
        for item in self.items:
            us = UserShopFront(self.usr, item.owner, item.id, str(item.price))
            us.loadInventory()
            
            if not item.name in us.inventory:
                return False
                
            if not us.inventory[item.name].buy():
                return False
                
        return True
                
    def submitQuest(self):
        pg = self.usr.getPage("http://www.neopets.com/island/kitchen2.phtml", {'type': 'gotingredients'})
        
        if "Woohoo" in pg.content:
            try:
                self.prize = pg.find(text = "The Chef waves his hands, and you may collect your prize...").parent.parent.find_all("b")[-1].text
            except Exception:
                logging.getLogger("neolib.quest").exception("Failed to parse kitchen quest prize")
                logging.getLogger("neolib.html").info("Failed to parse kitchen quest prize", {'pg': pg})
                raise parseException
                
            return True
        else:
            logging.getLogger("neolib.quest").info("Failed to complete kitchen quest")
            logging.getLogger("neolib.html").info("Failed to complete kitchen quest", {'pg': pg})
            return False
                

    def _parseActiveQuest(self, pg):
        try:
            dets = pg.find("td", "content").table.find_all("td")
            
            self.recipe = dets[1].text
            
            hour = dets[3].find_all("b")[1].text
            min = dets[3].find_all("b")[2].text
            self.time = (hour, min)
            
            imgs = pg.find("td", "content").table.find_all("td")[5].find_all("img")
            items = pg.find("td", "content").table.find_all("td")[5].find_all("b")
            
            self.items = []
            for i in range(len(items)):
                tmpItem = Item(items[i].text)
                tmpItem.img = imgs[i]['src']
                
                self.items.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.quest").exception("Failed to parse quest details")
            logging.getLogger("neolib.html").info("Failed to parse quest details", {'pg': pg})
            raise parseException

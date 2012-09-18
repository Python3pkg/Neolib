from neolib.exceptions import invalidSearch
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.exceptions import shopWizBanned
from neolib.exceptions import activeQuest
from neolib.exceptions import invalidMethod
from neolib.item.Item import Item
import logging
import time

class ShopWizard:
    
    SHOP = "shop"
    GALLERY = "gallery"
    
    CONTAINING = "containing"
    EXACT = "exact"

    AVERAGE = "AVERAGE"
    LOWDEDUCT = "LOWDEDUCT"
    AVGDEDUCT = "AVGDEDUCT"
    LOW = "LOW"
    RETLOW = ""
    
    waitTime = 5
    
    @staticmethod
    def search(usr, text, area = "shop", scope = "exact", min = "0", max = "99999"):
        if not usr:
            raise invalidUser
        
        if not text:
            raise invalidSearch
            
        if area != ShopWizard.SHOP and area != ShopWizard.GALLERY:
            logging.getLogger("neolib.shop").info("Invalid area supplied for shop wizard search: " + area)
            raise invalidSearch
            
        if scope != ShopWizard.CONTAINING and scope != ShopWizard.EXACT:
            logging.getLogger("neolib.shop").info("Invalid scope supplied for shop wizard search: " + area)
            raise invalidSearch
            
        if int(min) < 0:
            logging.getLogger("neolib.shop").info("Invalid min value supplied for shop wizard search: " + min)
            raise invalidSearch
            
        if int(max) > 99999:
            logging.getLogger("neolib.shop").info("Invalid max value supplied for shop wizard search: " + max)
            raise invalidSearch
            
        post = {'type': 'process_wizard', 'feedset': '0', 'shopwizard': text, 'table': area, 'criteria': scope, 'min_price': min, 'max_price': max}
        pg = usr.getPage("http://www.neopets.com/market.phtml", post, {'Referer': 'http://www.neopets.com/market.phtml'})
        
        # Indicates shop wizard banned
        if pg.content.find("Whoa there") != -1:
            time = pg.find("b", text = "Whoa there, too many searches!").parent.p.b.text
            e = shopWizBanned()
            e.time = time
            raise e
            
        # Indicates a faerie quest
        if pg.content.find("You're working for a faerie") != -1:
            logging.getLogger("neolib.shop").info("Could not search for " + text + ". A Faerie quest is active")
            raise activeQuest
            
        if pg.content.find("did not find") != -1:
            if pg.content.find(text) != -1:
                return False # Indicates UB item
            elif pg.content.find("...</span>") != -1:
                # Probably invalid item
                raise invalidSearch
        
        try:
            items = pg.find("td", "contentModuleHeaderAlt").parent.parent.find_all("tr")
            items.pop(0)
            
            results = []
            for item in items:
                tmpItem = Item(item.find_all("td")[1].text)
                
                tmpItem.owner = item.td.a.text
                tmpItem.location = item.td.a['href']
                tmpItem.stock = item.find_all("td")[2].text
                tmpItem.price = item.find_all("td")[3].text.replace(" NP", "").replace(",", "")
                tmpItem.id = tmpItem.location.split("buy_obj_info_id=")[1].split("&")[0]
                
                results.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.shop").exception("Unable to parse shop wizard results.")
            logging.getLogger("neolib.html").info("Unable to parse shop wizard results.", {'pg': pg})
            raise parseException
            
        return results
        
    @staticmethod
    def priceItem(usr, item, searches, method = "AVERAGE", deduct = 0):
        prices = []
        dets = {}
        for x in range(0, searches):
            results = ShopWizard.search(usr, item)
            
            # Set to -1 if not found
            if not results:
                prices.append(-1)
                continue
            
            prices.append(int(results[0].price))
            dets[str(results[0].price)] = (results[0].owner, results[0].id)
            
            time.sleep(ShopWizard.waitTime)
            
        # Determines if item was UB
        if sum(prices) == len(prices) * -1:
            return False
            
        prices = filter(lambda x: x != -1, prices)
            
        if method == ShopWizard.RETLOW:
            price = sorted(prices)[0]
            return (price, dets[str(price)][0], dets[str(price)][1])
            
        return ShopWizard.__determinePrice(prices, method)
        
    @staticmethod
    def __determinePrice(prices, method):
        price = 1
        if method == ShopWizard.AVERAGE:
            price = int(sum(prices) / len(prices))
        elif method == ShopWizard.LOWDEDUCT:
            if deduct < 1 and deduct > 0:
                price = int(sorted(prices)[0] * (1 - deduct))
            else:
                price = sorted(prices)[0] - deduct
                
            if price <= 0:
                price = 1
        elif method == ShopWizard.AVGDEDUCT:
            if deduct < 1 and deduct > 0:
                price = int((sum(prices) / len(prices)) * (1 - deduct))
            else:
                price = int(sum(prices) / len(prices)) - deduct
            
            if price <= 0:
                price = 1
        elif method == ShopWizard.LOW:
            price = sorted(prices)[0]
        else:
            logging.getLogger("neolib.shop").exception("Invalid method given in ShopWizard.priceItem: " + method)
            raise invalidMethod
            
        return price

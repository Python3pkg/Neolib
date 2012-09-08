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

    # Returns the average of lowest prices
    AVERAGE = "AVERAGE"
    
    # Takes the lowest price and deducts x
    LOWDEDUCT = "LOWDEDUCT"
    
    # Takes the average of lowest prices and deducts x
    AVGDEDUCT = "AVGDEDUCT"
    
    # Returns the lowest price
    LOW = "LOW"
    
    # The amount of time to wait between searches in priceItem
    waitTime = 5
    
    @staticmethod
    def search(usr, text, area = "shop", scope = "exact", min = "0", max = "99999"):
        # Ensure we have a user
        if not usr:
            raise invalidUser
        
        # Make sure we got a search string
        if not text:
            raise invalidSearch
            
        # Verify we got proper search parameters
        if area != ShopWizard.SHOP and area != ShopWizard.GALLERY:
            logging.getLogger("neolib.shop").info("Invalid area supplied for shop wizard search: " + area)
            raise invalidSearch
            
        if scope != ShopWizard.CONTAINING and scope != ShopWizard.EXACT:
            logging.getLogger("neolib.shop").info("Invalid scope supplied for shop wizard search: " + area)
            raise invalidSearch
            
        # Verify ranges
        if int(min) < 0:
            logging.getLogger("neolib.shop").info("Invalid min value supplied for shop wizard search: " + min)
            raise invalidSearch
            
        if int(max) > 99999:
            logging.getLogger("neolib.shop").info("Invalid max value supplied for shop wizard search: " + max)
            raise invalidSearch
            
        # Submit the search
        post = {'type': 'process_wizard', 'feedset': '0', 'shopwizard': text, 'table': area, 'criteria': scope, 'min_price': min, 'max_price': max}
        pg = usr.getPage("http://www.neopets.com/market.phtml", post, {'Referer': 'http://www.neopets.com/market.phtml'})
        
        # Check if we're shop wiz banned
        if pg.content.find("Whoa there") != -1:
            time = pg.getParser().find("b", text = "Whoa there, too many searches!").parent.p.b.text
            e = shopWizBanned()
            e.time = time
            raise e
            
        # Ensure a quest is not active
        if pg.content.find("You're working for a faerie") != -1:
            logging.getLogger("neolib.shop").info("Could not search for " + text + ". A Faerie quest is active")
            raise activeQuest
        
        # Random decoding problems due to UB items can cause exceptions. Isolate them here so they do not disrupt higher processes.
        try:
            # Check if it's a probable UB, invalid item, or shop wizard banned
            if pg.content.find("did not find") != -1:
                if pg.content.find(text) != -1:
                    # Probably an UB or the region searched yielded nothing
                    return False
                elif pg.content.find("...</span>") != -1:
                    # Probably invalid item
                    raise invalidSearch
        except Exception:
            return False
        
        try:
            # Parse the results
            items = pg.getParser().find("td", "contentModuleHeaderAlt").parent.parent.find_all("tr")
            items.pop(0)
            
            results = []
            # Loop through all items
            for item in items:
                # Make a new Item and set it's attributes
                tmpItem = Item(item.find_all("td")[1].text)
                
                tmpItem.owner = item.td.a.text
                tmpItem.location = item.td.a['href']
                tmpItem.stock = item.find_all("td")[2].text
                tmpItem.price = item.find_all("td")[3].text.replace(" NP", "").replace(",", "")
                
                # Append the item to the results
                results.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.shop").info("Unable to parse shop wizard results.")
            logging.getLogger("neolib.html").info("Unable to parse shop wizard results.", {'pg': pg})
            raise parseException
            
        return results
        
    @staticmethod
    def priceItem(usr, item, searches, method = "AVERAGE", deduct = 0):
        # Get prices
        prices = []
        for x in range(0, searches):
            results = ShopWizard.search(usr, item)
            
            # If it was not found, just set it to -1
            if not results:
                prices.append(-1)
                continue
            
            prices.append(int(results[0].price))
            
            # Wait before searching again
            time.sleep(ShopWizard.waitTime)
            
        # Check if the item is classified as UB and return False if so
        if sum(prices) == len(prices) * -1:
            return False
            
        # Return a price depending on the selected method
        if method == ShopWizard.AVERAGE:
            return int(sum(prices) / len(prices))
        elif method == ShopWizard.LOWDEDUCT:
            if deduct < 1 and deduct > 0:
                price = int(sorted(prices)[0] * (1 - deduct))
            else:
                price = sorted(prices)[0] - deduct
            if price <= 0:
                return 1
            else:
                return price
        elif method == ShopWizard.AVGDEDUCT:
            if deduct < 1 and deduct > 0:
                price = int((sum(prices) / len(prices)) * (1 - deduct))
            else:
                price = int(sum(prices) / len(prices)) - deduct
            
            if price <= 0:
                return 1
            else:
                return price
        elif method == ShopWizard.LOW:
            return sorted(prices)[0]
        else:
            logging.getLogger("neolib.shop").exception("Invalid method given in ShopWizard.priceItem: " + method)
            raise invalidMethod
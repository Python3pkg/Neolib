from neolib.exceptions import invalidSearch
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.exceptions import shopWizBanned
from neolib.user.User import User
from neolib.item.Item import Item
import logging

class ShopWizard:
    
    SHOP = "shop"
    GALLERY = "gallery"
    
    CONTAINING = "containing"
    EXACT = "exact"
    
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
            raise shopWizBanned
        
        # Check if it's a probable UB, invalid item, or shop wizard banned
        if pg.content.find("did not find") != -1:
            if pg.content.lower().find(text.lower()) != -1:
                # Probably an UB or the region searched yielded nothing
                return False
            elif pg.content.find("...</span>") != -1:
                # Probably invalid item
                raise invalidSearch
        
        try:
            # Parse the results
            items = pg.getParser().find("td", "contentModuleHeaderAlt").parent.parent.find_all("tr")
            items.pop(0)
            
            results = []
            for item in items:
                # Make a new Item and set it's attributes
                tmpItem = Item(item.find_all("td")[1].text)
                
                tmpItem.owner = User(item.td.a.text, "")
                tmpItem.location = item.td.a['href']
                tmpItem.stock = item.find_all("td")[2].text
                tmpItem.price = item.find_all("td")[3].text
                
                # Append the item to the results
                results.append(tmpItem)
        except Exception:
            logging.getLogger("neolib.shop").info("Unable to parse shop wizard results. Source: " + pg.content)
            raise parseException
            
        return results
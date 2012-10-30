""":mod:`ShopWizard` -- Provides an interface for searching with the Shop Wizard

.. module:: ShopWizard
   :synopsis: Provides an interface for searching with the Shop Wizard
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidSearch
from neolib.exceptions import invalidUser
from neolib.exceptions import parseException
from neolib.exceptions import shopWizBanned
from neolib.exceptions import activeQuest
from neolib.exceptions import invalidMethod
from neolib.inventory.ShopWizardResult import ShopWizardResult
from neolib.item.Item import Item
import logging
import time

class ShopWizard:
    
    """Provides an interface for searching with the Shop Wizard
    
    Has functionality for searching and pricing using the Shop Wizard.
    Provides several options for pricing an item including returning
    information on the lowest item in a search result.
    
    Attributes
       waitTime (int) -- Time to wait in seconds between searches
        
    Example
       >>> res = ShopWizard.search("Mau Codestone")
       >>> for item in res:
       ...     print item.price
       4000
       4005
       ...
    """
    
    SHOP = "shop"
    GALLERY = "gallery"
    
    CONTAINING = "containing"
    EXACT = "exact"

    AVERAGE = "AVERAGE"
    LOWDEDUCT = "LOWDEDUCT"
    AVGDEDUCT = "AVGDEDUCT"
    LOW = "LOW"
    RETLOW = "RETLOW"
    
    methods = ['AVERAGE', 'LOWDEDUCT', 'AVGDEDUCT', 'LOW', 'RETLOW']
    
    waitTime = 5
    
    @staticmethod
    def search(usr, item, area = "shop", scope = "exact", min = "0", max = "99999"):
        """ Searches the shop wizard for the given item, returns result
        
        Uses the given parameters to send a search request with the Shop Wizard.
        Automatically parses the search results into individual items and appends
        them to and returns a ShopWizardResult. 
           
        Parameters:
           usr (User) -- User to search with
           item (str, Item) -- Item to search for
           area (str) -- Area to search in (ShopWizard.SHOP, ShopWizard.GALLERY)
           scope (str) -- Scope to search for (ShopWizard.CONTAINING, ShopWizard.EXACT)
           min (str) -- Minimum price
           max (str) -- Maximum price
           
        Returns
           ShopWizardResult - Search results
           
        Raises
           activeQuest
           shopWizBanned
           parseException
           invalidSearch
        """
        if not usr:
            raise invalidUser
        
        if not item:
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
            
        if isinstance(item, Item):
            item = item.name
        
        pg = usr.getPage("http://www.neopets.com/market.phtml?type=wizard")
        
        form = pg.form(action="market.phtml")
        form.update({'shopwizard': item, 'table': area, 'criteria': scope, 'min_price': str(min), 'max_price': str(max)})
        pg = form.submit()
        
        # Indicates shop wizard banned
        if "too many searches" in pg.content:
            time = pg.find("b", text = "Whoa there, too many searches!").parent.p.b.item
            e = shopWizBanned()
            e.time = time
            raise e
            
        # Indicates a faerie quest
        if "You're working for a faerie" in pg.content:
            logging.getLogger("neolib.shop").info("Could not search for " + item + ". A Faerie quest is active")
            raise activeQuest
            
        if "did not find" in pg.content:
            if item in pg.content:
                return False # Indicates UB item
            elif "...</span>" in pg.content:
                # Probably invalid item
                raise invalidSearch
            
        return ShopWizardResult(pg, usr)
        
    @staticmethod
    def price(usr, item, searches = 2, method = "AVERAGE", deduct = 0):
        """ Searches the shop wizard for given item and determines price with given method
        
        Searches the shop wizard x times (x being number given in searches) for the
        given item and collects the lowest price from each result. Uses the given
        pricing method to determine and return the price of the item. Below is information
        on each pricing method available:
           ShopWizard.AVERAGE -- Average of the lowest prices
           ShopWizard.LOWDEDUCT -- Deducts x (x = deduct) from the lowest price
           ShopWizard.AVGDEDUCT -- Deducts x (x = deduct) from the average of the lowest prices
           ShopWizard.LOW -- Returns the lowest price
           ShopWizard.RETLOW -- Returns an Item instance of the lowest price found
           
        Parameters:
           usr (User) -- User to search with
           item (str, Item) -- Item to search for
           searches (int) -- Number of times to search for the item
           method (str) -- Pricing method
           deduct (int) -- Amount to deduct from the price (if applicable)
           
        Returns
           int -- The item price
        """
        if not method in ShopWizard.methods: raise invalidMethod()
        
        if isinstance(item, Item):
            item = item.name
        
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
            
        prices = list(filter(lambda x: x != -1, prices))
            
        if method == ShopWizard.RETLOW:
            price = sorted(prices)[0]
            return (price, dets[str(price)][0], dets[str(price)][1])
            
        return ShopWizard.__determinePrice(prices, method, deduct)
        
    @staticmethod
    def __determinePrice(prices, method, deduct):
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

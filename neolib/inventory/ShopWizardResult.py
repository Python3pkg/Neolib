""":mod:`ShopWizardResult` -- Provides an interface for shop wizard results

.. module:: ShopWizardResult
   :synopsis: Provides an interface for shop wizard results
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import parseException
from neolib.inventory.Inventory import Inventory
from neolib.shop.UserShopFront import UserShopFront
from neolib.item.Item import Item
import logging

class ShopWizardResult(Inventory):
    
    """Represents a shop wizard search result
    
    Sub-classes the Inventory class to provide an interface for the results
    from a Shop Wizard search. Automatically populates itself with the results
    upon initialization.
    
    Attributes
       usr (User) - The user associated with the results
       
    Initialization
       ShopWizardResult(pg, usr)
       
       Loads results from a shop wizard search
       
       Parameters
          pg (Page) - The page containing the results
          usr (User) - The user to load the SDB for
          
       Raises
          parseException
        
    Example
       >>> res = ShopWizard.search(usr, "Mau Codestone")
       >>> for item in res:
       ...     print item.price
       3,000
       3,001
       ...
    """
    
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
            logging.getLogger("neolib.shop").exception("Unable to parse shop wizard results.", {'pg': pg})
            raise parseException

    def shop(self, index):
        """ Return's the user shop the indexed item is in
           
        Parameters:
           index (int) -- The item index
           
        Returns
           UserShopFront - User shop item is in
        """
        return UserShopFront(self.usr, item.owner, item.id, str(item.price))

    def buy(self, index):
        """ Attempts to buy indexed item, returns result
           
        Parameters:
           index (int) -- The item index
           
        Returns
           bool - True if item was bought, false otherwise
        """
        item = self.items[index]
        us = UserShopFront(self.usr, item.owner, item.id, str(item.price))
        us.load()
        
        if not item.name in us.inventory:
            return False
        
        if not us.inventory[item.name].buy():
            return False
                
        return True
        

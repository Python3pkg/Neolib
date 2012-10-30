""":mod:`MainShopInventory` -- Represents an item in the back-end of a user shop

.. module:: MainShopInventory
   :synopsis: Represents an item in the back-end of a user shop
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.item.Item import Item

class UserShopBackItem(Item):
    
    """Represents an item in the back-end of a user shop
    
    Attributes
       pos (str) -- The item's position in the shop inventory
    
    Initialization
       See Item
        
    Example
       >>> itm = UserShopBackItem("Green Apple")
    """
    
    pos = None
    oldPrice = None

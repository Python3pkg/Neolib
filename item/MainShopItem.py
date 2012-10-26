""":mod:`MainShopInventory` -- Represents a main shop item

.. module:: MainShopInventory
   :synopsis: Represents a main shop item
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import failedOCR
from neolib.item.Item import Item
import Image
import StringIO
import time

class MainShopItem(Item):
    
    """Represents a main shop item
    
    Contains functionality for purchasing a main shop item
    including cracking it's associated OCR.
    
    Attributes
       stockid (str) -- The item's stock ID
       brr (str) -- Item's brr
    
    Initialization
       See Item
        
    Example
       >>> itm = MainShopItem("Green Apple")
       >>> itm.usr = usr
       >>> itm.stockid = "37483739"
       >>> itm.brr = "1337"
       >>> itm.buy("100")
       True
    """
    
    stockid = None
    brr = None
        
    def buy(self, price, pause=0):
        """ Attempts to purchase a main shop item, returns result
        
        Uses the item's stock id and brr to navigate to the haggle page. Auotmatically downloads
        the OCR image from the haggle page and attempts to crack it. Submits the haggle form with
        the given price and returns if the item was successfully bought or not.
           
        Parameters:
           price (str) -- The price to buy the item for
           pause (int) -- The time in seconds to pause before submitting the haggle form
           
        Returns
           bool - True if successful, false otherwise
           
        Raises:
           failedOCR
        """
        pg = self.usr.getPage("http://www.neopets.com/haggle.phtml?obj_info_id=%s&stock_id=%s&brr=%s" % (self.id, self.stockid, self.brr))
        form = pg.getForm(name="haggleform")
        
        form['x'], form['y'] = self.crackOCR(StringIO.StringIO(self.usr.getPage("http://www.neopets.com" + form.image).content))
        form['current_offer'] = price
        
        if pause != 0:
            time.sleep(pause)
        
        pg = form.submit(self.usr)
        
        if "I accept" in pg.content:
            return True
        elif "You must select the correct pet" in pg.content:
            logging.getLogger("neolib.item").exception("Failed to crack OCR")
            raise failedOCR
        else:
            return False
        
    def crackOCR(self, image):
        """ Attempts to crack the given OCR
        
        Uses the "darkest pixel" method to find the darkest pixel in the image. Once
        found it generates a virtual box around the rest of the pet and returns the
        x and y coordinate of the middle of the virtual box. About 98.7% accurate.
           
        Parameters:
           img (StringIO) -- The image content
           
        Returns
           tuple - The x and y coordinates of the center of the pet
           
        Raises
           failedOCR
        """
        try:
            im = Image.open(image)
            
            # Convert to greyscale, and find darkest pixel
            im = im.convert("L")
            lo, hi = im.getextrema()
            
            # Find the pet outline and create a rectangle around a part of it
            im = im.point(lambda p: p == lo)
            rect = im.getbbox()
            
            # Return the center point
            return (str(0.5 * (rect[0] + rect[2])), str(0.5 * (rect[1] + rect[3])))
        except Exception:
            logging.getLogger("neolib.item").exception("Failed to crack OCR")
            raise failedOCR

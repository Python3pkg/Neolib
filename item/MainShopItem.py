from neolib.exceptions import failedOCR
from neolib.item.Item import Item
import Image
import StringIO
import time

class MainShopItem(Item):
    
    stockid = None
    brr = None
        
    def buy(self, price, pause=0):
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

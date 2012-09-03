from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
import logging

class ShopOfOffers(Daily):
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/shop_of_offers.phtml?slorg_payout=yes")
        
        # Check if we got something
        if pg.content.find("Something has happened!") != -1:
            try:
                # Set win to true and parse nps
                self.win = True
                self.nps = pg.getParser().find("td", text = "Something has happened!").find_next("td", width="320").strong.text
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Pet Pet Park daily. Source: \n" + pg.content + "\n\n\n")
                raise parseException
        else:
            raise dailyAlreadyDone
            
        return True
        
    def getMessage(self):
        if self.win:
            return "You got " + self.nps + "!"
        else:
            return "You did not win anything"
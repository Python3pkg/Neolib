""":mod:`ShopOfOffers` -- Contains the ShopOfOffers class

.. module:: ShopOfOffers
   :synopsis: Contains the ShopOfOffers class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class ShopOfOffers(Daily):
    
    """Provides an interface for the Shop of Offers daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/shop_of_offers.phtml?slorg_payout=yes")
        
        # Check if we got something
        if "Something has happened!" in pg.content:
            try:
                # Parse nps
                self.nps = pg.find("td", text = "Something has happened!").find_next("td", width="320").strong.text
                
                # Show that we won
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Pet Pet Park daily.", {'pg': pg}) 
                raise parseException
        else:
            raise dailyAlreadyDone
        
    def getMessage(self):
        if self.win:
            return "You got " + self.nps + "!"
        else:
            return "You did not win anything"

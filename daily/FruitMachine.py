""":mod:`FruitMachine` -- Contains the FruitMachine class

.. module:: FruitMachine
   :synopsis: Contains the FruitMachine class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class FruitMachine(Daily):
    
    """Provides an interface for the Coltzan Shrine daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/desert/fruit/index.phtml")
        if "already had your free spin" in pg.content:
            raise dailyAlreadyDone
            
        form = pg.getForm(self.player, method="post")
        pg = form.submit()
        
        # Indicates we won
        if "this is not a winning spin" in pg.content:
            return
            
        try:
            self.win = True
            self.nps = pg.find("div", id="fruitResult").span.b.text
            
            # Indiciates addtional prize
            if "You also win" in pg.content:
                self.prize = pg.find("td", "prizeCell").img.b.text
                self.img = pg.find("td", "prizeCell").img['src']
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Fruit Machine daily.", {'pg': pg})
            raise parseException
                
    def getMessage(self):
        if self.win:
            ret = "You won " + self.nps
            
            if self.prize:
                ret += ". You also win " + self.prize
        else:
            ret = "You didn't win!"
            
        return ret

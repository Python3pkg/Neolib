""":mod:`GiantOmelette` -- Contains the GiantOmelette class

.. module:: GiantOmelette
   :synopsis: Contains the GiantOmelette class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class GiantOmelette(Daily):
    
    """Provides an interface for the Giant Omelette daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/prehistoric/omelette.phtml")
        
        form = pg.form(action="omelette.phtml")
        pg = form.submit()
        
        if "NO!" in pg.content:
            raise dailyAlreadyDone
        
        # Indiciates no omelette left
        if "there doesn't seem to be any left" in pg.content:
            return
        
        # Indiciates obtained some
        if "manage to take a slice" in pg.content:
            try:
                # Image is only indication of what type was grabbed
                self.img = pg.find("td", "content").img['src']
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Giant Omelette daily.", {'pg': pg})              
                raise parseException
        else:
            logging.getLogger("neolib.daily").exception("Failed to grab Omelette.", {'pg': pg})
            
    def getMessage(self):
        if self.win:
            return "You got some Omelette!"
        else:
            return "You did not win anything"

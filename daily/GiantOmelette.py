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
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/prehistoric/omelette.phtml")
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/prehistoric/omelette.phtml", {'type': 'get_omelette'})
        
        # Ensure daily not previously completed
        if "NO!" in pg.content:
            raise dailyAlreadyDone
        
        # Check if the omelette was there
        if "there doesn't seem to be any left" in pg.content:
            return
        
        # Check if we grabbed any
        if "manage to take a slice" in pg.content:
            try:
                # Grab the prize img
                self.img = pg.find("td", "content").img['src']
                
                # Show that we won
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Giant Omelette daily.")
                logging.getLogger("neolib.html").info("Could not parse Giant Omelette daily.", {'pg': pg})                
                raise parseException
        else:
            logging.getLogger("neolib.daily").exception("Failed to grab Omelette.")
            logging.getLogger("neolib.html").info("Failed to grab Omelette.", {'pg': pg}) 
            
    def getMessage(self):
        if self.win:
            return "You got some Omelette!"
        else:
            return "You did not win anything"

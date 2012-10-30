""":mod:`ColtzanShrine` -- Contains the ColtzanShrine class

.. module:: ColtzanShrine
   :synopsis: Contains the ColtzanShrine class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class ColtzanShrine(Daily):
    
    """Provides an interface for the Coltzan Shrine daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):   
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/desert/shrine.phtml")
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/desert/shrine.phtml", {'type': 'approach'})
        
        # Ensure daily not previously completed
        if "wait a while before visiting" in pg.content:
            raise dailyAlreadyDone
        
        # See if we won anything
        if not "http://images.neopets.com/desert/shrine_win.gif" in pg.content:
            return
        
        try:
            # Get the message
            self.msg = pg.find("p", text = "Coltzan's Shrine").find_next_sibling("div").text
            
            # See if there was an item
            block = pg.find("p", text = "Coltzan's Shrine").find_next_sibling("div").find_all("p")
            if len(block) >= 2:
                self.img = block[1].img['src']
                self.prize = block[1].img.text
                
            # Show that we won
            self.win = True
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Coltzan Shrine daily.", {'pg': pg})
            raise parseException
        
    def getMessage(self):
        if self.win:
            ret = "Coltzan says: " + self.msg
        
            if self.prize:
                ret += "You won: " + self.prize
        else:
            ret = "Coltzan didn't give you anything!"
            
        return ret
            

""":mod:`Anchor` -- Contains the Anchor class

.. module:: Anchor
   :synopsis: Contains the Anchor class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class Anchor(Daily):
        
    """Provides an interface for the Anchor Management daily
    
    For a more detailed description, please refer to the Daily class.
    """
        
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/pirates/anchormanagement.phtml")
        if "already done your share" in pg.content:
            raise dailyAlreadyDone
        
        form = pg.form(id="form-fire-cannon")
        pg = form.submit()
                
        # Indicates a prize
        if "left you a memento" in pg.content:
            try:
                self.prize = pg.find("span", "prize-item-name").text
                self.img = pg.find("span", "prize-item-name").parent.parent.img['src']
                
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Failed to parse Anchor daily.", {'pg': pg})
                raise parseException
        else:
            logging.getLogger("neolib.daily").info("Did not get a prize from Anchor.", {'pg': pg})
            
    def getMessage(self):
        if self.win:
            return "You won a " + self.prize + "!"
        else:
            return "You did not win anything"

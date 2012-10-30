""":mod:`PetPetPark` -- Contains the PetPetPark class

.. module:: PetPetPark
   :synopsis: Contains the PetPetPark class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class PetPetPark(Daily):
    
    """Provides an interface for the Pet Pet Park daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/petpetpark/daily.phtml")
        
        form = pg.form(action="/petpetpark/daily.phtml")
        pg = form.submit()
        
        if "already collected your prize" in pg.content:
            raise dailyAlreadyDone
        
        try:
            self.img =  pg.find("div", "ppx_daily_message").img['src']
            self.prize = pg.find("div", "ppx_daily_message").a.text
            
            self.win = True
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Pet Pet Park daily.", {'pg': pg})
            raise parseException
        
    def getMessage(self):
        if self.win:
            return "You won " + self.prize + "!"
        else:
            return "You did not win anything"

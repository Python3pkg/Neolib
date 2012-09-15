from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class PetPetPark(Daily):
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/petpetpark/daily.phtml")
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/petpetpark/daily.phtml", {'go': '1'})
        
        # Ensure daily not previously completed
        if pg.content.find("already collected your prize") != -1:
            raise dailyAlreadyDone
        
        try:
            # Parse the prize
            self.img =  pg.find("div", "ppx_daily_message").img['src']
            self.prize = pg.find("div", "ppx_daily_message").a.text
            
            # Show that we won
            self.win = True
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Pet Pet Park daily.")
            logging.getLogger("neolib.html").info("Could not parse Pet Pet Park daily.", {'pg': pg})
            raise parseException
        
    def getMessage(self):
        if self.win:
            return "You won " + self.prize + "!"
        else:
            return "You did not win anything"
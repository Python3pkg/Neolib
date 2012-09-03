from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
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
            # Set win to true and parse prize
            self.win = True
            
            self.img =  pg.getParser().find("div", "ppx_daily_message").img['src']
            self.prize = pg.getParser().find("div", "ppx_daily_message").img.text
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Pet Pet Park daily. Source: \n" + pg.content + "\n\n\n")
            raise parseException
        
        return True
        
    def getMessage(self):
        if self.win:
            return "You won " + self.prize + "!"
        else:
            return "You did not win anything"
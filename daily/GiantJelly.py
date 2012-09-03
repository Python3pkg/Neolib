from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
import logging

class GiantJelly(Daily):
    
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/jelly/jelly.phtml")
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/jelly/jelly.phtml", {'type': 'get_jelly'})
        
        # Ensure daily not previously completed
        if pg.content.find("NO!") != -1:
            raise dailyAlreadyDone
        
        # Parse prize
        try:
            parts = pg.getParser().find_all("p")
        
            self.img = parts[2].img['src']
            self.prize = parts[3].b.text
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Giant Jelly daily. Source: \n" + pg.content + "\n\n\n")
            raise parseException
            
        return True
        
    def getMessage(self):
        return "You recieved a " + self.prize + "!"
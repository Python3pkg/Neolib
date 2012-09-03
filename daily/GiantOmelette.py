from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
import logging

class GiantOmelette(Daily):
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/prehistoric/omelette.phtml")
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/prehistoric/omelette.phtml", {'type': 'get_omelette'})
        
        # Ensure daily not previously completed
        if pg.content.find("NO!") != -1:
            raise dailyAlreadyDone
        
        # Check if we grabbed any
        if pg.content.find("manage to take a slice") != -1:
            try:
                # Set win to true and grab prize image
                self.win = True
                self.img = pg.getParser().find("td", "content").img['src']
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Giant Omelette daily. Source: \n" + pg.content + "\n\n\n")
                raise parseException
                
            return True
        else:
            logging.getLogger("neolib.daily").info("Failed to grab omelette. Source: \n" + pg.content + " \n\n\n")
            return True
            
    def getMessage(self):
        return "You recieved " + self.img + "!"
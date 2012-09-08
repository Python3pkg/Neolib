from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class Anchor(Daily):
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/pirates/anchormanagement.phtml")
        
        # Ensure daily not previously completed
        if pg.content.find("already done your share") != -1:
            raise dailyAlreadyDone
        
        # Parse form value
        action = pg.getParser().find("form", id = "form-fire-cannon").input['value']
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/pirates/anchormanagement.phtml", {'action': action})
        
        # See if we got something
        if pg.content.find("left you a memento"):
            try:
                # Parse the prize
                self.prize = pg.getParser().find("span", "prize-item-name").text
                self.img = pg.getParser().find("span", "prize-item-name").parent.parent.img['src']
                
                # Show that we won
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Failed to parse Anchor daily.")
                logging.getLogger("neolib.html").info("Failed to parse Anchor daily.", {'pg': pg})
                raise parseException
        else:
            logging.getLogger("neolib.daily").info("Did not get a prize from Anchor.")
            logging.getLogger("neolib.html").info("Did not get a prize from Anchor.", {'pg': pg})
            
    def getMessage(self):
        if self.win:
            return "You won a " + self.prize + "!"
        else:
            return "You did not win anything"
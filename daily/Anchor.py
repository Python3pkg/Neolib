from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
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
                
                self.win = True
            except Exception:
                logging.getLogger("neolib.daily").exception("Failed to parse Anchor daily. Source: \n" + pg.content + "\n\n\n")
                raise parseException
                
            return True
        else:
            logging.getLogger("neolib.daily").info("Did not get a prize from Anchor. Source: \n" + pg.content + "\n\n\n")
            return True
            
    def getMessage(self):
        return "You won a " + self.prize + "!"
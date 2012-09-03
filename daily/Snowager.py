from neolib.exceptions import snowagerAwake
from neolib.exceptions import dailyAlreadyDone
from neolib.daily.Daily import Daily
import logging

class Snowager(Daily):
    
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/winter/snowager.phtml")
        
        # See if he's awake
        if pg.content.find("Snowager is awake") != -1:
            raise snowagerAwake
            
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/winter/snowager2.phtml")
        
        # Ensure daily not previously completed
        if pg.content.find("dont want to try and enter again") != -1:
            raise dailyAlreadyDone
        
        # See if we ran
        if pg.content.find("decide to run") != -1:
            return True
            
        # Otherwise see what we got
        #mats = RegexLib.getMat("daily", "snowager", pg.content)
        
        # Ensure we matched
        #if not mats:
            #logging.getLogger("neolib.daily").exception("Failed to parse prize from Snowager. Source: \n" + pg.content + " \n\n\n")
            #return False
            
        self.win = True
        self.prize = mats[0][0]
        
        return True
            
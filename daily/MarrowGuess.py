from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.exceptions import marrowNotAvailable
from neolib.daily.Daily import Daily
import logging
import random

class MarrowGuess(Daily):
    
    def play(self, pounds = 0):  
        # If no guess was given, automatically generate one.
        if not pounds:
            # Neopets suggests between 200 - 800 pounds
            pounds = random.randrange(200, 800)
            
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/medieval/guessmarrow.phtml")
        
        f = open("test.html", "w")
        f.write(pg.content)
        f.close()
        
        # Ensure we can guess
        if pg.content.find("enter your value as an integer") == -1:
            raise marrowNotAvailable
            
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/medieval/process_guessmarrow.phtml", {'guess': str(pounds)})
        
        # Check if we got it right
        if pg.content.find("WRONG!") != -1:
            return True
            
    def getMessage(self):
        if this.win:
            # Future
            return "..."
        else:
            return "You did not guess right!"
""":mod:`MarrowGuess` -- Contains the MarrowGuess class

.. module:: MarrowGuess
   :synopsis: Contains the MarrowGuess class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.exceptions import marrowNotAvailable
import logging
import random

class MarrowGuess(Daily):
    
    """Provides an interface for the Marrow Guess daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self, pounds = 0):  
        # If no guess was given, automatically generate one.
        if not pounds:
            # Neopets suggests between 200 - 800 pounds
            pounds = random.randrange(200, 800)
            
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/medieval/guessmarrow.phtml")
        
        # Ensure we can guess
        if pg.content.find("enter your value as an integer") == -1:
            raise marrowNotAvailable
            
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/medieval/process_guessmarrow.phtml", {'guess': str(pounds)})
        
        # Check if we got it right
        if pg.content.find("WRONG!") != -1:
            return
            
        # NOTE: This daily is still under development
        # It is not currently known what a winning page looks like, thus it's logged until further development
        logging.getLogger("neolib.html").info("Possible Marrow Guess winning page", {'pg': pg})
        self.win = True
            
    def getMessage(self):
        if self.win:
            # NOTE: This daily is still under development
            return "You won. Please notify the application developer ASAP."
        else:
            return "You did not guess right!"
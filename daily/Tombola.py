""":mod:`Tombola` -- Contains the Tombola class

.. module:: Tombola
   :synopsis: Contains the Tombola class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class Tombola(Daily):
    
    """Provides an interface for the Tombola daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    booby = False
    ticket = ""
    
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/island/tombola.phtml")
	    
        pg = self.player.getPage("http://www.neopets.com/island/tombola2.phtml", {'submit': 'play'})
        
        if pg.content.find("only allowed one") != -1:
			raise dailyAlreadyDone()
        
        # Indicates no prizes
        if pg.content.find("don't even get a booby prize") != -1:
			return
		
        # The content layout will be different if the user won.
        if pg.content.find("YOU ARE A WINNER")!= -1:
            try:
                panel = pg.find("b", text="Tiki Tack Tombola").parent
                
                self.nps = panel.find_all("font")[1].text.split("Win ")[1]
                
                # First image is the ticket, so pop it off
                imgs = panel.find_all("img")
                imgs.pop(0)
                
                # The rest of the images are prizes, so parse them
                for img in imgs:
                    self.prize += img['src'].split("/")[-1].split(".")[0] + ", "
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily.")
                logging.getLogger("neolib.html").info("Could not parse Tombola daily.", {'pg': pg})
                raise parseException
        else:
            try:
                panel = pg.find("b", text="Tiki Tack Tombola").parent
                
                # Grab the item image and ticket number
                self.img = panel.img['src']
                self.ticket = panel.img['src'].split("/")[-1].replace(".gif", "")
                
                # Grab the message and the prize name
                parts = panel.find_all("b")
                self.msg = parts[1].text + parts[2].text
                self.prize = parts[3].text.replace("Your Prize - ", "")
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily.")
                logging.getLogger("neolib.html").info("Could not parse Tombola daily.", {'pg': pg})
                raise parseException
            
        if pg.content.find("feeling sorry for you") != -1:
            self.nps = panel.find_all("p")[-1].b.text + " NPS"
        
        if pg.content.find("not a winning ticket") != -1:
            self.booby = True
			
        self.win = True

    def getMessage(self):
        if self.win:
            ret = "You win " + self.prize + "!"
            
            if self.nps:
                ret += " You also win " + self.nps + "!"
                
            return ret
        else:
            return "You did not win anything!"
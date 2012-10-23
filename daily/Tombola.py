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
	    
        form = pg.getForm(self.player, action="tombola2.phtml")
        pg = form.submit()
        
        if "only allowed one" in pg.content:
			raise dailyAlreadyDone()
        
        # Indicates no prizes
        if "don't even get a booby prize" in pg.content:
			return
		
        # The content layout will be different if the user won.
        if "YOU ARE A WINNER" in pg.content:
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
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily.", {'pg': pg})
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
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily.", {'pg': pg})
                raise parseException
            
        if "feeling sorry for you" in pg.content:
            self.nps = panel.find_all("p")[-1].b.text + " NPS"
        
        if "not a winning ticket" in pg.content:
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

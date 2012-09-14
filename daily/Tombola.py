from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class Tombola(Daily):
    # Whether or not the prize was a booby prize
    booby = False
    
    # The ticket number
    ticket = ""
    
    def play(self):
	    # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/island/tombola.phtml")
	    
	    # Process daily
        pg = self.player.getPage("http://www.neopets.com/island/tombola2.phtml", {'submit': 'play'})
        
        # Ensure daily not previously completed
        if pg.content.find("only allowed one") != -1:
			raise dailyAlreadyDone()
        
        # Check if we got any prize at all
        if pg.content.find("don't even get a booby prize") != -1:
			return
		
        # Check if we won. The content layout will be different if we won.
        if pg.content.find("YOU ARE A WINNER")!= -1:
            # Parse the response
            try:
                panel = pg.getParser().find("b", text="Tiki Tack Tombola").parent
                
                # Grab the nps won
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
            # Parse the response
            try:
                panel = pg.getParser().find("b", text="Tiki Tack Tombola").parent
                
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
            
        # See if they were feeling sorry
        if pg.content.find("feeling sorry for you") != -1:
            # Grab the "feel sorry" nps
            self.nps = panel.find_all("p")[-1].b.text + " NPS"
        
		# If it was a booby, make it known
        if pg.content.find("not a winning ticket") != -1:
            self.booby = True
			
		# Show that we won
        self.win = True

    def getMessage(self):
        if self.win:
            ret = "You win " + self.prize + "!"
            
            if self.nps:
                ret += " You also win " + self.nps + "!"
                
            return ret
        else:
            return "You did not win anything!"
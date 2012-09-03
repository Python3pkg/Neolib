from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
import logging

class Tombola(Daily):
    booby = False
    
    ticket = ""
    
    def play(self):
	    # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/island/tombola.phtml")
	    
	    # Process daily
        pg = self.player.getPage("http://www.neopets.com/island/tombola2.phtml", {'submit': 'play'})
        
        f = open("test.html", "w")
        f.write(pg.content)
        f.close()
        
        # Ensure daily not previously completed
        if pg.content.find("only allowed one") != -1:
			raise dailyAlreadyDone()
        
        # Check if we got any prize at all
        if pg.content.find("don't even get a booby prize") != -1:
			return True
		
        # Check if we won. The content layout will be different if we won.
        if pg.content.find("YOU ARE A WINNER"):
            # Parse the response
            try:
                panel = pg.getParser().find("b", text="Tiki Tack Tombola").parent
                
                self.nps = panel.find_all("font")[1].text.split("Win ")[1]
                
                # First image is the ticket
                imgs = panel.find_all("img")
                imgs.pop(0)
                
                for img in imgs:
                    self.prize += img['src'] + ", "
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily. Source: \n" + pg.content + "\n\n\n")
                raise parseException
        else:
            # Parse the response
            try:
                panel = pg.getParser().find("b", text="Tiki Tack Tombola").parent
                
                self.img = panel.img['src']
                self.ticket = panel.img['src'].split("/")[-1].replace(".gif", "")
                
                parts = panel.find_all("b")
                self.msg = parts[1].text + parts[2].text
                self.prize = parts[3].text.replace("Your Prize - ", "")
            except Exception:
                logging.getLogger("neolib.daily").exception("Could not parse Tombola daily. Source: \n" + pg.content + "\n\n\n")
                raise parseException
            
        # See if they were feeling sorry
        if pg.content.find("feeling sorry for you") != -1:
            self.nps = panel.find_all("p")[-1].b.text + " NPS"
        
		# If it was a booby, let them know
        if pg.content.find("not a winning ticket") != -1:
            self.booby = True
			
		# Set win to true and return
        self.win = True
        return True

    def getMessage(self):
        if self.win:
            ret = "You win " + self.prize + "!"
            
            if self.nps:
                ret += " You also win " + self.nps + "!"
                
            return ret
        else:
            return "You did not win anything!"
from neolib.RegexLib import RegexLib
import logging

class Tombola:
	
    win = False
    booby = False
    alreadyPlayed = False
	
    ticket = ""
    prize = ""
	
    def __init__(self):
        pass
		
    def play(self, usr):
        if not usr:
            logging.getLogger("neolib.daily").info("Invalid user object supplied to Tombola")
            return False
			
	    # Navigate to Tombola page
        pg = usr.getPage("http://www.neopets.com/island/tombola.phtml")
	    
	    # Play
        pg = usr.getPage("http://www.neopets.com/island/tombola2.phtml", {'submit': 'play'})
		
        f = open("test.html", "w")
        f.write(pg.pageContent)
        f.close()
        
        # Ensure user hasn't already played
        if pg.pageContent.find("only allowed one") != -1:
			self.alreadyPlayed = True
			return True
        
        # Check if we got any prize at all
        if pg.pageContent.find("don't even get a booby prize") != -1:
			return True
		
        # Parse the response
        mats = RegexLib.getMat("daily", "tombola", pg.pageContent)
        print mats
	    
	    # Ensure we have a proper response
        if not mats:
            logging.getLogger("neolib.daily").exception("Failed to parse tombola game message. HTTP Content was as follows: \n" + pg.pageContent + "\n\n\n")
            return False
		
		
		# Set the ticket number and prize
        self.ticket = mats[0][0]
        self.prize = mats[0][1]
		
		# If it was not a winning ticket, return now
        if pg.pageContent.find("not a winning ticket") != -1:
            self.booby = True
            return True
			
		# Otherwise set win to true and return
        self.win = True
        return True

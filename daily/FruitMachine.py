from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class FruitMachine(Daily):
    
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/desert/fruit/index.phtml")
        
        # Ensure daily not previously completed
        if pg.content.find("already had your free spin") != -1:
            raise dailyAlreadyDone
        
        # Parse form values
        spin = pg.find("div", "result").form.find_all("input")[0]['value']
        ck = pg.find("div", "result").form.find_all("input")[1]['value']
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/desert/fruit/index.phtml", {'spin': spin, 'ck': ck})
        
        # Check if we won
        if pg.content.find("this is not a winning spin") != -1:
            return
            
        try:
            # Set win to true and parse NPs won
            self.win = True
            self.nps = pg.find("div", id="fruitResult").span.b.text
            
            # Check if we have an additional prize
            if pg.content.find("You also win") != -1:
                # Parse the prize item name and image
                self.prize = pg.find("td", "prizeCell").img.b.text
                self.img = pg.find("td", "prizeCell").img['src']
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Fruit Machine daily.")
            logging.getLogger("neolib.html").info("Could not parse Fruit Machine daily.", {'pg': pg})
            raise parseException
                
    def getMessage(self):
        if self.win:
            ret = "You won " + self.nps
            
            if self.prize:
                ret += ". You also win " + self.prize
        else:
            ret = "You didn't win!"
            
        return ret
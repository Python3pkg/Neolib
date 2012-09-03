from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.daily.Daily import Daily
import logging

class FruitMachine(Daily):
    
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/desert/fruit/index.phtml")
        
        # Ensure daily not previously completed
        if pg.content.find("already had your free spin") != -1:
            raise dailyAlreadyDone
        
        # Parse form values
        spin = pg.getParser().find("div", "result").form.find_all("input")[0]['value']
        ck = pg.getParser().find("div", "result").form.find_all("input")[1]['value']
        
        # Process daily
        pg = self.player.getPage("http://www.neopets.com/desert/fruit/index.phtml", {'spin': spin, 'ck': ck})
        
        f = open("test.html", "w")
        f.write(pg.content)
        f.close()
        
        # Check if we won
        if pg.content.find("this is not a winning spin") != -1:
            return True
            
        try:
            # Set win to true and parse NPs won
            self.win = True
            self.nps = pg.getParser().find("div", id="fruitResult").span.b.text
            
            # Check if we have an additional prize
            if pg.content.find("You also win") != -1:
                # Parse the prize item name and image
                self.prize = pg.getParser().find("td", "prizeCell").img.b.text
                self.img = pg.getParser().find("td", "prizeCell").img['src']
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Fruit Machine daily. Source: \n" + pg.content + "\n\n\n")
            raise parseException
            
        return True
                
    def getMessage(self):
        if self.win:
            ret = "You won " + self.nps
            
            if self.prize:
                ret += ". You also win " + self.prize
        else:
            ret = "You didn't win!"
            
        return ret
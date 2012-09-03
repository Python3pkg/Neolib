from neolib.daily.Daily import Daily

class Obsidian(Daily):
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/magma/quarry.phtml")
        
        # Check if we got something
        if pg.content.find("has been added") != -1:
            self.win = True
        else:
            self.win = False
            
    def getMessage(self):
        if self.win:
            return "You add some Obsidian to your inventory"
        else:
            return "You did not get anything"
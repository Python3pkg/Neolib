""":mod:`Obsidian` -- Contains the Obsidian class

.. module:: Obsidian
   :synopsis: Contains the Obsidian class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily

class Obsidian(Daily):
        
    """Provides an interface for the Obsidian Quarry daily
    
    For a more detailed description, please refer to the Daily class.
    """
        
    def play(self):
        # Visit daily page
        pg = self.player.getPage("http://www.neopets.com/magma/quarry.phtml")
        
        # Check if we got something
        if "has been added" in pg.content:
            self.win = True
        else:
            self.win = False
            
    def getMessage(self):
        if self.win:
            return "You add some Obsidian to your inventory"
        else:
            return "You did not get anything"

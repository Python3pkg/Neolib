from neolib.exceptions import invalidUser
from neolib.exceptions import invalidDaily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.exceptions import marrowNotAvailable

#from neolib.daily.Anchor import Anchor
#from neolib.daily.ColtzanShrine import ColtzanShrine
#from neolib.daily.FruitMachine import FruitMachine
#from neolib.daily.GiantJelly import GiantJelly
#from neolib.daily.GiantOmelette import GiantOmelette
#from neolib.daily.MarrowGuess import MarrowGuess
#from neolib.daily.Obsidian import PetPetPark
#from neolib.daily.ShopOfOffers import ShopOfOffers
#from neolib.daily.Tombola import Tombola

class Daily(object):
    
    # Any message a daily may return
    msg = ""
    
    # Any prize a daily rewards
    prize = ""
    
    # Any nps a daily rewards
    nps = ""
    
    # The image of any item the daily rewards
    img = ""
    
    # The User object associated with the user playing this daily
    player = None
    
    # The status of whether the daily was successful or not
    win = False
    
    def __init__(self, usr):
        # Ensure we have a valid user
        if not usr:
            raise invalidUser
        
        # Set the user
        self.player = usr
    
    @staticmethod
    def doDailies(usr, dailyList):
        # Load all supported dailies
        dailies = []
        for daily in Daily.__subclasses__():
            dailies.append(daily.__name__)
            
        # Verify the list is accurate
        for daily in dailyList:
            if not daily in dailies:
                raise invalidDaily
                
        # Do dailies:
        for daily in Daily.__subclasses__():
            inst = daily(usr)
            try:
                inst.play()
                yield daily.__name__ + ": " + inst.getMessage()
            except dailyAlreadyDone:
                yield daily.__name__ + ": This daily is already done!"
            except parseException:
                yield daily.__name__ + ": A serious error has occurred. Please refer to the logs."
            except marrowNotAvailable:
                yield daily.__name__ + ": Not available at this time!"
""":mod:`Daily` -- Contains the Daily class

.. module:: Daily
   :synopsis: Contains the Daily class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import invalidUser
from neolib.exceptions import invalidDaily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
from neolib.exceptions import marrowNotAvailable

class Daily(object):
    
    """Provides an interface for dailies to subclass
    
    This class provides an interface for dailies to subclass as well as functionality
    for running through a list of dailies and performing each one.
    
    Attributes
       msg (str) - Daily's message
       prize (str) - Prize associated with the daily
       nps (str) - NPs associated with the daily
       img (str) - An image or item image associated with the daily
       player (User) - The User playing a daily
       win (bool) - Whether the user won or not
       
    Initialization
       Config(name)
       
       Initializes the daily
       
       Parameters
          usr (User) - The user playing the daily
        
    Example
       >>> list = ['Tombola', 'FruitMachine', 'PetPetPark']
       >>> for message in Daily.doDailies(usr, list):
       ...     print message
    """
    
    msg = ""
    prize = ""
    nps = ""
    img = ""
    player = None
    win = False
    
    def __init__(self, usr):
        if not usr:
            raise invalidUser
        
        self.player = usr
    
    @staticmethod
    def doDailies(usr, dailyList):
        """ Does a list of dailies and yields each result
        
        Takes a list of valid dailies, initiates each one, and then proceeds
        to play each one and yield it's resulting message. Note that the names
        given in the list must be the same as the daily's class file. 
        
        Parameters
           usr (User) - User to do the dailies with
           dailyList (list) - List of all daily names to perform
        """
        # Load all supported dailies
        dailies = []
        for daily in Daily.__subclasses__():
            dailies.append(daily.__name__)
            
        # Verify the list is accurate
        for daily in dailyList:
            if not daily in dailies:
                raise invalidDaily
                
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
from neolib.exceptions import invalidUser

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
    
    
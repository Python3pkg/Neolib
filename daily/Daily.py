from neolib.exceptions import invalidUser

class Daily:
    
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
    
    
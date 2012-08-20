from neolib.http.Page import Page
from neolib.RegLib import RegLib
from neolib.inventory.UserInventory import UserInventory

class User:
    username = ""
    password = ""
    
    cookieJar = None
    inventory = None
    
    nps = 0
    
    def __init__(self, username, password):
        # Set the username and password
        self.username = username
        self.password = password
        
    def login(self):
        # Construct the post data
        data = "username=" + self.username + "&password=" + self.password + "&destination=/index.phtml"
        
        # Send it
        pg = Page("http://www.neopets.com/login.phtml", postData = data)
        
        # Load the index and verify we're logged in
        pg = Page("http://www.neopets.com/index.phtml", pg.cookies)
        
        if pg.pageContent.find(self.username.lower()) != -1:
            # Set cookies
            self.cookieJar = pg.cookies
            
            # Grab NPs and active Neopet while we have the data
            self.nps = int( RegLib.getMat("user", "neopoints", pg.pageContent)[0].replace(",", "") )
            
            return True
        else:
            return False
            
    def loadInventory(self):
        # Loads the user's current inventory and sets inventory as an UserInventory object
        self.inventory = UserInventory(self)
            
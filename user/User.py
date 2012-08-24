from neolib.http.Page import Page
from neolib.RegLib import RegLib
from neolib.inventory.UserInventory import UserInventory

class User:
    # Account's username and password
    username = ""
    password = ""
    
    # User's stored cookies in form of a CookieJar object
    cookieJar = None
    
    # User's inventory in form of an UserInventory object
    inventory = None
    
    # User's current amount of neopoints
    nps = 0
    
    # Defines whether or not to automatically append a referer using the user's last visited page
    useRef = True
    
    # The user's last visisted page
    lastPage = ""
    
    def __init__(self, username, password):
        # Set the username and password
        self.username = username
        self.password = password
        
    def login(self):
        # Construct the post data
        data = "username=" + self.username + "&password=" + self.password + "&destination=/index.phtml"
        
        # Send it
        pg = self.getPage("http://www.neopets.com/login.phtml", {'username': self.username, 'password': self.password, 'destination': '/index.phtml'})
        
        # Store cookies
        self.cookieJar = pg.cookies
        
        # Load the index and verify we're logged in
        pg = self.getPage("http://www.neopets.com/index.phtml")
        
        if pg.pageContent.find(self.username.lower()) != -1:
            # Grab NPs and active Neopet while we have the data
            self.nps = int( RegLib.getMat("user", "neopoints", pg.pageContent)[0].replace(",", "") )
                
            return True
        else:
            return False
            
    def loadInventory(self):
        # Loads the user's current inventory and sets inventory as an UserInventory object
        self.inventory = UserInventory(self)
        
    def getPage(self, url, postData = None, vars = None):
        
        # If using a referer is desired and one has not already been supplied, then set the referer to the user's last visited page
        if self.useRef and len(self.lastPage) > 0:
            if not vars: vars = {'Referer': self.lastPage}
            elif not vars['Referer']: vars['Referer'] = self.lastPage
            
        # Update the user's last visited page
        self.lastPage = url
        
        # Return the page, ensuring to pass of user's cookies
        return Page(url, self.cookieJar, postData, vars)
            
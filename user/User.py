from neolib.http.Page import Page
from neolib.RegexLib import RegexLib
from neolib.inventory.UserInventory import UserInventory
from exceptions import LogoutException
import logging

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
    
    # Set's whether the class will attempt to automatically log back in when it detects a log out, or just raise an exception
    autoLogin = True
    
    # The user's state of being logged in
    loggedIn = False
    
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
            self.nps = int( RegexLib.getMat("user", "neopoints", pg.pageContent)[0].replace(",", "") )
            
            # Set the user as logged in
            self.loggedIn = True
            
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
        
        # Grab the page
        pg = Page(url, self.cookieJar, postData, vars)
        
        # Update user cookies
        self.cookieJar = pg.cookies
        
        # Check if the user was logged out
        if "Location" in pg.pageHeader.respVars:
            if pg.pageHeader.respVars['Location'].find("loginpage.phtml") != -1:
                # If auto login is enabled, try to log back in, otherwise raise an exception to let higher processes know the user is logged out.
                if self.autoLogin:
                    # Clear cookies
                    self.cookieJar = None
                    
                    if self.login():
                        # Update status
                        self.loggedIn = True
                        
                        # Request the page again now that the user is logged in
                        pg = Page(url, self.cookieJar, postData, vars)
                    else:
                        # Failed to login. Update status, log it, and raise an exception
                        self.loggedIn = False
                        logging.getLogger("neolib.user").info("User was logged out. Failed to log back in.")
                        raise LogoutException
                else:
                    # Auto login is not enabled. Update status and raise an exception.
                    self.loggedIn = False
                    logging.getLogger("neolib.user").info("User was logged out. Auto login is disabled.")
                    raise LogoutException
                    
        # Return the page
        return pg        
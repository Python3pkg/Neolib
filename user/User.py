from neolib.exceptions import logoutException
from neolib.inventory.UserInventory import UserInventory
from neolib.shop.UserShop import UserShop
from neolib.config.Config import Config
from neolib.http.Page import Page
from neolib.user.Bank import Bank
from neolib.user.hooks import *
from neolib.user.Pet import Pet
from neolib.user.SDB import SDB
import logging

class User:
    # Account's username and password
    username = ""
    password = ""
    
    # User's stored cookies in form of a CookieJar object
    cookieJar = None
    
    # User's inventory in form of an UserInventory object
    inventory = None
    
    # User's bank
    bank = None
    
    # User's shop
    shop = None
    
    # User's Safety Deposit Box
    SDB = None
    
    # User's current amount of neopoints
    nps = 0
    
    # User's active pet
    activePet = None
    
    # User's optional PIN number
    pin = None
    
    # The user's configuration data
    config = None
    
    # Defines whether or not to automatically append a referer using the user's last visited page
    useRef = True
    
    # The user's last visisted page
    lastPage = ""
    
    # User's optional proxy
    proxy = None
    
    # Set's whether the class will attempt to automatically log back in when it detects a log out, or just raise an exception
    autoLogin = True
    
    # The user's state of being logged in
    loggedIn = False
    
    # Set's whether or not this user will load and execute hooks
    useHooks = True
    
    def __init__(self, username, password, pin = None):
        # Set the username, password, and pin
        self.username = username
        self.password = password
        self.pin = pin
        
    def login(self):
        # Construct the post data
        data = "username=" + self.username + "&password=" + self.password + "&destination=/index.phtml"
        
        # Send it
        pg = self.getPage("http://www.neopets.com/login.phtml", {'username': self.username, 'password': self.password, 'destination': '/index.phtml'})
        
        # Store cookies
        self.cookieJar = pg.cookies
        
        # Load the index and verify we're logged in
        pg = self.getPage("http://www.neopets.com/index.phtml")
        
        if pg.content.find(self.username.lower()) != -1:
            # Set the user as logged in
            self.loggedIn = True
            
            return True
        else:
            return False
            
    def loadInventory(self):
        # Loads the user's current inventory and sets inventory as an UserInventory object
        self.inventory = UserInventory(self)
        
    def loadBank(self):
        # Loads the user's basic bank information and allows for actions like withdrawl, deposit, etc.
        self.bank = Bank(self)
        
    def loadShop(self):
        # Load the user's shop
        self.shop = UserShop(self)
        self.shop.loadInventory()
        
    def loadSDB(self):
        # Load the user's Safety Deposit Box
        self.SDB = SDB(self)
        self.SDB.loadInventory()
    
    def loadConfig(self):
        
        # Attempt to load user configuration file
        self.config = Config(self.username)
        
        # If it doesn't exist, create a new one with default settings
        if not self.config.data:
            data = {'useHooks': 'True', 'autoLogin': 'True'}
            
            Config.createUserConfig(self.username, data)
            self.config = Config(self.username)
    
    def updateNps(self, pg = None):
        # If no page is supplied, just load the index
        if not pg:
            pg = self.getPage("http://www.neopets.com/index.phtml")
            
        self.nps = int( pg.getParser().find("a", id = "npanchor").text.replace(",", "") )
    
    def setProxy(self, host, port):
        self.proxy = (host, port)
    
    def getPage(self, url, postData = None, vars = None, usePin = False):
        
        # If using a referer is desired and one has not already been supplied, then set the referer to the user's last visited page
        if self.useRef and len(self.lastPage) > 0:
            if not vars: vars = {'Referer': self.lastPage}
            elif not "Referer" in vars: vars['Referer'] = self.lastPage
            
        # Update the user's last visited page
        self.lastPage = url
        
        # Check if we need to include a pin
        if usePin:
            if self.pin:
                postData['pin'] = str(self.pin)
        
        # Grab the page
        pg = Page(url, self.cookieJar, postData, vars, self.proxy)
        
        # Update user cookies
        self.cookieJar = pg.cookies
        
        # Check if we are using hooks, and execute them if so
        if self.useHooks:
            for hook in UserHook.__subclasses__():
                self, pg = hook.processHook(self, pg)
                    
        # Return the page
        return pg        
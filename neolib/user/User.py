""":mod:`SDB` -- Represents a Neopets user account

.. module:: SDB
   :synopsis: Represents a Neopets user account
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import logoutException
from neolib.exceptions import neopetsOfflineException
from neolib.exceptions import noCookiesForDomain
from neolib.inventory.UserInventory import UserInventory
from neolib.http.browser.BrowserCookies import BrowserCookies
from neolib.shop.UserShop import UserShop
from neolib.config.Configuration import Configuration
from neolib.http.Page import Page
from neolib.user.Bank import Bank
from neolib.user.hooks import *
from neolib.user.Pet import Pet
from neolib.user.SDB import SDB
import logging
import zlib
import base64
import hashlib
import pickle

class User:
    
    """Represents a Neopets user account
    
    The glue of this library, this class represents a Neopets user account
    in the scope of an automated program. It links together many key components
    of the library including Bank, UserShop, SDB, and UserInventory. It allows
    for easy configuration, browser synchronization, and other basic configuration
    like username, password, pin, etc. This class is used as the focal point for
    the rest of the library.
    
    
    Attributes
       username (str) -- User's username
       password (str) -- User's password
       session (request-client) -- User's HTTP session
       inventory (UserInventory) -- User's inventory
       bank (Bank) -- User's bank
       shop (UserShop) -- User's shop
       SDB (SDB) -- User's safety deposit box
       nps (int) -- User's NPs
       activePet (Pet) -- User's current active neopet
       pin (int) -- User's pin
       config (Configuration) -- User's configuration
       hooks (list[func]) -- User's hooks for getPage()
       proxy (tuple) -- User's proxy
       browser (str) -- User's browser for syncing
       RECallBack (func) -- User's callback function for random events
       lastPage (str) -- Last page user visited
       useRef (bool) -- Whether or not to automatically append a referrer to requests (uses User.lastPage)
       autoLogin (bool) -- Whether or not to automatically log back in when a logout is detected
       useHooks (bool) -- Whether or not to use hooks with User.getPage()
       browserSync (bool) -- Whether or not to synchronize cookies with a web browser
       savePassword (bool) -- Whether or not to save the user's password in the configuration
       configVars (list[str]) -- List of attributes to save with User.exportVars()
       loggedIn (bool) -- Whether or not the user is logged in
       browsers (list[str]) -- List of all installed browsers on the local machine
       
    Initialization
       User(username, password="", pin=None)
       
       Initializes the user with the given details and attempts to load any configuration
       
       Sets the username, password, and pin. Checks if configuration is loaded and attempts
       to load it if not. Searches the configuration to see if this username has any saved 
       configuration data. If none is found, creates a section for this username with some
       default settings. If configuration is found, loads the configuration, including
       any exported attribute values. Also loads some default hooks which accomplish
       tasks like auto-login and keeping the activePet and NPs up to date.
       
       Parameters
          username (str) -- User's username
          password (str) -- User's password
          pin (int) -- User's 4 digit pin
        
    Example
       >>> usr = User("username", "password")
       >>> usr.login()
       True
       >>> usr.inventory.load()
       >>> usr.inventory
       {'someitem': Item<...>}
       >>> pg = usr.getPage("http://www.neopets.com/")
       >>> pg.title
       'Welcome to Neopets!'
    """
    
    username = ""
    password = ""
    
    session = None
    
    inventory = None
    bank = None
    shop = None
    SDB = None
    
    nps = 0
    activePet = None
    pin = None
    config = None
    hooks = None
    proxy = None
    browser = None
    RECallback = None
    
    lastPage = ""
    useRef = True
    autoLogin = True
    useHooks = True
    browserSync = False
    savePassword = False
    
    configVars = ['username', 'password', 'session', 'proxy', 'browser', 'useRef', 'autoLogin', 'useHooks', 'browserSync', 'savePassword']
    
    def __init__(self, username, password="", pin=None):
        # Neopets automatically converts all capitals in a username to lowercase
        self.username = username.lower()
        self.password = password
        self.pin = pin
        
        # Initialize
        self.inventory = UserInventory(self)
        self.shop = UserShop(self)
        self.bank = Bank(self)
        self.SDB = SDB(self)
        
        # Each User instance needs a unique session
        self.session = Page.newSession()
        
        # Default hooks
        self.hooks = []
        self.hooks.append(updateNPs)
        self.hooks.append(updatePet)
        self.hooks.append(autoLogin)
        
        # Config
        if not Configuration.loaded():
            if Configuration.initialize():
                self.__loadConfig()
        else:
            self.__loadConfig()
        
    @property
    def loggedIn(self):
        pg = self.getPage("http://www.neopets.com/")
        return self.username in pg.content
        
    @property
    def browsers(self):
        return BrowserCookies.loadBrowsers()
    
    def login(self):
        """ Logs the user in, returns the result
           
        Returns
           bool - Whether or not the user logged in successfully
        """
        # Request index to obtain initial cookies and look more human
        pg = self.getPage("http://www.neopets.com")
        
        form = pg.form(action="/login.phtml")
        form.update({'username': self.username, 'password': self.password})
        pg = form.submit()
        
        return self.username in pg.content
    
    def addHook(self, hook):
        """ Adds a hook for User.getPage()
        """
        self.hooks.append(hook)
        
    def setRandomEventCallback(self, cb):
        """ Sets the callback function for when a random event is detected
        """
        self.RECallback = cb
    
    def sync(self, browser):
        """ Enables cookie synchronization with specified browser, returns result
           
        Returns
           bool - True if successful, false otherwise
        """
        BrowserCookies.loadBrowsers()
        if not browser in BrowserCookies.browsers:
                return False
        
        self.browserSync = True
        self.browser = browser
        return True
        
    def deSync(self):
        """ Disables browser synchronization
        """
        self.browserSync = False
        
    def save(self):
        """ Exports all user attributes to the user's configuration and writes configuration
        
        Saves the values for each attribute stored in User.configVars
        into the user's configuration. The password is automatically
        encoded and salted to prevent saving it as plaintext. The 
        session is pickled, encoded, and compressed to take up
        less space in the configuration file. All other attributes
        are saved in plain text. Writes the changes to the configuration file.
        """
        # Code to load all attributes
        for prop in dir(self):
            if getattr(self, prop) == None: continue
            if not prop in self.configVars: continue
            
            # Special handling for some attributes
            if prop == "session":
                pic = pickle.dumps(getattr(self, prop).cookies)
                comp = zlib.compress(pic)
                enc = base64.b64encode(comp)
                self.config[prop] = enc.decode()
                continue
                    
            if prop == "password" and not self.savePassword: continue
            if prop == "password":
                s = hashlib.md5(self.username.encode()).hexdigest()
                p = base64.b64encode(getattr(self, prop).encode()) + s.encode()
                self.config[prop] = p.decode()
                continue
                
            self.config[prop] = str(getattr(self, prop))
                
        if 'password' in self.config and not self.savePassword: del self.config.password
        self.config.write()
        self.__loadConfig()
        
    def getPage(self, url, postData = None, vars = None, usePin = False):
        """ Requests and returns a page using the user's session
        
        If useRef is set to true, automatically appends a referer using
        the user's last page to the request. If usePin is set to true,
        automatically appends the user's pin to the POST data. If browser
        sync is enabled, automatically retrieves and uses the browser's
        most up to date cookies for the request and attempts to save the
        updated cookies to the browser's cookie database. If useHooks is
        set to true, delivers the resulting Page object to each hook
        function for processing. Finally, returns the requested page.
        
        Parameters
           url (str) -- URL of remote page
           postData (dict) -- POST data to send with request
           vars (dict) -- Additional HTTP Header variables to send with request
           usePin (bool) -- Whether or not to send the user's pin with the request
           
        Returns
           Page -- Requested page
           
        Raises
           neopetsOfflineException
        """
        # If using a referer is desired and one has not already been supplied, 
        # then set the referer to the user's last visited page.
        if self.useRef and len(self.lastPage) > 0:
            if not vars: vars = {'Referer': self.lastPage}
            elif not "Referer" in vars: vars['Referer'] = self.lastPage
            
        self.lastPage = url
        
        if usePin:
            if self.pin:
                # All forms that require a pin share the same variable name of 'pin'
                postData['pin'] = str(self.pin)
        
        if bool(self.browserSync):
            self.__syncCookies()
        
        pg = Page(url, usr=self, postData=postData, vars=vars, proxy=self.proxy)
        
        if self.browserSync:
            self.__writeCookies()
        
        if "http://images.neopets.com/homepage/indexbak_oops_en.png" in pg.content:
            raise neopetsOfflineException
        
        if self.useHooks:
            for hook in self.hooks:
                self, pg = hook(self, pg)
        return pg
        
    def __syncCookies(self):
        if self.browserSync:  
            cj = BrowserCookies.getCookies(self.browser, ".neopets.com")
            if not cj:
                return False
                
            self.session.cookies = cj
            return True
        return False
        
    def __writeCookies(self):
        if self.browserSync:  
            BrowserCookies.setCookies(self.browser, ".neopets.com", self.session.cookies)
            
    def __loadConfig(self):
        c = Configuration.getConfig()
        if not self.username in c.users:
            c.users.addSection(self.username)
            self.config = c.users[self.username]
            self.save()
            return
            
        self.config = c.users[self.username]
        for key in self.config:
            if not key in self.configVars: continue
            
            if self.config[key] == 'True':
                self.config.__dict__[key] = True
            elif self.config[key] == 'False':
                self.config.__dict__[key] = False
                
            # Special handling for some attributes
            if key == "session":
                enc = base64.b64decode(self.config.__dict__[key].encode())
                comp = zlib.decompress(enc)
                pic = pickle.loads(comp)
                self.session.cookies = pic
                continue
                
            if key == "password":
                s = hashlib.md5(self.username.encode()).hexdigest()
                p = base64.b64decode(self.config.__dict__[key].replace(s, "").encode())
                setattr(self, key, p.decode())
                continue
            
            setattr(self, key, self.config.__dict__[key])
        
    def __str__(self):
        return self.username
        
    def __repr__(self):
        return "<User \"" + self.username + "\">"

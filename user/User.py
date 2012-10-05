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

class User:
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
    loggedIn = False
    useHooks = True
    browserSync = False
    
    configVars = ['username', 'proxy', 'browser', 'useRef', 'autoLogin', 'useHooks', 'browserSync']
    
    def __init__(self, username, password = "", pin=None):
        # Neopets automatically converts all capitals in a username to lowercase
        self.username = username.lower()
        self.password = password
        self.pin = pin
        
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
        
    def login(self):
        pg = self.getPage("http://www.neopets.com/login.phtml", {'username': self.username, 'password': self.password, 'destination': '/index.phtml'})
        
        # Index page should contain the username if successfully logged in
        if pg.content.find(self.username) != -1:
            self.loggedIn = True
            return True
        else:
            return False
            
    def loadInventory(self):
        self.inventory = UserInventory(self)
        
    def loadBank(self):
        self.bank = Bank(self)
        
    def loadShop(self):
        self.shop = UserShop(self)
        self.shop.loadInventory()
        
    def loadSDB(self):
        self.SDB = SDB(self)
        self.SDB.loadInventory()
    
    def addHook(self, hook):
        self.hooks.append(hook)
        
    def setRandomEventCallback(self, cb):
        self.RECallback = cb
    
    def updateNps(self, pg = None):
        # If no page is supplied, just load the index
        if not pg:
            pg = self.getPage("http://www.neopets.com/index.phtml")
            
        self.nps = int( pg.find("a", id = "npanchor").text.replace(",", "") )
    
    def setProxy(self, proxy):
        self.proxy = proxy
    
    def syncWithBrowser(self, browser):
        BrowserCookies.loadBrowsers()
        if not browser in BrowserCookies.browsers:
                return False
        
        self.browserSync = True
        self.browser = browser
        return True
        
    def exportVars(self):
        # Code to load all attributes
        for prop in dir(self):
            if getattr(self, prop) == None: continue
            if not prop in self.configVars: continue
            self.config[prop] = str(getattr(self, prop))
            
        self.config.write()
        
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
            self.exportVars()
            return
            
        self.config = c.users[self.username]
        for key in self.config:
            if not key in self.configVars: continue
            if self.config[key] == 'True':
                self.config.__dict__[key] = True
            elif self.config[key] == 'False':
                self.config.__dict__[key] = False
            setattr(self, key, self.config.__dict__[key])
        
    
    def getPage(self, url, postData = None, vars = None, usePin = False):
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
        
        pg = Page(url, self.session, postData, vars, self.proxy)
        self.cookieJar = pg.cookies
        
        if self.browserSync:
            self.__writeCookies()
        
        if pg.content.find("http://images.neopets.com/homepage/indexbak_oops_en.png") != -1:
            raise neopetsOfflineException
        
        if self.useHooks:
            for hook in self.hooks:
                self, pg = hook(self, pg)
        return pg        
        
    def __str__(self):
        return self.username

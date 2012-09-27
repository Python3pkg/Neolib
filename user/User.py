from neolib.exceptions import logoutException
from neolib.exceptions import neopetsOfflineException
from neolib.exceptions import noCookiesForDomain
from neolib.inventory.UserInventory import UserInventory
from neolib.http.browser.BrowserCookies import BrowserCookies
from neolib.http.CookieJar import CookieJar
from neolib.shop.UserShop import UserShop
from neolib.config.Config import Config
from neolib.http.Page import Page
from neolib.user.Bank import Bank
from neolib.user.hooks import *
from neolib.user.Pet import Pet
from neolib.user.SDB import SDB
import logging

class User:
    username = ""
    password = ""
    
    cookieJar = None
    
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
    
    def __init__(self, username, password, pin=None):
        # Neopets automatically converts all capitals in a username to lowercase
        self.username = username.lower()
        self.password = password
        self.pin = pin
        
        # Default hooks
        self.hooks = []
        self.hooks.append(updateNPs)
        self.hooks.append(updatePet)
        self.hooks.append(autoLogin)
        
    def login(self):
        data = "username=" + self.username + "&password=" + self.password + "&destination=/index.phtml"
        pg = self.getPage("http://www.neopets.com/login.phtml", {'username': self.username, 'password': self.password, 'destination': '/index.phtml'})
        self.cookieJar = pg.cookies
        
        pg = self.getPage("http://www.neopets.com/index.phtml")
        
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
    
    def loadConfig(self):
        self.config = Config(self.username)
        
        # A lack of data indicates the user configuration file didn't exist
        if not self.config.data:
            data = {'useHooks': 'True', 
                    'autoLogin': 'True',
                    'browserSync': 'False'} # Default configuration options
            self.config = Config.createUserConfig(self.username, data)
    
    def addHook(self, hook):
        self.hooks.append(hook)
        
    def setRandomEventCallback(self, cb):
        self.RECallback = cb
    
    def updateNps(self, pg = None):
        # If no page is supplied, just load the index
        if not pg:
            pg = self.getPage("http://www.neopets.com/index.phtml")
            
        self.nps = int( pg.find("a", id = "npanchor").text.replace(",", "") )
    
    def setProxy(self, host, port):
        self.proxy = (host, port)
    
    def syncWithBrowser(self, browser):
        BrowserCookies.loadBrowsers()
        if not browser in BrowserCookies.browsers:
                return False
        
        self.browserSync = True
        self.browser = browser
        return True
        
    def __syncCookies(self):
        if self.browserSync:  
            cj = BrowserCookies.getCookies(self.browser, ".neopets.com")
            if not cj:
                return False
                
            self.cookieJar = cj
            return True
        return False
        
    def __writeCookies(self):
        if self.browserSync:  
            cj = BrowserCookies.setCookies(self.browser, ".neopets.com", self.cookieJar)
    
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
        
        if self.browserSync:
            self.__syncCookies()
        
        pg = Page(url, self.cookieJar, postData, vars, self.proxy)
        self.cookieJar = pg.cookies
        
        if self.browserSync:
            self.__writeCookies()
        
        if pg.content.find("http://images.neopets.com/homepage/indexbak_oops_en.png") != -1:
            raise neopetsOfflineException
        
        if self.useHooks:
            for hook in self.hooks:
                self, pg = hook(self, pg)
        return pg        

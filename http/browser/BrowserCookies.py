""":mod:`BrowserCookies` -- Contains the BrowserCookies class

.. module:: BrowserCookies
   :synopsis: Contains the BrowserCookies class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

class BrowserCookies(object):
    
    """Provides an interface for retrieving browser cookies
    
    Provides functionality for detecting a browser, determining a browser's application
    data storage path, and querying a browser's cookie storage for any cookies associated
    with a given domain.
        
    Attributes:
       name (str) - Name to access browser with
       desc (str) - Readable name of the browser (I.E 'Google Chrome')
    """
    
    name = ""
    desc = ""
    
    browsers = {}
    
    @property
    def installed():
        pass
        
    @staticmethod
    def loadCookies(domain):
        pass
        
    @staticmethod
    def loadBrowsers():
        """ Loads all installed and supported browsers into BrowserCookies.browsers
        
        Loops through all classes that subclass BrowserCookies and checks the installed
        attribute. If the browser is installed, it's instance is loaded into
        BrowserCookies.browsers in the format of browsers[browser.name] = browser
        """
        for browser in BrowserCookies.__subclasses__():
            if browser.installed:
                BrowserCookies.browsers[browser.name] = browser
            
    @staticmethod
    def getCookies(browser, domain):
        """ Returns all stored cookies in the given browser using the given domain
        
        Returns:
           CookieeJar - All stored cookies
        """
        return BrowserCookies.browsers[browser].loadCookies(domain)
        
    @staticmethod
    def setCookies(browser, domain, cookieJar):
        """ Writes all given cookies to the given browser
        
        Returns:
           bool - True if successful, false otherwise
        """
        return BrowserCookies.browsers[browser].writeCookies(domain, cookieJar)
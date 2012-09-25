""":mod:`CookieJar` -- Contains the CookieJar class

.. module:: CookieJar
   :synopsis: Contains the CookieJar class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from Cookie import Cookie

class CookieJar:
    
    """Acts as storage for HTTP Cookies
    
    This class provides functionality for storing and obtaining
    HTTP cookies to be used in conjunction with HTTP requests
    
    Attributes
       cookies (dictionary) - All stored HTTP cookies stored as cookies[domain][cookiename]
    """
    
    cookies = None
    
    def __init__(self):
        self.cookies = {}
        
    def addCookies(self, domain, cookies):
        """ Adds a list of Cookie objects to the stored cookies
        
        Parameters:
           domain (str) - Domain cookies belong to
           cookies (list) - List of Cookie objects to add
        """
        if not domain in self.cookies:
                self.cookies[domain] = {}
        
        for cookie in cookies:
            self.cookies[domain][cookie.name] = cookie
            
    def addCookiesFromStr(self, cookies):
        """ Adds a list of raw cookie strings to the stored cookies
        
        Parameters:
           domain (str) - Domain cookies belong to
           cookies (list) - List of raw cookie strings
        """
        for cookie in cookies:
            tmpCookie = Cookie.cookieFromStr(cookie)
            
            if not tmpCookie.domain in self.cookies:
                self.cookies[tmpCookie.domain] = {}
            
            self.cookies[tmpCookie.domain][tmpCookie.name] = tmpCookie
    
    def getCookies(self, domain):
        """ Returns list of Cookie objects belonging to domain
           
        Returns
            list - List of Cookie objects
        """
        ret = []
        for cookie in self.cookies[domain]:
            if not self.cookies[domain][cookie].expired:
                ret.append(self.cookies[domain][cookie])
            
        return ret
    
    @staticmethod
    def cookiesToStr(cookies):
        """ Concats all associated cookies into a string, returns formatted string
        
        Parameters:
           cookies (list) - List of Cookie objects to concat
        """
        strCookies = []
        for cookie in cookies:
            strCookies.append(str(cookie))
            
        return ";".join(strCookies)
        
    def __getitem__(self, key):
        return self.cookies[key]
        
    def __setitem__(self, key, value):
        self.cookies[key] = value
        
    def __delitem__(self, key):
        self.cookies.pop(key)
        
    def __contains__(self, key):
        if key in self.cookies:
            return True
        else:
            return False
            
    def __iter__(self):
        for domain in self.cookies:
            yield self.cookies[domain]
            
    def __len__(self):
        return len(self.cookies)
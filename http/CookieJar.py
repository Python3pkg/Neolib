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
       cookies (dictionary) - All stored HTTP cookies
    """
    
    cookies = {}
    
    def getCookies(self):
        """ Returns all cookies in a formatted string to be used in a HTTP Request Header
        
        Loops through all stored cookies, ensuring no expired cookies are included in the
        returned string, and requests a string format of each cookie and compiles it to one
        string such that the returned string looks like "name=value;name=value;"
           
        Returns
           str - Formatted cookie string
        """
        cookieStr = ""
        
        # name=value;name=value; format
        for cookieName in self.cookies:
            if not self.cookies[cookieName].isExpired():
                cookieStr += self.cookies[cookieName].toStr()
        return cookieStr
        
    def addCookies(self, cookies):
        """ Adds a list of Cookie objects to the stored cookies
        
        Parameters
           cookies (list) - List of Cookie objects
        """
        for cookie in cookies:
            self.cookies[cookie.name] = cookie
        
    def addCookiesFromStr(self, strCookies):
        """ Adds a list of raw cookie strings to the stored cookies
        
        Parameters
           cookies (list) - List of raw cookie strings
        """
        for strCookie in strCookies:
            cookie = Cookie(strCookie)
            self.cookies[cookie.name] = cookie
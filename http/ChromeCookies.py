""":mod:`ChromeCookies` -- Contains the ChromeCookies class

.. module:: ChromeCookies
   :synopsis: Contains the ChromeCookies class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.http.CookieJar import CookieJar
from neolib.http.Cookie import Cookie
from sqlite3 import dbapi2 as sqlite
import os
import datetime

class ChromeCookies:
    
    """Provides an interface for retrieving stored Neopets cookies from Google Chrome
    
    Provides functionality for detecting Google Chrome, determining Chrome's application
    data storage path, and querying Chrome's cookies DB for any cookies associated with
    Neopets. 
    """
    
    @staticmethod
    def isChromeInstalled():
        """ Returns whether or not Cookie Chrome is installed
        
        Determines the application data path for Google Chrome
        and checks if the path exists. If so, returns True, otherwise
        it will return False.
           
        Returns
           bool - True if Chrome is installed
        """
        try:
            path = ChromeCookies._getPath()
            with open(path) as f: pass
                
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def loadChromeCookies(usr):
        """ Loads all Neopets cookie stored by Google Chrome into the specified User object
        
        Determines the application data path for Google Chrome, finds the cookie database file,
        queries it for cookies with domain neopets.com, and proceeds to build a CookieJar with
        the associated data and assigns the CookieJar to the given User.
        
        Parameters
           usr (User) - User to assign cookies to
           
        Returns
           usr or bool - If failed, returns False, otherwise returns modified User object
        """
        try:
            path = ChromeCookies._getPath()
            cursor = sqlite.connect(path, timeout=0.1).cursor()
            cursor.execute("select name, value from cookies WHERE host_key='.neopets.com'")
            results = cursor.fetchall()
            
            cookies = []
            expire = datetime.datetime.now() + datetime.timedelta(365)
            for result in results:
                cookies.append(Cookie(name=result[0], value=result[1], expires=expire))
            
            cj = CookieJar()
            cj.addCookies(cookies)
        
            usr.cookieJar = cj
        
            return usr
        except Exception as e:
            print e
            return False
        
    @staticmethod
    def _getPath():
        """ Returns Chrome's cookie database path
           
        Returns
           str - Google Chrome's cookie database path
        """
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        path = _winreg.QueryValueEx(key, 'Local AppData')[0]
        path = os.path.join(path, 'Google\\Chrome\\User Data\\Default\\Cookies')
        
        return path
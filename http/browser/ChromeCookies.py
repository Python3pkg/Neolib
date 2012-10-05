""":mod:`ChromeCookies` -- Contains the ChromeCookies class

.. module:: ChromeCookies
   :synopsis: Contains the ChromeCookies class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from sqlite3 import dbapi2 as sqlite
from neolib.http.browser.BrowserCookies import BrowserCookies
import datetime
import requests
import calendar
import logging
import time
import pytz
import os

class ChromeCookies(BrowserCookies):
    
    """Provides an interface for retrieving stored Neopets cookies from Google Chrome
    
    Provides functionality for detecting Google Chrome, determining Chrome's application
    data storage path, and querying Chrome's cookies DB for any cookies associated with
    Neopets.
    
    Attributes:
       name (str) - Name to access browser with
       desc (str) - Readable name of the browser (I.E 'Google Chrome')
    """
    
    name = "CHROME"
    desc = "Google Chrome"
    
    @property
    def installed():
        """ Returns whether or not Google Chrome is installed
        
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
    def loadCookies(domain):
        """ Loads all Neopets cookie stored by Google Chrome into a CookieJar
        
        Determines the application data path for Google Chrome, finds the cookie database file,
        queries it for cookies with domain neopets.com, and proceeds to build a CookieJar with
        the associated data.
        
        Parameters
           domain (str) - Domain to search for cookies with
           
        Returns
           CookieJar or bool - If failed, returns False, otherwise returns CookieJar
        """
        try:
            cj = requests.cookies.RequestsCookieJar()
            path = ChromeCookies._getPath()
            results = []
            with sqlite.connect(path, timeout=0.1) as conn:
                cursor = conn.cursor()
                cursor.execute("select name, value, path, expires_utc from cookies WHERE host_key='" + domain + "'")
                results = cursor.fetchall()
            
            if not results:
                raise noCookiesForDomain
            
            for result in results:
                if not result[3]:
                    expire = datetime.datetime.now() + datetime.timedelta(365)
                else:
                    epoch = datetime.datetime(1601, 1, 1)
                    expire = epoch + datetime.timedelta(microseconds=result[3])
                
                expire = calendar.timegm(expire.utctimetuple())
                cargs = {'expires': expire, 'domain': domain, 'path': result[2]}
                cj.set(result[0], result[1], **cargs)
        
            return cj
        except Exception as e:
            logging.getLogger("neolib.http").exception("Failed to load Google Chrome cookies")
            return False
    
    @staticmethod
    def writeCookies(domain, cookieJar):
        try:
            path = ChromeCookies._getPath()
            with sqlite.connect(path, timeout=3.0) as conn:
                cursor = conn.cursor()
                cursor.execute("delete from cookies where host_key='" + domain + "'")
                
                for cookie in cookieJar.getCookies(domain):
                    now = int(round(time.time(), 0)) * 10000000
                    expires = int(time.mktime(datetime.datetime.utcfromtimestamp(cookie.expires).timetuple())) * 10000000
                    sql = "insert into cookies (host_key, path, secure, expires_utc, name, value, last_access_utc, httponly) VALUES('%s','%s',0,%d,'%s','%s',%d,0)" % (domain, cookie.path, expires, cookie.name, cookie.value, now)
                    
                    cursor.execute(sql)
                
                conn.commit()
            return True
        except Exception as e:
            return False
            
    @staticmethod
    def _getPath():
        """ Returns Chrome's cookie database path
           
        Returns
           str - Google Chrome's cookie database path
        """
        
        if os.name == "posix":
            path = os.getenv("HOME") + "/.config/google-chrome/Default/Cookies"
            return path
        
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        path = _winreg.QueryValueEx(key, 'Local AppData')[0]
        path = os.path.join(path, 'Google\\Chrome\\User Data\\Default\\Cookies')
        
        return path

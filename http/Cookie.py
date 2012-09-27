""":mod:`Cookie` -- Contains the Cookie class

.. module:: Cookie
   :synopsis: Contains the Cookie class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from datetime import datetime
import logging
import pytz
import re

class Cookie:
    
    """Objectifies a HTTP Cookie
    
    This class provides a basic interface which resembles a HTTP Cookie.
    
    Attributes
       name (str) - Cookie name
       value (str) - Cookie Value
       expires (datetime) - Cookie expiration date
       expired (bool) - Whether or not cookie is expired
       path (str) - Cookie path
       domain (str) - Cookie's domain
        
    Initialization
       Cookie(self, name, value, expires, domain, path):
       
       Initializes the Cookie object with given parameters 
       
       Parameters
          name (str) - Cookie name
          value (str) - Cookie value
          expires (datetime) - Cookie expiration date
          domain (str) - Cookie's domain
          path (str) - Cookie's path
    """
    
    name = ""
    value = ""
    expires = None
    domain = ""
    path = ""
    
    def __init__(self, name, value, expires, domain, path):
        if not isinstance(expires, datetime):
            raise TypeError("Invalid cookie expiration")
        
        self.name = name
        self.value = value
        self.expires = expires
        self.domain = domain
        self.path = path
        
    @staticmethod
    def cookieFromStr(cookieStr):
        """ Parses a raw cookie string, returns a Cookie object representing the string
        
        Parameters:
           cookieStr (str) - Raw cookie string
           
        Returns:
           Cookie - Cookie object representing the string
           
        Raises:
           Exception
        """
        # Small addition to simplify parsing
        cookieStr += "\r"
        
        try:
            mat = re.match("(.*)=(.*); expires=(.*); path=(.*); domain=(.*?)\r", cookieStr)
            expires = datetime.strptime(mat.group(3), "%a, %d-%b-%Y %H:%M:%S %Z")
            
            return Cookie(mat.group(1), mat.group(2), expires, mat.group(5), mat.group(4))
        except Exception:
            logging.getLogger("neolib").exception("Failed to parse cookie string: " + cookieStr)
            raise Exception("Failed to parse HTTP cookie from string")
            
    @property
    def expired(self):
        if not self.expires.tzinfo:
            if datetime.now() < self.expires:
                return False
            else:
                return True
        else:
            if datetime.now().replace(tzinfo=pytz.UTC) < self.expires:
                return False
            else:
                return True
            
    def __str__(self):
        return "=".join([self.name, self.value])

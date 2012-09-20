""":mod:`Cookie` -- Contains the Cookie class

.. module:: Cookie
   :synopsis: Contains the Cookie class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from datetime import datetime
import logging
import re

class Cookie:
    
    """Objectifies a HTTP Cookie
    
    This class provides a basic interface which resembles a HTTP Cookie.
    
    Attributes
       name (str) - Cookie name
       value (str) - Cookie Value
       expires (datetime) - Cookie expiration date
       path (str) - Cookie path
       domain (str) - Cookie's domain
        
    Initialization
       HTTPRequestHeader(self, cookieStr = "", name="", value="", expires=None):
       
       Receives a raw cookie string and parses its contents or receives cookie
       details and sets itself appropriately. 
       
       Parameters
          cookieStr (str) - Raw cookie string from a HTTP Response Header
          name (str) - Cookie name
          value (str) - Cookie value
          expires (datetime) - Cookie expiration date
          
       Raises
          Exception
    """
    
    name = ""
    value = ""
    expires = ""
    path = ""
    domain = ""
    
    def __init__(self, cookieStr = "", name="", value="", expires=None):
        if name and value and expires:
            self.name = name
            self.value = value
            self.expires = expires
            return
        
        # Small addition to simplify parsing
        cookieStr += "\r"
        
        try:
            mat = re.match("(.*)=(.*); expires=(.*); path=(.*); domain=(.*?)\r", cookieStr)
            
            self.name = mat.group(1)
            self.value = mat.group(2)
            self.expires = datetime.strptime(mat.group(3), "%a, %d-%b-%Y %H:%M:%S %Z")
            self.path = mat.group(4)
            self.domain = mat.group(5)
        except Exception:
            logging.getLogger("neolib").exception("Failed to parse cookie string: " + cookieStr)
        
    def isExpired(self):
        """ Compares cookie expiration date to now, returns if cookie is expired
           
        Returns
           bool - True if cookie is expired
        """
        # Compare the cookie expiration date to now and determine if it's expired
        if datetime.now() < self.expires:
            return False
        else:
            return True
    
    def toStr(self):
        """ Returns a string representation of the cookie
           
        Returns
           str - Cookie string ("name-value;")
        """
        return self.name + "=" + self.value + ";"
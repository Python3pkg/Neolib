from datetime import datetime
import logging
import re

class Cookie:
    # Cookie name
    name = ""
    
    # Cookie value
    value = ""
    
    # Cookie expiration date
    expires = ""
    
    # Cookie path
    path = ""
    
    # Cookie's associated domain
    domain = ""
    
    def __init__(self, cookieStr):
        # Small addition to simplify parsing
        cookieStr += "\r"
        
        try:
            # Parse out the necessary information from the cookie string
            mat = re.match("(.*)=(.*); expires=(.*); path=(.*); domain=(.*?)\r", cookieStr)
        
            # Update the cookie data
            self.name = mat.group(1)
            self.value = mat.group(2)
            self.expires = mat.group(3)
            self.path = mat.group(4)
            self.domain = mat.group(5)
        except Exception:
            logging.getLogger("neolib").exception("Failed to parse cookie string: " + cookieStr)
        
    def isExpired(self):
        # Compare the cookie expiration date to now and determine if it's expired
        if datetime.now() < datetime.strptime(self.expires, "%a, %d-%b-%Y %H:%M:%S %Z"):
            return False
        else:
            return True
    
    def toStr(self):
        # Return's the cookie's string value, which is a simple name=value format
        return self.name + "=" + self.value + ";"
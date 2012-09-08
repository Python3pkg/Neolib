import re
import logging

class HTTPResponseHeader:
    
    # Raw HTTP Response Header content
    content = ""
    
    # HTTP Response Header variables in a dictionary format
    vars = {}
    
    # All raw cookie strings
    cookies = []
    
    
    # The HTTP version included with the response
    HTTPVer = ""
    
    # The HTTP status code
    statusCode = ""
    
    # The associated status code message
    statusMessage = ""
    
    
    def __init__(self, respHeader):
        # Set the header content
        self.content = respHeader
        
        try:
            # First get the version, status code, and status message
            mat = re.match("HTTP/(.*) (.*) (.*)", self.content)
            self.HTTPVer = mat.group(1)
            self.statusCode = mat.group(2)
            self.statusMessage = mat.group(3)
        
            # Then grab the cookies
            self.cookies = re.findall(r"Set-Cookie: (?P<value>.*?)\r\n", self.content)
        
            # Finally grab the rest of the variables
            self.vars = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", self.content))
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to parse HTTP headers: " + self.content)
            raise Exception
            
            
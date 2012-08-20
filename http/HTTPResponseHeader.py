import StringIO
import re
import logging

class HTTPResponseHeader:
    
    respContent = ""
    respVars = {}
    cookies = []
    
    HTTPVer = ""
    statusCode = ""
    statusMessage = ""
    
    
    def __init__(self, respHeader):
        self.respContent = respHeader
        respHeader = StringIO.StringIO(respHeader)
        
        try:
            # First get the version, status code, and status message
            mat = re.match("HTTP/(.*) (.*) (.*)", self.respContent)
            self.HTTPVer = mat.group(1)
            self.statusCode = mat.group(2)
            self.statusMessage = mat.group(3)
        
            # Then grab the cookies
            self.cookies = re.findall(r"Set-Cookie: (?P<value>.*?)\r\n", self.respContent)
        
            # Finally grab the rest of the variables
            self.respVars = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", self.respContent))
        except Exception:
            logging.getLogger("neolib").exception("Failed to parse HTTP headers: " + self.respContent)
            raise Exception
            
            
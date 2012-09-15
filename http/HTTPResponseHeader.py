import re
import logging

class HTTPResponseHeader:
    content = ""
    vars = {}
    cookies = []
    
    HTTPVer = ""
    statusCode = ""
    statusMessage = ""
    
    def __init__(self, respHeader):
        self.content = respHeader
        
        try:
            mat = re.match("HTTP/(.*) (.*) (.*)", self.content)
            self.HTTPVer = mat.group(1)
            self.statusCode = mat.group(2)
            self.statusMessage = mat.group(3)
            
            self.cookies = re.findall(r"Set-Cookie: (?P<value>.*?)\r\n", self.content)
            self.vars = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", self.content))
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to parse HTTP headers: " + self.content)
            raise Exception
            
            
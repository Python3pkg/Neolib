from HTTPWrapper import HTTPWrapper
from neolib.exceptions import HTTPException
from neolib.bs4 import BeautifulSoup

class Page:
    _wrapper = None
    _parser = None
    
    cookies = None
    reqHeader = None    
    header = None
    content = ""
    
    success = False
    
    images = None
    
    def __init__(self, url, cookies = None, postData = None, vars = None):
        # Set own instance of HTTPWrapper
        if not self._wrapper:
            self._wrapper = HTTPWrapper()
            
            # Set any cookies provided
            if cookies:
                self._wrapper.cookieJar = cookies
            
            # Determine type of request based on whether or not post data was provided
            if postData:
                type = "POST"
            else:
                type = "GET"
            
            # Make the request
            try:
                self.content = self._wrapper.request(type, url, postData, vars)
            except HTTPException:
                self.success = False
                self.content = None
                return
            
            # Set the response header
            self.header = self._wrapper.respHeader
            
            # Set the request header
            self.reqHeader = self._wrapper.reqHeader
            
            # Set any updated cookies
            self.cookies = self._wrapper.cookieJar
            
            # Set the parser
            self._parser = BeautifulSoup(self.content)
    
    def getParser(self):
        return self._parser
    
    def imageToFile(self, url, localfile):   
        # Download and save the image
        return self._wrapper.downloadFile("GET", url, localfile, binary = True)

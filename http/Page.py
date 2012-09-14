from neolib.exceptions import HTTPException
from HTTPWrapper import HTTPWrapper
from bs4 import BeautifulSoup

class Page:
    _wrapper = None
    _parser = None
    
    cookies = None
    reqHeader = None    
    header = None
    content = ""
    
    
    url = ""
    intCookies = None
    postData = None
    vars = None
    
    def __init__(self, url, cookies=None, postData=None, vars=None, proxy=None):
        if not self._wrapper:
            self._wrapper = HTTPWrapper()
            
        self.url = url
        self.intCookies = cookies
        self.postData = postData
        self.vars = vars
        
        if cookies:
            self._wrapper.cookieJar = cookies
            
        # Assume request type POST if postData is present
        if postData:
            type = "POST"
        else:
            type = "GET"
            
        try:
            # Better to decode UTF-8, or else you get decoding errors on some pages with special characters
            self.content = self._wrapper.request(type, url, postData, vars, proxy).decode('utf-8')
        except HTTPException:
            self.content = None
            return
        
        self.header = self._wrapper.respHeader
        self.reqHeader = self._wrapper.reqHeader
        self.cookies = self._wrapper.cookieJar
        self._parser = BeautifulSoup(self.content, "lxml")
    
    def getParser(self):
        return self._parser
    
    def imageToFile(self, url, localfile):   
        # Failure to set binary to true will most likely cause a corrupted image file
        return self._wrapper.downloadFile("GET", url, localfile, binary = True)
        
    def __bool__(self):
        return self.content

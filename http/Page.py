from neolib.exceptions import HTTPException
from HTTPWrapper import HTTPWrapper
from bs4 import BeautifulSoup

class Page:
    # Instance of HTTPWrapper
    _wrapper = None
    
    # Instance of BeautifulSoup
    _parser = None
    
    
    # Associated CookieJar instance
    cookies = None
    
    # Associated HTTPRequestHeader instance
    reqHeader = None    
    
    # Associated HTTPResponseHeader instance 
    header = None
    
    # Content of the page
    content = ""
    
    
    # URL page was intialized with
    url = ""
    
    # CookieJar page was intialized with
    intCookies = None
    
    # postData the page was initialized with
    postData = None
    
    # HTTP Request variables page was initialized with
    vars = None
    
    
    # Whether the page loaded successfully
    success = False
    
    def __init__(self, url, cookies = None, postData = None, vars = None, proxy = None):
        # Set own instance of HTTPWrapper
        if not self._wrapper:
            self._wrapper = HTTPWrapper()
            
        # Store parameters for reference purposes
        self.url = url
        self.intCookies = cookies
        self.postData = postData
        self.vars = vars
            
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
            self.content = self._wrapper.request(type, url, postData, vars, proxy)
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
        self._parser = BeautifulSoup(self.content, "lxml")
    
    def getParser(self):
        return self._parser
    
    def imageToFile(self, url, localfile):   
        # Download and save the image
        return self._wrapper.downloadFile("GET", url, localfile, binary = True)

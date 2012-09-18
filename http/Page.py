""":mod:`Page` -- Contains the Page class

.. module:: Page
   :synopsis: Contains the Page class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import HTTPException
from HTTPWrapper import HTTPWrapper
from bs4 import BeautifulSoup

class Page(BeautifulSoup):
    
    """Represents an HTML web page
    
    Uses an instance of HTTPWrapper to request a remote doucment and uses processed data
    to wrap itself with. Subclasses BeautifulSoup to allow for easy page exploration. This
    class is the main means for communicating with Neopets, and should be used over
    HTTPWrapper and it's associated classes.
    
    Attributes
       cookies (CookieJar) -- Page cookies
       reqHeader (HTTPRequestHeader) -- Represents the request header page was sent with
       header (HTTPResponseHeader) -- Page HTTP Response Header
       content (str) -- Page's HTML content
       url (str) -- URL of Page
       intCookies (CookieJar) -- Cookies Page was initialized with
       postData(dict) -- POST data Page was initialized with
       vars (dict) -- Additional HTTP Request Header variables Page was intiialized with
       
    Initialization
       Page(url, cookies=None, postData=None, vars=None, proxy=None)
       
       Requests a remote document and initializes Page with the data
       
       Initiates it's own instance of HTTPWrapper and requests a remote document using the
       given parameters. Uses the received content to load basic page details and initiate
       the parent class, BeautifulSoup. 
       
       Parameters
          url (str) -- Remote URL address of the page
          cookies (CookieJar) -- Cookies sent with HTTP Request
          postData (dict) -- POST data {name: 'value'} sent with HTTP Request
          vars (dict) -- HTTP Request variables {name: 'value'} sent with HTTP Request
          proxy (tuple) -- Proxy host and port to connect with
          
       Raises
          HTTPException
        
    Example
       >>> pg = Page("http://www.neopets.com/index.phtml")
       >>> pg.content
       <!DOCTYPE HTML PUBLIC> .....
       >>> pg.a
       <a href="http://www.petpetpark.com/">petpet park</a>
    """
    
    _wrapper = None
    
    cookies = None
    reqHeader = None    
    header = None
    content = ""
    
    url = ""
    intCookies = None
    postData = None
    vars = None
    
    def __init__(self, url, cookies=None, postData=None, vars=None, proxy=None):
        """ Requests a remote document and initializes Page with the data
        
        Initiates it's own instance of HTTPWrapper and requests a remote document using the
        given parameters. Uses the received content to load basic page details and initiate
        the parent class, BeautifulSoup. 
        """
        
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
            
        # Decode UTF-8 or else you get decoding errors on some pages with special characters
        self.content = self._wrapper.request(type, url, postData, vars, proxy).decode('utf-8')
        
        self.header = self._wrapper.respHeader
        self.reqHeader = self._wrapper.reqHeader
        self.cookies = self._wrapper.cookieJar
        
        BeautifulSoup.__init__(self, self.content)
    
    def imageToFile(self, url, localfile):
        """ Downloads an image to a local file, returns if it was sucessful or not
        
        Uses instance of HTTPWrapper to request a remote file and save it's contents to a
        local file. 
        
        Parameters
           url (str) -- Remote URL address
           localfile (str) -- Local file path to save image
           
        Returns
           bool - True if successful, False otherwise
           
        Raises
           HTTPException
        """
        # Failure to set binary to true will most likely cause a corrupted image file
        return self._wrapper.downloadFile("GET", url, localfile, binary = True)
        
    def __bool__(self):
        return self.content

""":mod:`Page` -- Provides an interface for HTTP communicating and HTML parsing

.. module:: Page
   :synopsis: Provides an interface for HTTP communicating and HTML parsing
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.http.HTTPForm import HTTPForm
from bs4 import BeautifulSoup
import requests

class Page(BeautifulSoup):
    
    """Represents an HTML web page
    
    Provides an interface for handling an HTTP web page by subclassing the popular
    HTML parsing library, BeautifulSoup, to allow for easy page exploration and utilizing
    the Requests library for handling HTTP requests. This class aims to intertwine both
    popular libraries to create one accessible class. 
    
    Attributes
       resp (Response) -- A Requests Response object representing the HTTP Response
       request (Request) -- A Requests Request object representing the HTTP Request
       header (dict) -- All HTTP Response Header Variables
       content (str) -- Page content
       url (str) -- Page URL
       postData(dict) -- POST data Page was initialized with
       vars (dict) -- Additional HTTP Request Header variables Page was intiialized with
       usr (User) -- User that initialized the page
       
    Initialization
       Page(url, usr=None, session=None, postData=None, vars=None, proxy=None)
       
       Requests a remote document and initializes Page with the data
       
       Either uses the supplied Requests session or uses a new Requests session to request
       a remote document using the given parameters. Uses the received content to load basic
       page details and initiate the parent class, BeautifulSoup. 
       
       Parameters
          url (str) -- Remote URL address of the page
          usr (User) -- Optional user to initiate the page with
          session (request-client) -- Requests session to use with making the request
          postData (dict) -- POST data {name: 'value'} sent with HTTP Request
          vars (dict) -- HTTP Request variables {name: 'value'} sent with HTTP Request
          proxy (tuple) -- Proxy host and port to connect with
        
    Example
       >>> pg = Page("http://www.neopets.com/index.phtml")
       >>> pg.content
       <!DOCTYPE HTML PUBLIC> .....
       >>> pg.a
       <a href="http://www.petpetpark.com/">petpet park</a>
    """
    
    _wrapper = None
    
    resp = None
    request = None
    header = None
    content = ""
    
    url = ""
    postData = None
    vars = None
    
    usr = None
    
    _defaultVars = {"USER-AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                   "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "ACCEPT-LANGUAGE": "en-us,en;q=0.5"}
    
    def __init__(self, url, usr=None, session=None, postData=None, vars=None, proxy=None):
        self.url = url
        self.postData = postData
        self.vars = vars
        
        if not session and not usr:
            if postData:
                r = requests.post(url, data=postData, headers=vars, proxies=proxy)
            else:
                r = requests.get(url, headers=vars, proxies=proxy)
        elif usr:
            if postData:
                r = usr.session.post(url, data=postData, headers=vars, proxies=proxy)
            else:
                r = usr.session.get(url, headers=vars, proxies=proxy)
        elif session:
            if postData:
                r = session.post(url, data=postData, headers=vars, proxies=proxy)
            else:
                r = session.get(url, headers=vars, proxies=proxy)
        
        self.resp = r
        self.request = r.request
        self.header = r.headers
        self.content = r.text
        self.usr = usr
        
        if "text/html" in r.headers['content-type']:
            BeautifulSoup.__init__(self, r.content)
        else:
            self.content = r.content
        
    def form(self, usr=None, **kwargs):
        """ Returns an HTTPForm that matches the given criteria
        
        Searches for an HTML form in the page's content matching the criteria
        specified in kwargs. If a form is found, returns an HTTPForm instance
        that represents the form.
           
        Parameters:
           usr (User) -- User to associate with the form (used in HTTPForm.submit()
           **kwargs (dict) -- Data to search for the form with (I.E action='blah.phtml')
           
        Returns
           HTTPForm - Represents the HTML form
        """
        if self.usr: usr = self.usr
        if self.find("form", kwargs):
            return HTTPForm(usr, self.url, self.find("form", kwargs))
    
    @staticmethod
    def newSession():
        """ Returns a new Requests session with pre-loaded default HTTP Headers
        
        Generates a new Requests session and consults with the Configuration class
        to determine if a Configuration exists and attempts to use the configured
        HTTP Request headers first. If this fails, it attempts to create a new
        default configuration and use those values. Finally, if a configuration
        cannot be initiaized it uses the hard-coded Mozilla headers.
           
        Returns
           request-client - The configured Requests session
           
        Raises
           HTTPException
        """
        from neolib.config.Configuration import Configuration
        
        s = requests.session()
        if not Configuration.loaded():
            if not Configuration.initialize():
                s.headers.update(Page._defaultVars)
            else:
                s.headers.update(Configuration.getConfig().core.HTTPHeaders.toDict())
        else:
            s.headers.update(Configuration.getConfig().core.HTTPHeaders.toDict())
        
        return requests.session()

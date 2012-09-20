""":mod:`HTTPRequestHeader` -- Contains the HTTPRequestHeader class

.. module:: HTTPRequestHeader
   :synopsis: Contains the HTTPRequestHeader class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.config.Config import Config
from urlparse import urlparse
from textwrap import dedent
import HTTPResponseHeader
import logging
import urllib
import json
import os

class HTTPRequestHeader:
    
    """Objectifies a HTTP Request Header
    
    This class wraps a HTTP Request Header by providing functionality to create
    and properly format a standard compliant HTTP Request Header.
    
    Attributes
       content (str) - Raw HTTP Request Header content
       vars (dict) - All HTTP Request variables
        
    Initialization
       HTTPRequestHeader(type, host, document, cookies="", postData=None, vars=None, proxyURL=None):
       
       Builds a compliant HTTP Request Header and stores it in HTTPRequestHeader.content
       
       Takes the given parameters and formats them into a compliant HTTPRequestHeader.
       Note the POST data and additional variables are given as a dictionary in the
       format of {'name': 'value'}. The class will convert these dictionaries into
       their proper string equivalents in initialization. 
       
       Parameters
          type (str) - Type of HTTP Request (GET or POST)
          host (str) - Remote host URL
          document (str) - Remote document to request
          cookies (str) - Cookies to be attached with the request
          postData (dict) - Post DATA to be sent with the request
          vars (dict) - Additional HTTP Request variables to add or override
          proxyURL (str) - Full URL to the remote document
          
       Raises
          Exception
    """
    
    content = ""
    vars = {}
    
    GET = "GET"
    POST = "POST"
    
    _defaultVars = {"HTTPVER": "1.1",
                   "USER-AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                   "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "ACCEPT-LANGUAGE": "en-us,en;q=0.5",
                   "ACCEPT-ENCODING": "gzip, deflate",
                   "CONNECTION": "close"}
    
    def __init__(self, type, host, document, cookies="", postData=None, vars=None, proxyURL=None):
        if not (type == self.GET or type == self.POST):
            logging.getLogger("neolib.http").info("Invalid request header type given: " + type)
            raise Exception
        
        if not Config.getGlobal():
            # Set Firefox as the default
            self.vars = self._defaultVars
        else:
            # Ensure the setting actually exists
            if 'HTTPHEADER' in Config.getGlobal():
                self.vars = Config.getGlobal()['HTTPHEADER']
            else:
                # Set Firefox as the default
                self.vars = self._defaultVars
        
        # Updates default loaded variables with any user added variables
        if vars:
            self.vars.update(vars)
        
        # The full URL must be provided when connecting via a proxy
        if proxyURL:
            document = proxyURL
        
        self.content = """\
            %s %s HTTP/%s
            Host: %s
            User-Agent: %s
            Accept: %s
            Accept-Language: %s
            Accept-Encoding: %s
            Connection: %s""" % \
            (type, document, self.vars['HTTPVER'], host, self.vars['USER-AGENT'], self.vars['ACCEPT'], self.vars['ACCEPT-LANGUAGE'], self.vars['ACCEPT-ENCODING'], self.vars['CONNECTION'])
        
        # Remove above indentations
        self.content = dedent(self.content)
        
        if cookies:
            self.content += "\nCookie: " + cookies
        
        if "Referer" in self.vars:
            self.content += "\nReferer: " + self.vars['Referer']
        
        strData = ""
        if type == self.POST:
            # Ensure the data is URL encoded to ensure proper transmission
            # This method will also convert the dictionary into it's proper string format
            strData = urllib.urlencode(postData)
            
            self.content += "\nContent-Type: application/x-www-form-urlencoded"
            self.content += "\nContent-Length: " + str(len(strData))
        
        # Two return lines are expected at the end of each HTTP Request
        self.content += "\r\n\r\n"
        
        if type == self.POST:
            self.content += strData
        
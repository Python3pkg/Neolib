""":mod:`HTTPResponseHeader` -- Contains the HTTPResponseHeader class

.. module:: HTTPResponseHeader
   :synopsis: Contains the HTTPResponseHeader class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

import re
import logging

class HTTPResponseHeader:
    
    """Objectifies a HTTP Response Header
    
    This class wraps a HTTP Response Header by providing functionality to parse
    its contents into logical segments upon initialization. These segments include
    the HTTP Version, response code and message, cookies, and HTTP Response variables
    
    Attributes
       content (str) - Raw HTTP Response Header content
       vars (dict) - All HTTP Response variables
       cookies (list) - All raw cookie strings
       HTTPVers (str) - HTTP Version
       statusCode (str) - Response status code
       statusMessage (str) - Response status message
        
    Initialization
       HTTPResponseHeader(respHeader)
       
       Parses a raw HTTP Request Header into it's logical segments
       
       Uses a set regular expression strings to parse a raw HTTP Response Header
       into it's HTTP version, status code, status message, cookies, and HTTP
       Response variables.
       
       Parameters
          respHeader (str) - Raw HTTP Response Header
          
       Raises
          Exception
    """
    
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
            
            
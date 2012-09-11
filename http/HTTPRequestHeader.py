from neolib.config.Config import Config
from urlparse import urlparse
from textwrap import dedent
import HTTPResponseHeader
import logging
import urllib
import json
import os

class HTTPRequestHeader:
    # All request header variables in a dictionary format
    vars = {}
    
    # The raw request header content
    content = ""
    
    GET = "GET"
    POST = "POST"
    
    def __init__(self, type, host, document, cookies = "", postData = None, vars = None, proxyURL = None):
        
        # Verify a proper type was specified
        if not (type == self.GET or type == self.POST):
            logging.getLogger("neolib.http").info("Invalid request header type given: " + type)
            raise Exception
        
        # Load the default header vars from the local JSON file
        path = os.path.dirname(os.path.abspath(HTTPResponseHeader.__file__)) + "/HTTPHeaders.json"
        loadedVars = json.loads( open( path).read() )
        
        # Check if a global config option is set
        if not Config.getGlobal():
            # Set Firefox as the default
            self.vars = loadedVars["Firefox"]
        else:
            # Ensure the setting actually exists
            if Config.getGlobal()['HTTPHeaderVer'] in loadedVars:
                self.vars = loadedVars[Config.getGlobal()['HTTPHeaderVer']]
            else:
                # Otherwise just set it to default Firefox
                self.vars = loadedVars["Firefox"]
        
        # Import any user appended variables
        if vars:
            self.vars.update(vars)
        
        # Setup the proxy
        if proxyURL:
            document = proxyURL
        
        # Construct the HTTP Request Header
        self.content = """\
            %s %s HTTP/%s
            Host: %s
            User-Agent: %s
            Accept: %s
            Accept-Language: %s
            Accept-Encoding: %s
            Connection: %s""" % \
            (type, document, self.vars['HTTPVER'], host, self.vars['USER-AGENT'], self.vars['ACCEPT'], self.vars['ACCEPT-LANGUAGE'], self.vars['ACCEPT-ENCODING'], self.vars['CONNECTION'])
        
        # Remove the indentations I made above
        self.content = dedent(self.content)
        
        # If cookies exist, add them
        if cookies:
            self.content += "\nCookie: " + cookies
        
        # If referer exists, add it
        if "Referer" in self.vars:
            self.content += "\nReferer: " + self.vars['Referer']
        
        # If it was a POST request, build the post data and append headers
        strData = ""
        if type == self.POST:
            # Ensure the data is encoded to prevent any issues
            # This method will also convert the dictionary into it's proper string format
            strData = urllib.urlencode(postData)
            
            self.content += "\nContent-Type: application/x-www-form-urlencoded"
            self.content += "\nContent-Length: " + str(len(strData))
        
        # Add the new lines at the end
        self.content += "\r\n\r\n"
        
        # If it was a POST, append the data
        if type == self.POST:
            self.content += strData
            
        # All done!
        
        
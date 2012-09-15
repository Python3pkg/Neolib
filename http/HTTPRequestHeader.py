from neolib.config.Config import Config
from urlparse import urlparse
from textwrap import dedent
import HTTPResponseHeader
import logging
import urllib
import json
import os

class HTTPRequestHeader:
    vars = {}
    content = ""
    
    GET = "GET"
    POST = "POST"
    
    def __init__(self, type, host, document, cookies = "", postData = None, vars = None, proxyURL = None):
        if not (type == self.GET or type == self.POST):
            logging.getLogger("neolib.http").info("Invalid request header type given: " + type)
            raise Exception
        
        # Load the default header vars from the local JSON file
        path = os.path.dirname(os.path.abspath(HTTPResponseHeader.__file__)) + "/HTTPHeaders.json"
        loadedVars = json.loads( open( path).read() )
        
        if not Config.getGlobal():
            # Set Firefox as the default
            self.vars = loadedVars["Firefox"]
        else:
            # Ensure the setting actually exists
            if Config.getGlobal()['HTTPHeaderVer'] in loadedVars:
                self.vars = loadedVars[Config.getGlobal()['HTTPHeaderVer']]
            else:
                # Set Firefox as the default
                self.vars = loadedVars["Firefox"]
        
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
        
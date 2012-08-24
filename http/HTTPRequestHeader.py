import json
import os
from urlparse import urlparse
from textwrap import dedent
import HTTPResponseHeader

class HTTPRequestHeader:
    headerVars = {}
    headerContent = ""
    
    GET = "GET"
    POST = "POST"
    
    def __init__(self, type, host, document, cookies = "", postData = None, vars = None):
        
        # Verify a proper type was specified
        if not (type == self.GET or type == self.POST):
            return # Insert future error handling
        
        # Load the default header vars from the local JSON file
        path = os.path.dirname(os.path.abspath(HTTPResponseHeader.__file__)) + "/HTTPHeaders.json"
        loadedVars = json.loads( open( path).read() )
        
        # Future compatibility, for now just sticking with Firefox
        self.headerVars = loadedVars["Firefox"]
        
        # Import any user appended variables
        if vars:
            self.headerVars.update(vars)
                    
        # Construct the HTTP Request Header
        self.headerContent = """\
            %s %s HTTP/%s
            Host: %s
            User-Agent: %s
            Accept: %s
            Accept-Language: %s
            Accept-Encoding: %s
            Connection: %s""" % \
            (type, document, self.headerVars['HTTPVER'], host, self.headerVars['USER-AGENT'], self.headerVars['ACCEPT'], self.headerVars['ACCEPT-LANGUAGE'], self.headerVars['ACCEPT-ENCODING'], self.headerVars['CONNECTION'])
        
        # Remove the indentations I made above
        self.headerContent = dedent(self.headerContent)
        
        # If cookies exist, add them
        if cookies:
            self.headerContent += "\nCookie: " + cookies
        
        # If referer exists, add it
        if "Referer" in self.headerVars:
            self.headerContent += "\nReferer: " + self.headerVars['Referer']
        
        # If it was a POST request, build the post data and append headers
        strData = ""
        if type == self.POST:
            for key in postData:
                strData += "=".join([key, postData[key]]) + "&"
            strData = strData[:-1]
            
            self.headerContent += "\nContent-Type: application/x-www-form-urlencoded"
            self.headerContent += "\nContent-Length: " + str(len(strData))
        
        # Add the new lines at the end
        self.headerContent += "\r\n\r\n"
        
        # If it was a POST, append the data
        if type == self.POST:
            self.headerContent += strData
            
        # All done!
        
        
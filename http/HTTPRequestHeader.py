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
    
    def __init__(self, type, host, document, cookies = "", postData = "", vars = None):
        
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
            for var in vars:
                self.headerVars[var] = vars[var]
                
        # Construct the HTTP Request Header
        self.headerContent = """\
            %s %s HTTP/%s
            Host: %s
            User-Agent: %s
            Accept: %s
            Accept-Language: %s
            Accept-Encoding: %s
            Connection: %s
            Cookie: %s""" % \
            (type, document, self.headerVars['HTTPVER'], host, self.headerVars['USER-AGENT'], self.headerVars['ACCEPT'], self.headerVars['ACCEPT-LANGUAGE'], self.headerVars['ACCEPT-ENCODING'], self.headerVars['CONNECTION'], cookies)
        
        # Remove the indentations I made above
        self.headerContent = dedent(self.headerContent)
        
        # If referer exists, add it
        if "Referer" in self.headerVars:
            self.headerContent += "\nReferer: " + self.headerVars['Referer']
        
        # Need to add content length and type if it was a POST
        if type == self.POST:
            self.headerContent += "\nContent-Type: application/x-www-form-urlencoded"
            self.headerContent += "\nContent-Length: " + str(len(postData))
        
        # Add the new lines at the end
        self.headerContent += "\r\n\r\n"
        
        # If it was a POST, append the data
        if type == self.POST:
            self.headerContent += postData
            
        # All done!
        
        
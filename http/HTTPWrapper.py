from HTTPRequestHeader import HTTPRequestHeader
from HTTPResponseHeader import HTTPResponseHeader
from urlparse import urlparse
from CookieJar import CookieJar
from Cookie import Cookie
from exceptions import HTTPException
import socket
import zlib
import logging

class HTTPWrapper:
    sock = None
    repHeader = None
    repContent = ""
    cookieJar = None
    
    timeout = 15.00
    
    _logger = None
    
    def __init__(self):
        # Setup a logger instance for debugging use
        if not self._logger:
            self._logger = logging.getLogger("neolib.http")
    
    def request(self, type, url, postData = None, vars = None):
        # Create a socket to use
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a 15 second timeout so operations won't hang
        s.settimeout(self.timeout)
        
        # Parse the URL to determine what exactly we're doing
        parsedUrl = urlparse(url)
            
        # Grab any cookies
        if self.cookieJar:
            cookies = self.cookieJar.getCookies()
        else:
            cookies = ""
        
        # Add a query if it exists
        if parsedUrl.query:
            document = parsedUrl.path + "?" + parsedUrl.query
        else:
            document = parsedUrl.path
        
        # Let's build a request header before connecting
        rHeader = HTTPRequestHeader(type, parsedUrl.netloc, document, cookies, postData, vars)
        
        # Now we can connect and send the request
        try:
            s.connect((parsedUrl.netloc, 80))
        except Exception:
            errMsg = "Failed to connect to host: %s on port 80" % parsedURL.netloc
            self._logger.exception(errMsg)
            raise HTTPException
            
        # Send the request
        s.sendall(rHeader.headerContent)
        
        # Now begin buffering the response
        # 4096 is a mid-sized buffer and is divisible by 2, thus making it an ideal choice
        try:
            data = ""
            while True:
                buff = s.recv(4096)
                
                if not buff:
                    break
                
                data += buff
        except socket.timeout:
            errMsg = "Connection timed-out while connecting to %s. Request headers were as follows: %s" % (parsedUrl.netloc, rHeader.headerContent)
            self._logger.exception(errMsg)
            raise HTTPException
            
        # Don't forget to close your sockets!
        s.close()
        
        # Split the response header and content
        header, content = data.split("\r\n\r\n")
        
        # Parse the headers for future usage
        try:
            self.repHeader = HTTPResponseHeader(header)
        except Exception:
            self._logger.exception("Failed to parse HTTP Response Header. Header content: " + header)
            raise HTTPException
        
        # Update cookies
        if not self.cookieJar:
            self.cookieJar = CookieJar(self.repHeader.cookies)
        else:
            self.cookieJar.addCookies(self.repHeader.cookies)
            
        # Check if the content is encoded
        if "Content-Encoding" in self.repHeader.respVars:
            # If the content is gzip encoded, decode it
            if self.repHeader.respVars['Content-Encoding'].find("gzip") != -1:
                self.repContent = zlib.decompress(content, 16+zlib.MAX_WBITS)
        else:
            self.repContent = content
            
        # Return the content       
        return self.repContent
        
    def downloadFile(self, type, url, localpath, cookies = None, postData = "", vars = None, binary = False):
        # Set any given cookies
        if cookies:
            self.cookieJar = cookies
            
        try:
            # Download the file
            fileData = self.request(type, url, postData, vars)
        
            # Determine which method to write with
            if binary:
                f = open(localpath, "wb")
            else:
                f = open(localpath, "w")
            
            # Write and close the file
            f.write(fileData)
            f.close
        except Exception:
            self._logger.exception("Failed to download file. File URL: " + url + ". Local path: " + localpath + "\nResponse Header:\n" + self.repHeader.respContent)
            return False
            
        return True
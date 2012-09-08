from neolib.exceptions import HTTPException
from HTTPResponseHeader import HTTPResponseHeader
from HTTPRequestHeader import HTTPRequestHeader
from CookieJar import CookieJar
from Cookie import Cookie
from urlparse import urlparse
import logging
import socket
import zlib

class HTTPWrapper:
    # Instance of a socket
    sock = None
    
    # The associated HTTPRequestHeader
    reqHeader = None
    
    # The associated HTTPResponseHeader
    respHeader = None
    
    # The request content returned with HTTPWrapper.request()
    respContent = ""
    
    # The associated CookieJar
    cookieJar = None
    
    
    # The time to wait for a server response prior to timing out
    timeout = 45.00
    
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
        self.reqHeader = HTTPRequestHeader(type, parsedUrl.netloc, document, cookies, postData, vars)
        
        # Now we can connect and send the request
        try:
            s.connect((parsedUrl.netloc, 80))
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to connect to host: %s on port 80" % parsedUrl.netloc)
            raise HTTPException
            
        # Send the request
        s.sendall(self.reqHeader.content)
        
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
            logging.getLogger("neolib.http").exception("Connection timed-out while connecting to %s. Request headers were as follows: %s" % (parsedUrl.netloc, self.reqHeader.content))
            raise HTTPException
            
        # Don't forget to close your sockets!
        s.close()
        
        # Split the response header and content
        header, content = data.split("\r\n\r\n")
        
        # Parse the headers for future usage
        try:
            self.respHeader = HTTPResponseHeader(header)
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to parse HTTP Response Header. Header content: " + header)
            raise HTTPException
        
        # Update cookies
        if not self.cookieJar:
            self.cookieJar = CookieJar(self.respHeader.cookies)
        else:
            self.cookieJar.addCookies(self.respHeader.cookies)
            
        # Check if the content is encoded
        if "Content-Encoding" in self.respHeader.vars:
            # If the content is gzip encoded, decode it
            if self.respHeader.vars['Content-Encoding'].find("gzip") != -1:
                self.respContent = zlib.decompress(content, 16+zlib.MAX_WBITS)
        else:
            self.respContent = content
            
        # Return the content       
        return self.respContent
        
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
            logging.getLogger("neolib.http").exception("Failed to download file. File URL: " + url + ". Local path: " + localpath + "\nResponse Header:\n" + self.repHeader.respContent)
            return False
            
        return True
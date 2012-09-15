from neolib.exceptions import HTTPException
from neolib.exceptions import invalidProxy
from HTTPResponseHeader import HTTPResponseHeader
from HTTPRequestHeader import HTTPRequestHeader
from CookieJar import CookieJar
from Cookie import Cookie
from urlparse import urlparse
import logging
import socket
import zlib

class HTTPWrapper:
    sock = None
    
    reqHeader = None
    respHeader = None
    respContent = ""
    cookieJar = None
    
    timeout = 45.00
    
    def request(self, type, url, postData=None, vars=None, proxy=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        
        parsedUrl = urlparse(url)
            
        # Convert any cookies to string form
        cookies = ""
        if self.cookieJar:
            cookies = self.cookieJar.getCookies()
        
        # Add a query if it exists
        document = parsedUrl.path
        if parsedUrl.query:
            document += "?" + parsedUrl.query
        
        # Necessary to send the entire URL to HTTPRequestHeader as 
        # it's required by the proxy host.
        proxyURL = ""
        if proxy:
            proxyURL = url
        
        # Builds a HTTP Request Header
        try:
            self.reqHeader = HTTPRequestHeader(type, parsedUrl.netloc, document, cookies, postData, vars, proxyURL)
        except Exception:
            raise HTTPException("Could not build HTTP Request Header")
        
        try:
            if proxy:
                s.connect(proxy)
            else:
                s.connect((parsedUrl.netloc, 80))
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to connect to host: %s on port 80" % parsedUrl.netloc)
            raise HTTPException("Could not connect to host")
            
        s.sendall(self.reqHeader.content)
        
        # Buffer the response
        # 4096 is a mid-sized buffer and is divisible by 2, thus making it an ideal choice.
        try:
            data = ""
            while True:
                buff = s.recv(4096)
                
                if not buff:
                    break
                
                data += buff
        except socket.timeout:
            logging.getLogger("neolib.http").exception("Connection timed-out while connecting to %s. Request headers were as follows: %s" % (parsedUrl.netloc, self.reqHeader.content))
            raise HTTPException("Connection timed out")
            
        s.close()
        
        # Split the response header and content
        header, content = data.split("\r\n\r\n")
        
        # Parse HTTP Response Header
        try:
            self.respHeader = HTTPResponseHeader(header)
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to parse HTTP Response Header. Header content: " + header)
            raise HTTPException("Invalid HTTP Response Header")
        
        # Update cookies to reflect this request
        if not self.cookieJar:
            self.cookieJar = CookieJar(self.respHeader.cookies)
        else:
            self.cookieJar.addCookies(self.respHeader.cookies)
            
        if "Content-Encoding" in self.respHeader.vars:
            if self.respHeader.vars['Content-Encoding'].find("gzip") != -1:
                try:
                    self.respContent = zlib.decompress(content, 16+zlib.MAX_WBITS)
                except Exception:
                    raise HTTPException("Invalid or malformed gzip data")
        else:
            self.respContent = content
                   
        return self.respContent
        
    def downloadFile(self, type, url, localpath, cookies=None, postData = "", vars=None, proxy=None, binary=False):
        if cookies:
            self.cookieJar = cookies
            
        try:
            # Request the remote file
            fileData = self.request(type, url, postData, vars, proxy)
        
            if binary:
                f = open(localpath, "wb")
            else:
                f = open(localpath, "w")
                
            f.write(fileData)
            f.close
        except Exception:
            logging.getLogger("neolib.http").exception("Failed to download file. File URL: " + url + ". Local path: " + localpath + "\nResponse Header:\n" + self.repHeader.respContent)
            return False
            
        return True
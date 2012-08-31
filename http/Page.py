from HTTPWrapper import HTTPWrapper
from neolib.RegexLib import RegexLib
from exceptions import HTTPException
import urlparse

class Page:
    wrapper = None
    cookies = None
    pageHeader = ""
    pageContent = ""
    success = False
    
    images = None
    
    def __init__(self, url, cookies = None, postData = None, vars = None):
        # Set own instance of HTTPWrapper
        if not self.wrapper:
            self.wrapper = HTTPWrapper()
            
            # Set any cookies provided
            if cookies:
                self.wrapper.cookieJar = cookies
            
            # Determine type of request based on whether or not post data was provided
            if postData:
                type = "POST"
            else:
                type = "GET"
            
            # Make the request
            try:
                self.pageContent = self.wrapper.request(type, url, postData, vars)
            except HTTPException:
                self.success = False
                self.pageContent = None
                return
            
            # Set the response header
            self.pageHeader = self.wrapper.repHeader
            
            # Set any updated cookies
            self.cookies = self.wrapper.cookieJar
    
    def loadImages(self):
        # Parse all images
        mats = RegexLib.getMat("page", "images", self.pageContent)
        
        # Ensure we actually have images
        self.images = {}
        if mats:
            # Loop through each image and assign in {'path': 'url'} format
            for mat in mats:
                path = urlparse.urlparse(mat).path
                self.images[path] = mat
    
    def imageToFile(self, path, localfile):
        # Verify a valid path was given
        if not path in self.images:
            return False
            
        # Download and save the image
        return self.wrapper.downloadFile("GET", self.images[path], localfile, binary = True)

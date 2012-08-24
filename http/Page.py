from HTTPWrapper import HTTPWrapper
from neolib.RegLib import RegLib
import urlparse

class Page:
    wrapper = None
    cookies = None
    pageHeader = ""
    pageContent = ""
    
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
            self.pageContent = self.wrapper.request(type, url, postData, vars)
            
            # Set the response header
            self.pageHeader = self.wrapper.repHeader
            
            # Set any updated cookies
            self.cookies = self.wrapper.cookieJar
    
    def loadImages(self):
        # Parse all images
        mats = RegLib.getMat("page", "images", self.pageContent)
        
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
        
        # Grab the image data
        imgData = self.wrapper.request("GET", self.images[path])
        
        # Save the image to the given local file
        f = open(localfile, "wb")
        f.write(imgData)
        f.close()
        
        # Return operation was successful
        return True
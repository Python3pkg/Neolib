from HTTPWrapper import HTTPWrapper

class Page:
    wrapper = None
    cookies = None
    pageHeader = ""
    pageContent = ""
    
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
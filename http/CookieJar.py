from Cookie import Cookie

class CookieJar:
    # All stored cookies
    cookies = {}
    
    def __init__(self, strCookies):
        # Add the given cookies
        self.addCookies(strCookies)
            
    def getCookies(self):
        cookieStr = ""
        
        # Loop through each cookie, convert it to its string value, and append it to the final string
        for cookieName in self.cookies:
            if not self.cookies[cookieName].isExpired():
                cookieStr += self.cookies[cookieName].toStr()
        return cookieStr
        
    def addCookies(self, strCookies):
        # Loop through given cookies
        for strCookie in strCookies:
            # Create a Cookie to represent each one
            cookie = Cookie(strCookie)
            
            # Add to the stored cookies in the format of {'cookie name': 'cookie object'}
            self.cookies[cookie.name] = cookie
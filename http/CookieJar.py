from Cookie import Cookie

class CookieJar:
    cookies = {}
    
    def __init__(self, strCookies):
        self.addCookies(strCookies)
            
    def getCookies(self):
        cookieStr = ""
        
        # name=value;name=value; format
        for cookieName in self.cookies:
            if not self.cookies[cookieName].isExpired():
                cookieStr += self.cookies[cookieName].toStr()
        return cookieStr
        
    def addCookies(self, strCookies):
        for strCookie in strCookies:
            cookie = Cookie(strCookie)
            self.cookies[cookie.name] = cookie
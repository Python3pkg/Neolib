from Cookie import Cookie

class CookieJar:
    cookies = []
    
    def __init__(self, strCookies):
        for strCookie in strCookies:
            cookie = Cookie(strCookie)
            self.cookies.append(cookie)
            
    def getCookies(self):
        cookieStr = ""
        for cookie in self.cookies:
            if not cookie.isExpired():
                cookieStr += cookie.toStr()
        return cookieStr
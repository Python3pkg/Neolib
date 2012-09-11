from neolib.exceptions import logoutException
from neolib.exceptions import invalidUser
from neolib.http.Page import Page
from neolib.user.Pet import Pet

class UserHook(object):
    pass

# Automatically updates a user's NPs on each page request
class updateNPs(UserHook):
    
    @staticmethod
    def processHook(usr, pg):
        # Ensure this page has the current Nps on it
        if pg.content.find("npanchor") != -1:
            try:
                # Parse and set Nps
                usr.nps = int( pg.getParser().find("a", id = "npanchor").text.replace(",", "") )
            except Exception:
                return [usr, pg]
                
        return [usr, pg]
                
# Automatically updates a user's active pet on each page request
class updateActivePet(UserHook):
    
    @staticmethod
    def processHook(usr, pg):
        # Ensure this page has the current active pet on it
        if pg.content.find("sidebarTable") != -1:
            try:
                # Parse the active pet details
                panel = pg.getParser().find("table", "sidebarTable")
                
                usr.activePet = Pet(panel.tr.td.text)
                
                # Grab pet stats
                stats = panel.find("table").find_all("td", align="left")
                
                # Update the pet stats
                usr.activePet.species = stats[0].text
                usr.activePet.health = stats[1].text
                usr.activePet.mood = stats[2].text
                usr.activePet.hunger = stats[3].text
                usr.activePet.age = stats[4].text
                usr.activePet.level = stats[5].text
            except Exception:
                return [usr, pg]
                
        return [usr, pg]
        
# Checks if a user has been logged out, and attempts to log the user back in if autoLogin is set to True
class logBackIn(UserHook):
    
    @staticmethod
    def processHook(usr, pg):
        if "Location" in pg.header.vars:
            if pg.header.vars['Location'].find("loginpage.phtml") != -1:
                # If auto login is enabled, try to log back in, otherwise raise an exception to let higher processes know the user is logged out.
                if usr.autoLogin:
                    # Clear cookies
                    usr.cookieJar = None
                    if usr.login():
                        # Update status
                        usr.loggedIn = True
                            
                        # Request the page again now that the user is logged in
                        pg = Page(pg.url, usr.cookieJar, pg.postData, pg.vars)
                    else:
                        # Failed to login. Update status, log it, and raise an exception
                        usr.loggedIn = False
                        logging.getLogger("neolib.user").info("User was logged out. Failed to log back in.")
                        raise logoutException
                else:
                    # Auto login is not enabled. Update status and raise an exception.
                    usr.loggedIn = False
                    logging.getLogger("neolib.user").info("User was logged out. Auto login is disabled.")
                    raise logoutException
            
        return [usr, pg]
from neolib.exceptions import logoutException
from neolib.exceptions import invalidUser
from neolib.http.Page import Page
from neolib.user.Pet import Pet

def updateNPs(usr, pg):
    # Ensure this page has the current Nps on it
    if pg.content.find("npanchor") != -1:
        try:
            # Parse and set Nps
            usr.nps = int( pg.find("a", id = "npanchor").text.replace(",", "") )
        except Exception:
            return [usr, pg]
                
    return [usr, pg]
                
def updatePet(usr, pg):
    # Ensure this page has the current active pet on it
    if pg.content.find("sidebarTable") != -1:
        try:
            # Parse the active pet details
            panel = pg.find("table", "sidebarTable")
            
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
        
def autoLogin(usr, pg):
    if pg.title == "Neopets - Hi!":
        # If auto login is enabled, try to log back in, otherwise raise an exception to let higher processes know the user is logged out.
        if usr.autoLogin:
            # Clear cookies
            usr.session = Page.newSession()
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
    
def checkRandomEvent(usr, pg):
    pass
    

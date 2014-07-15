""":mod:`HTTPForm` -- An interface for manipulating HTML Forms

.. module:: HTTPForm
   :synopsis: An interface for manipulating HTML Forms
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from urllib.parse import urlparse

class HTTPForm:
    
    """Provides an interface for manipulating an HTML form
    
    Parses recieved HTML form data into respective parts for easy modification
    and form manipulation. Also reduces end-user work by providing a convient
    function for submitting form data.
    
    Attributes
       items (dict) -- All form inputs
       usr (User) -- User associated with this form
       url (str) -- Page URL this form came from (Used as referer)
       action (str) -- Form submit action
       name (str) -- Form name
       method (str) -- Form HTTP method
       image (str) -- Any associated image (I.E Main Shop Captcha)
       usePin (bool) -- Whether or not to submit user's pin with the form data
       
    Initialization
       HTTPForm(usr, url, content)
       
       Parses the given HTML and populates the form data
       
       Parameters
          usr (User) -- User associated with the form (used in HTTPForm.submit())
          url (str) -- Page URL this form came from
          content (str) -- Form HTML
        
    Example
       >>> pg = usr.getPage("http://www.neopets.com")
       >>> form = pg.getForm(usr, action='login.phtml')
       >>> form['username'] = 'blah'
       >>> form['password'] = 'moreblah'
       >>> pg = form.submit()
    """
    
    items = None
    
    usr = None
    url = ""
    action = ""
    name = ""
    method = ""
    image = ""
    
    usePin = False
    
    def __init__(self, usr, url, content):
        self.usr = usr
        self.url = url
        self.__dict__.update(content.attrs)
        
        self.items = {}
        for inp in content.find_all("input"):
            if inp.has_key("name"):
                if inp['type'] == 'submit': continue
                if not inp.has_key("value"): inp['value'] = ""
                self.items[inp['name']] = inp['value']
            elif inp.has_key('type'):
                if inp['type'] == 'image':
                    self.image = inp['src']
                    self.items.update({'x': '', 'y': ''})
    
    def submit(self):
        """ Posts the form's data and returns the resulting Page
           
        Returns
           Page - The resulting page
        """
        u = urlparse(self.url)
        
        if not self.action:
            self.action = self.url
        elif self.action == u.path:
            self.action = self.url
        else:
            if not u.netloc in self.action:
                path = "/".join(u.path.split("/")[1:-1])
                if self.action.startswith("/"):
                    path = path + self.action
                else:
                    path = path + "/" + self.action
                self.action = "http://" + u.netloc + "/" + path
            
        return self.usr.getPage(self.action, self.items, {'Referer': self.url}, self.usePin)
        
    def update(self, d):
        """ Updates the form data with the given dictionary
        
        Parameters
           d - Dictionary to update with
        """
        self.items.update(d)
        
    def __getitem__(self, key):
        return self.items[key]
        
    def __setitem__(self, key, value):
        self.items[key] = value
        
    def __delitem__(self, key):
        self.items.pop(key)
        
    def __contains__(self, key):
        if key in self.items:
            return True
        else:
            return False
            
    def __iter__(self):
        for item in self.items:
            yield self.items[item]
            
    def __len__(self):
        return len(self.items)

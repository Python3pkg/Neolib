""":mod:`Bank` -- Provides an interface for administrating a user's bank

.. module:: Bank
   :synopsis: Provides an interface for administrating a user's bank
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import notEnoughBalance
from neolib.exceptions import parseException
from neolib.exceptions import notEnoughNps
import logging

class Bank:
    
    """Provides an interface for administrating a user's bank
    
    Provides functionality for loading a user's bank account, withdrawing
    and depositing neopoints, as well as collecting the user's daily interest.
    
    
    Attributes
       usr (User) -- User that owns the bank
       type (str) -- Type of bank account
       balance (str) -- Account balance
       yearlyInterest (str) -- Account yearly interest
       dailyInterest (str) -- Account daily interest
       collectedInterest (bool) -- Whether or not daily interest has been collected yet
        
    Example
       >>> usr.bank.load()
       >>> usr.bank.balance
       100000
       >>> usr.bank.withdraw(100)
       True
    """
    
    usr = None
    type = ""
    balance = ""
    yearlyInterest = ""
    dailyInterest = ""
    
    collectedInterest = True
    
    def __init__(self, usr):
        if not usr:
            return
            
        self.usr = usr
            
    def load(self):
        """ Loads the user's account details and 
           
        Raises
           parseException
        """
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Verifies account exists
        if not "great to see you again" in pg.content:
            logging.getLogger("neolib.user").info("Could not load user's bank. Most likely does not have an account.", {'pg': pg})
            raise noBankAcct
            
        self.__loadDetails(pg)
    
    def deposit(self, amount):
        """ Deposits specified neopoints into the user's account, returns result
           
        Parameters:
           amount (int) -- Amount of neopoints to deposit
           
        Returns
           bool - True if successful, False otherwise
           
        Raises
           notEnoughNps
        """
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        if self.usr.nps < int(amount):
            raise notEnoughNps
            
        form = pg.form(action="process_bank.phtml")
        form.update({'type': 'deposit', 'amount': str(amount)})
        form.usePin = True
        pg = form.submit()
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            self.__loadDetails(pg)
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to deposit NPs for unknown reason. User NPs: " + str(self.usr.nps) + ". Amount: " + str(amount), {'pg': pg})
            return False
            
    def withdraw(self, amount):
        """ Withdraws specified neopoints from the user's account, returns result
           
        Parameters:
           amount (int) -- Amount of neopoints to withdraw
           
        Returns
           bool - True if successful, False otherwise
           
        Raises
           notEnoughBalance
        """
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        try:
            results = pg.find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            self.balance = results[1].text.replace(" NP", "")
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank balance.", {'pg': pg})
        
        if int(amount) > int(self.balance.replace(",", "")):
            raise notEnoughBalance
            
        form = pg.form(action="process_bank.phtml")
        form.update({'type': 'withdraw', 'amount': str(amount)})
        form.usePin = True
        pg = form.submit()
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            self.__loadDetails(pg)
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to withdraw NPs for unknown reason. User NPs: " + str(self.usr.nps) + ". Amount: " + str(amount), {'pg': pg})
            return False
            
    def collectInterest(self):
        """ Collects user's daily interest, returns result
           
        Returns
           bool - True if successful, False otherwise
        """
        if self.collectedInterest:
            return False
            
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        form = pg.form(action="process_bank.phtml")
        form['type'] = "interest"
        pg = form.submit()
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            self.__loadDetails(pg)
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to collect daily interest for unknown reason.", {'pg': pg})
            return False
        
        
    def __loadDetails(self, pg = None):
        try:
            results = pg.find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            
            self.type = results[0].text
            self.balance = results[1].text.replace(" NP", "")
            self.interestRate = results[2].text
            self.yearlyInterest = results[3].text
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank details.", {'pg': pg})
            raise parseException
        
        # Checks if interest has been collected
        if not "not be able to collect" in pg.content and not "have already collected" in pg.content:
            try:
                self.dailyInterest = pg.find("input", {'value': 'interest'}).find_next_sibling('input')['value'].split("(")[1].split(" NP)")[0]
                self.collectedInterest = False
            except Exception:
                logging.getLogger("neolib.user").exception("Could not parse user's bank daily interest.", {'pg': pg})
                raise parseException

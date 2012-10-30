""":mod:`Bank` -- Represents a Neopet

.. module:: Bank
   :synopsis: Represents a Neopet
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""


class Pet:
    
    """Represents a Neopet
    
    Attributes
       name (str) -- Neopet name
       species (str) -- Neopet species
       health (str) -- Neopet health
       mood (str) -- Neopet mood
       hunger (str) -- Neopet hunger level
       age (str) -- Neopet age
       level (str) -- Neopet level
        
    Example
       >>> pet = Pet("somename")
    """
    
    name = ""
    species = ""
    health = ""
    mood = ""
    hunger = ""
    age = ""
    level = ""
    
    def __init__(self, name):
        self.name = name

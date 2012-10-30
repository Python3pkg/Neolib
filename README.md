Neolib
======

Neolib is an in-depth and robust Python library designed to assist programmers in creating programs which automate mundane tasks on the popular browser based game, Neopets. The goal of Neolib is to objectify Neopets by translating it's many objects and tasks into classes and functions that represent them.

Installation
======

The easiest way to install Neolib is by downloading the PyPi distribution using easy_install:

```
easy_install neolib
```

Alternatively you can download the tar archive above and use setuptools to install it:

```
python setup.py install
```

Getting Started
======

Neolib is a robust library that consists of many components that each serve a specific function. Your application may not need access to all of these components, however some components are used in almost all applications.

Creating a User
------

A user is defined as both a Neopets account and an end-user of a program in Neolib. Thus, the User object is by far the most important object in Neolib. Initializing a User object does a few things:

* Initializes user attributes: Sets the username, password, and optional PIN.
* Initializes configuration: If no previous configuration block for the given username is found, attempts to create a new block with some default values. Otherwise, the existing configuration values are loaded into the User object.
* Initializes a new session: A new HTTP session is created for tracking the user's cookies. Note this session is normally saved with the configuration and can be loaded later to resume a previously created session.

The following shows the basic process of initializing a user object and logging the user into Neopets:

```python
>>> from neolib.user.User import User
>>> usr = User("username", "password")
>>> usr.login()
True
```

Below is an example of how the configuration aspect works:

```python
>>> usr.savePassword = True
>>> usr.save()
>>> usr = User("username")
>>> usr.password
'password'
>>> usr.loggedIn
True
```

The above example shows how setting the savePassword attribute to True will save the user's password (in an encoded text) to the configuration. It also shows how the configuration data was saved for the username "username". Finally, it shows that the previous session was saved and that upon loading the user again, the user was stilled logged in since the old session was loaded.

Basic Inventory Management
------

Another common feature used in programs is inventory management. Below we assume the user has a Green Apple in their inventory. We first stock the item in their shop, price the item and update the shop. Then we remove it from the shop. place it in the SDB, and finally move it back to the user's inventory.

```python
>>> from neolib.item.Item import Item
>>> from neolib.shop.ShopWizard import ShopWizard
>>> usr.inventory.load()
>>> usr.inventory['Green Apple']
<Item 'Green Apple'>
>>> usr.inventory['Green Apple'].sendTo(Item.SHOP)
True
>>> usr.shop.load()
>>> usr.shop.inventory['Green Apple'].price = ShopWizard.priceItem(usr, 'Green Apple')
>>> usr.shop.update()
True
>>> usr.shop.load()
>>> usr.shop.inventory['Green Apple'].remove = 1
>>> usr.shop.update()
True
>>> usr.inventory.load()
>>> usr.inventory['Green Apple'].sendTo(Item.SDB)
True
>>> usr.SDB.load()
>>> usr.SDB.inventory['Green Apple'].remove = 1
>>> usr.SDB.update()
True
>>> usr.inventory.load()
>>> usr.inventory['Green Apple']
<Item 'Green Apple'>
```

Buying Items
------

Another common feature required for programs is the ability to buy items. Neolib currently supports the ability to buy items from both user shops and main shops. Below is an example of searching for a 'Mau Codestone' with the Shop Wizard and buying the first result.

```python 
>>> from neolib.shop.ShopWizard import ShopWizard
>>> res = ShopWizard.search(usr, 'Mau Codestone')
>>> res.buy(0)
True
>>> usr.inventory.load()
>>> 'Mau Codestone' in usr.inventory
True
```

Here is an example of buying a main shop item:

```python
>>> from neolib.shop.MainShop import MainShop
>>> ms = MainShop(usr, '1')
>>> ms.load()
>>> ms.name
'Neopian Fresh Foods'
>>> ms.inventory['Peanut'].buy("1107")
True
>>> usr.inventory.load()
>>> 'Peanut' in usr.inventory
```

#In script.py we’ve defined a CandleShop class for our new candle shop that we’ve named Here’s a Hot Tip: Buy Drip Candles. We want to define our own exceptions for when we run out of candles to sell.
#Define your own exception called OutOfStock that inherits from the Exception class.

# Define your exception up here:
class OutOfStock(Exception):
  pass

# Update the class below to raise OutOfStock
class CandleShop:
  name = "Here's a Hot Tip: Buy Drip Candles"
  def __init__(self, stock):
    self.stock = stock
    
  #Have CandleShop raise your OutOfStock exception when CandleShop.buy() tries to buy a candle that’s out of stock.
  def buy(self, color):
    if (self.stock[color] <= 0):
      raise OutOfStock
    self.stock[color] = self.stock[color] - 1

candle_shop = CandleShop({'blue': 6, 'red': 2, 'green': 0})
candle_shop.buy('blue')

# This should raise OutOfStock:
# candle_shop.buy('green')

#----------------------------------------------------------------------------------------------------------------------------------------

class Message:
  def __init__(self, sender, recipient, text):
    self.sender = sender
    self.recipient = recipient
    self.text = text

class User:
  def __init__(self, username):
    self.username = username
    
  def edit_message(self, message, new_text):
    if message.sender == self.username:
      message.text = new_text
      
#In script.py, we’ve defined two classes, Message and User. Create an Admin class that subclasses the User class.
#Override User‘s .edit_message() method in Admin so that an Admin can edit any messages.
class Admin(User):
  def edit_message(self, message, new_text):
    message.text = new_text

#----------------------------------------------------------------------------------------------------------------------------------------

class PotatoSalad:
  def __init__(self, potatoes, celery, onions):
    self.potatoes = potatoes
    self.celery = celery
    self.onions = onions
    
#You’re invited to a potluck this week and decide to make your own special version of Potato Salad!
#In script.py you’ll find a class called PotatoSalad, make a subclass of PotatoSalad called SpecialPotatoSalad.
#The difference with your special potato salad is… you add raisins to it! You can’t remember when you started doing this, but Dolores always hoots about it at her potlucks and if that isn’t the nicest thing. You always use the full package of raisins for every potato salad you make, and each package has 40 raisins in it.
#In your constructor for SpecialPotatoSalad, after making regular potato salad, set self.raisins = 40.
class SpecialPotatoSalad(PotatoSalad):
  def __init__(self, potatoes, celery, onions):
    super().__init__(potatoes, celery, onions)
    self.raisins = 40
    
#----------------------------------------------------------------------------------------------------------------------------------------
    
class InsurancePolicy:
  def __init__(self, price_of_item):
    self.price_of_insured_item = price_of_item
    
#In script.py we’ve defined an InsurancePolicy class. Create a subclass of InsurancePolicy called VehicleInsurance.
#Give VehicleInsurance a .get_rate() method that takes self as a parameter. Return .001 multiplied by the price of the vehicle.
class VehicleInsurance(InsurancePolicy):
  def get_rate(self):
    return self.price_of_insured_item*0.001

#Create a different subclass of InsurancePolicy called HomeInsurance.
#Give HomeInsurance a .get_rate() method that takes self as a parameter. Return .00005 multiplied by the price of the home.
class HomeInsurance(InsurancePolicy):
  def get_rate(self):
    return self.price_of_insured_item*0.00005
	
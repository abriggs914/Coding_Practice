import pytz
from datetime import datetime, timezone
#from tzlocal import get_localzone
#LEARN PYTHON: CLASSES
#Basta Fazoolin'
#Youve started position as the lead programmer for the family-style Italian restaurant Basta Fazoolin with My Heart. The restaurant has been doing fantastically and seen a lot of growth lately. Youve been hired to keep things organized.

#At Basta Fazoolin with my Heart our motto is simple: when youre here with family, thats great! We have four different menus: brunch, early-bird, dinner, and kids.
#Create a Menu class.

#Lets create our first menu: brunch. Brunch is served from 11am to 4pm. The following items are sold during brunch:
#{  'pancakes': 7.50, 'waffles': 9.00, 'burger': 11.00, 'home fries': 4.50, 'coffee': 1.50, 'espresso': 3.00, 'tea': 1.00, 'mimosa': 10.50, 'orange juice': 3.50}

#Lets create our second menu item early_bird. Early-bird Dinners are served from 3pm to 6pm. The following items are available during the early-bird menu:
#{'salumeria plate': 8.00, 'salad and breadsticks (serves 2, no refills)': 14.00, 'pizza with quattro formaggi': 9.00, 'duck ragu': 17.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 1.50, 'espresso': 3.00}

#Lets create our third menu, dinner. Dinner is served from 5pm to 11pm. The following items are available for dinner:
#{  'crostini with eggplant caponata': 13.00, 'ceaser salad': 16.00, 'pizza with quattro formaggi': 11.00, 'duck ragu': 19.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 2.00, 'espresso': 3.00,}

#And lets create our last menu, kids. The kids menu is available from 11am until 9pm. The following items are available on the kids menu.
#{  'chicken nuggets': 6.50, 'fusilli with wild mushrooms': 12.00, 'apple juice': 3.00}

#Give our Menu class a string representation method that will tell you the name of the menu. Also, indicate in this representation when the menu is available.

#Give Menu a method .calculate_bill() that has two parameters: self, and purchased_items, a list of the names of purchased items.
#Have calculate_bill return the total price of a purchase consisiting of all the items in purchased_items.

#additional method to convert string representations of strings to a number (0-23)
def adjust_string_time(time):
  suffix = time[-2:]
  suffix = suffix.upper()
  x = len(time) - len(suffix)
  num = time[0:x]
  if (suffix == "AM"):
    return num
  elif (suffix == "PM"):
    if (num == "12"):
      return 12
    return int(num) + 12
  else:
    # error just returning noon
    return 12

class Menu:
  
  def calculate_bill(self, purchased_items):
    total = 0
    for item in purchased_items:
      foods = list(self.items.keys())
      if (item in foods):
        price = self.items[item]
        total += price
    return total
  
  def open_hours(start, end):
    startSuffix = "AM"
    endSuffix = "AM"
    if (start > 12):
    	start -= 12
    	startSuffix = "PM"
    if (end > 12):
    	end -= 12
    	endSuffix = "PM"
    return str(start) + startSuffix + " to " + str(end) + endSuffix
  
  def check_availability(start, end, timeOfDay):
    hour = timeOfDay.hour
    if (hour < start or hour > end):
      return "CLOSED"
    return "OPEN"
  
  def getTime():
    #this function was tricky, the isoformat() function will convert the dattime object into a string
    atl = pytz.timezone('Canada/Atlantic')
    utc_dt = datetime.now(timezone.utc)
    d = utc_dt.astimezone(atl)#.isoformat()
    #datetime.datetime.strptime('16Sep2012', '%d%b%Y')
    current_time = d
    return current_time
  
  def __init__(self, name, items, start_time, end_time):
    self.name = name
    self.items = items
    self.start_time = start_time
    self.end_time = end_time    
  
  def __repr__(self):
    current_time = Menu.getTime()
    name = self.name
    hours = Menu.open_hours(self.start_time, self.end_time)
    availability = Menu.check_availability(self.start_time, self.end_time, current_time)
    return "{name}\'s menu:\n\tTime of Day: {time}\n\tHours: {hours}\n\tAvailable: {availability}\n".format(name = name, time = current_time, hours = hours, availability = availability)
  
brunch = Menu("brunch", {'pancakes': 7.50, 'waffles': 9.00, 'burger': 11.00, 'home fries': 4.50, 'coffee': 1.50, 'espresso': 3.00, 'tea': 1.00, 'mimosa': 10.50, 'orange juice': 3.50}, 11, 16)

early_bird = Menu("early bird", {'salumeria plate': 8.00, 'salad and breadsticks (serves 2, no refills)': 14.00, 'pizza with quattro formaggi': 9.00, 'duck ragu': 17.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 1.50, 'espresso': 3.00}, 15, 18)

dinner = Menu("dinner",{  'crostini with eggplant caponata': 13.00, 'ceaser salad': 16.00, 'pizza with quattro formaggi': 11.00, 'duck ragu': 19.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 2.00, 'espresso': 3.00,}, 17, 23)

kids = Menu("kids", {'chicken nuggets': 6.50, 'fusilli with wild mushrooms': 12.00, 'apple juice': 3.00}, 11, 21)

#Try out our string representation. If you call print(brunch) it should print out something like the following:
#brunch menu available from 11am to 4pm
print(brunch)
print(early_bird)
print(dinner)
print(kids)

#Test out Menu.calculate_bill(). We have a breakfast order for one order of pancakes, one order of home fries, and one coffee. Pass that into brunch.calculate_bill() and print out the price.
#You should get the value 13.5.
print(brunch.calculate_bill(['pancakes', 'home fries', 'coffee']))

#What about an early-bird purchase? Our last guests ordered the salumeria plate and the vegan mushroom ravioli. Calculate the bill with .caluclate_bill().
#This purchase should result in a bill of 21.5.
print(early_bird.calculate_bill(['salumeria plate', 'mushroom ravioli (vegan)']))

#Basta Fazoolin with my Heart has seen tremendous success with the family market, which is fantastic because when youre at Basta Fazoolin with my Heart with family, thats great!
#Weve decided to create more than one restaurant to offer our fantastic menus, services, and ambience around the country.
#First, lets create a Franchise class.

#Give the Franchise class a constructor. Take in an address, and assign it to self.address. Also take in a list of menus and assign it to self.menus.

#Give our Franchises a string represenation so that we’ll be able to tell them apart. If we print out a Franchise it should tell us the address of the restaurant.

#Let’s tell our customers what they can order! Give Franchise an .available_menus() method that takes in a time parameter and returns a list of the Menu objects that are available at that time.

class Franchise:
  def __init__(self, name, address, menus):
    self.name = name
    self.address = address
    self.menus = menus
  
  def __repr__(self):
    print("{name} is locaated at {address}".format(name = self.name, address = self.address))
    
  def available_menus(self, time):
    if (type(time) is str):
      time = adjust_string_time(time)
    menus = self.menus
    items_available = []
    for menu in menus:
      start = menu.start_time
      end = menu.end_time
      if (time < end and time > start):
        items_available.append(menu)
    return items_available

#Lets create our first two franchises! Our flagship store is located at "1232 West End Road" and our new installment is located at "12 East Mulberry Street". Pass in all four menus along with these addresses to define flagship_store and new_installment.
flagship_store = Franchise("Flagship Store", "1232 West End Road", [brunch, early_bird, dinner, kids])
new_installment = Franchise("New Installment", "12 East Mulberry Street", [brunch, early_bird, dinner, kids])

#Let’s test out our .available_menus() method! Call it with 12 noon as an argument and print out the results.
flag_ship_available_menus = flagship_store.available_menus(12)
print(flag_ship_available_menus)

#Let’s do another test! If we call .available_menus() with 5pm as an argument and print out the results.
new_installment_available_menus = flagship_store.available_menus('5pm')
print(new_installment_available_menus)

#Since we’ve been so successful building out a branded chain of restaurants, we’ve decided to diversify. We’re going to create a restaurant that sells arepas!
#First let’s define a Business class.

#Give Business a constructor. A Business needs a name and a list of franchises.
class Business:
  
  def __init__(self, name, franchises):
    self.name = name
    self.franchises = franchises

basta_fazoolin_with_my_heart = Business("Basta Fazoolin' with my Heart", [flagship_store, new_installment])

#Before we create our new business, we’ll need a Franchise and before our Franchise we’ll need a menu. The items for our Take a’ Arepa available from 10am until 8pm are the following:
#{  'arepa pabellon': 7.00, 'pernil arepa': 8.50, 'guayanes arepa': 8.00, 'jamon arepa': 7.50}
#Save this to a variable called arepas_menu.
arepas_menu = {'arepa pabellon': 7.00, 'pernil arepa': 8.50, 'guayanes arepa': 8.00, 'jamon arepa': 7.50}

#Next let’s create our first Take a’ Arepa franchise! Our new restaurant is located at "189 Fitzgerald Avenue". Save the Franchise object to a variable called arepas_place.
arepas_place = Franchise("Arepa's Place", "189 Fitzgerald Avenue", [arepas_menu])

#Now let’s make our new Business! The business is called "Take a' Arepa"!
take_a_arepa = Business("Take a' Arepa", arepas_place)

#Congrats! You created a system of classes that help structure your code and perform all business requirements you need. Whenever we need a new feature we’ll have the well-organized code required to make developing and shipping it easy.

#If you are stuck on the project or would like to see an experienced developer work through the project, watch the following project walkthrough video!
# https://youtu.be/Dk-ePlxdmBU





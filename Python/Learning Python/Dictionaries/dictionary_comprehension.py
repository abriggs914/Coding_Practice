#CREATING DICTIONARIES
#List Comprehensions to Dictionaries
#Let’s say we have two lists that we want to combine into a dictionary, like a list of students and a list of their heights, in inches:
#names = ['Jenny', 'Alexus', 'Sam', 'Grace']
#heights = [61, 70, 67, 64]
#Python allows you to create a dictionary using a list comprehension, with this syntax:
#students = {key:value for key, value in zip(names, heights)}
#students is now {'Jenny': 61, 'Alexus': 70, 'Sam': 67, 'Grace': 64}
#Remember that zip() combines two lists into a list of pairs. This list comprehension:
#Takes a pair from the zipped list of pairs from names and heights
#Names the elements in the pair key (the one originally from the names list) and value (the one originally from the heights list)
#Creates a key : value item in the students dictionary
#Repeats steps 1-3 for the entire list of pairs
#Instructions
drinks = ["espresso", "chai", "decaf", "drip"]
caffeine = [64, 40, 0, 120]

#You have two lists, representing some drinks sold at a coffee shop and the milligrams of caffeine in each. First, create a variable called zipped_drinks that is a list of pairs between the drinks list and the caffeine list.
zipped_drinks = zip(drinks, caffeine)

#Create a dictionary called drinks_to_caffeine by using a list comprehension that goes through the zipped_drinks list and turns each pair into a key:value item.
drinks_to_caffeine = {key:value for key, value in zipped_drinks}

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

user_ids = {"teraCoder": 100019, "pythonGuy": 182921, "samTheJavaMaam": 123112, "lyleLoop": 102931, "keysmithKeith": 129384}

#Use .get() to get the value of "teraCoder"‘s user ID, with 100000 as a default value if the user doesn’t exist. Store it in a variable called tc_id. Print tc_id to the console.
tc_id = user_ids.get("teraCoder", 10000)
print(tc_id)

#Use .get() to get the value of "superStackSmash"‘s user ID, with 100000 as a default value if the user doesn’t exist. Store it in a variable called stack_id. Print stack_id to the console.
stack_id = user_ids.get("superStackSmash", 100000)
print(stack_id)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

available_items = {"health potion": 10, "cake of the cure": 5, "green elixir": 20, "strength sandwich": 25, "stamina grains": 15, "power stew": 30}
health_points = 20

#You are designing the video game Big Rock Adventure. We have provided a dictionary of items in the player’s inventory to add points to their health meter. In one line, add the value of "stamina grains" to health_points and remove the item from the dictionary. If the key does not exist, add 0 to health_points.

health_points += available_items.pop("stamina grains", 0)

#In one line, add the value of "power stew" to health_points and remove the item from the dictionary. If the key does not exist, add 0 to health_points.

health_points += available_items.pop("power stew", 0)

#In one line, add the value of "mystic bread" to health_points and remove the item from the dictionary. If the key does not exist, add 0 to health_points.

health_points += available_items.pop("mystic bread", 0)

#Print available_items and health_points.
print(available_items)
print(health_points)


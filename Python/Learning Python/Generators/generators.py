from time import time
import random

# Python program to compare the benefits of lists and generators
# The key differences seem to be only memory usage. The generators
# will release their used memory when it yields the next value.
# the list comprehensions or list versions of these tasks, compute
# all elements first in memory then return the entire list.
# Both methods seem to take relatively the same time.

# If this script is run on a linux system, then you can uncomment and
# attempt to analyze the memory usage of the two methods.
# import mem_profile

class Person:
	
	def __init__(self, name, age, fav_nums):
		self.name = name
		self.age = age
		self.fav_nums = fav_nums
		
	def __repr__(self):
		message = "\n{0} is {1}".format(self.name, self.age)
		suffix = "year"
		if self.age > 1:
			suffix += "s"
		message += " {0} old. Their Favorite numbers are:\n\t{1}\n".format(suffix, self.fav_nums)
		return message
		
		
def create_person(people_data):
	for person in people_data:
		name, age, fav_nums = person
		yield Person(name, age, fav_nums)
	
def how_long(title, start, stop):
	length = stop - start
	print("\nTitle:\t\t{0}\nlength\t\t{1}".format(title, length))
	
	
avery_data = ("Avery", 24, [8, 15, 99])

num_people = 1000000
people_names = ["Bill", "Sarah", "James", "Kate", "Ted", "Stacey"]
people_ages = [i for i in range(18, 76)]
people_fav_nums = [i for i in range(200)]

def create_population_iter(num_people):
	population = []
	for p in range(num_people):
		name = random.choice(people_names)
		age = random.choice(people_ages)
		fav_nums = [random.choice(people_fav_nums) for i in range(3)]
		population.append(Person(name, age, fav_nums))
	return population
	
def create_population_gen(num_people):
	for p in range(num_people):
		name = random.choice(people_names)
		age = random.choice(people_ages)
		fav_nums = [random.choice(people_fav_nums) for i in range(3)]
		yield Person(name, age, fav_nums)
	
	
	
#######################################################################################################################
# Object version

start_time = time()
avery_obj = Person(*avery_data)
print(avery_obj)
end_time = time()
how_long("Object version - Person creation", start_time, end_time)

#######################################################################################################################
# Generator version

start_time = time()
people_data = [avery_data]
print(list(create_person(people_data)))
end_time = time()
how_long("Generator version - Person creation", start_time, end_time)


#######################################################################################################################
# Object version

start_time = time()
population_obj = create_population_iter(num_people)
# print(population_obj)
end_time = time()
how_long("Object version - Population creation", start_time, end_time)

#######################################################################################################################
# Generator version

start_time = time()
population_gen = list(create_population_gen(num_people))
# print(population_gen)
end_time = time()
how_long("Generator version - Population creation", start_time, end_time)

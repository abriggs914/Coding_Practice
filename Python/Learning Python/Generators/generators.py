from time import time
import mem_profile

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
	
#######################################################################################################################
# Object version

start_time = time()
avery_obj = Person(*avery_data)
print(avery_obj)
end_time = time()
how_long("Object version", start_time, end_time)


#######################################################################################################################
# Generator version

start_time = time()
people_data = [avery_data]
print(list(create_person(people_data)))
end_time = time()
how_long("Generator version", start_time, end_time)
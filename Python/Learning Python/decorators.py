
spacer = "".join(["_" for i in range(120)])

# 1. Functions are objects

def add_five_1(num):
	print("add_five_1: {" + str(num + 5) + "}")

add_five_1  # no error
add_five_1(7)  # prints 12
print(add_five_1)  # <function add_five at 0x01440858>
print(add_five_1(7))  # None

print(spacer)

# 2. Functions within functions

def add_five_2(num):
	def add_two(num):
		return num + 2
	num_plus_two = add_two(num)
	print("add_five_2: {" + str(num_plus_two + 3) + "}")
	
# add_two(7)  # throws an error, only defined locally
add_five_2  # no error
add_five_2(7)  # prints 12
print(add_five_2)  # <function add_five_2 at 0x03A6C0C0>
print(add_five_2(7))  # None

print(spacer)

# 3. Returning functions from functions

def get_math_function(operation): # + or -
	def add(n1, n2):
		return n1 + n2
	def sub(n1, n2):
		return n1 - n2
	
	if operation == '+':
		return add
	elif operation == '-':
		return sub
	
add_function = get_math_function('+')
sub_function = get_math_function('-')
print(add_function)  # prints <function get_math_function.<locals>.add at 0x0036F780>
print(add_function(4, 6))  #  prints 10
print(sub_function(4, 6))  #  prints -2

# 4. Decorating a function

def title_decorator(print_name_function):
	def wrapper():
		print("Professor:")
		print_name_function()
	return wrapper

def print_my_name():
	print("Avery")
	
print_my_name()  # prints "Avery"
	
decorated_function = title_decorator(print_my_name)  # stores the wrapper function
	
decorated_function()  # prints 
                      # Professor:
                      # Avery
					  
def print_joes_name():
	print("Joe")
	
decorated_function = title_decorator(print_joes_name)  # stores the wrapper function
	
decorated_function()  # prints
                      # Professor:
                      # Joe

	
# 5. Decorators

def title_decorator_dec(print_name_function):
	def wrapper():
		print("Professor:")
		print_name_function()
	return wrapper

@title_decorator_dec
def print_my_name_dec():
	print("Avery")
	
print_my_name_dec()  # prints 
                     # Professor:
					 # Avery
	
@title_decorator_dec	  
def print_joes_name_dec():
	print("Joe")
	
print_joes_name()  # prints 
                   # Professor:
				   # Joe
# 6. Decorators w/ Parameters

def title_decorator_param_dec(print_name_function):
	def wrapper(*args, **kwargs):
		print("Professor:")
		print_name_function(*args, **kwargs)
	return wrapper

@title_decorator_param_dec
def print_name(name, age):
	print(name + " is " + str(age) + " years old.")
	
print_name("Shelby", 50)  # prints
                          # Professor:
					      # Shelby
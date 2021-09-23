import inspect
import traceback

def foo(a, b):
	try:
		return a + b
	except ValueError:
		return a
	except TypeError:
		return b

print(inspect.findsource(foo))
print(dir(foo))

vals = dir(foo)

for val in vals:
	try:
		print("XXX\tval: <{}>: <{}>".format(val, eval(val)))
	except NameError:
		print("val: <{}>: cannot be evaluated".format(val))
	except TypeError:
		print("val: <{}>: cannot be evaluated".format(val))
	except AttributeError:
		print("No attribute found: <{}>".format(val))
		
print("file: {}".format(__file__))

frame = inspect.stack()
print("frame:", frame)
module = inspect.getmodule(frame[0])
print("module:", module)
filename = module.__file__
print("filename:", filename)
import math

x = math.sin(1)
print(traceback.format_stack())

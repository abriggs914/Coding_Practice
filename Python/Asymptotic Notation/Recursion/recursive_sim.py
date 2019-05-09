def sum_to_one_iter(n):
  result = 1
  call_stack = []
  
  while n != 1:
    execution_context = {"n_value": n}
    call_stack.append(execution_context)
    n -= 1
    print(call_stack)
  print("BASE CASE REACHED")
  while len(call_stack) > 0:
    return_value = call_stack.pop()#call_stack[-1]
    print(call_stack)
    result += return_value["n_value"]
    print("Adding",return_value["n_value"],"to",result)
  return result, call_stack

sum_to_one_iter(4)

#------------------------------------------------------------------------------------------------------------------------------------

# Define sum_to_one() below...

def sum_to_one_rec(n):
  while n > 1:
    print("Recursing with input: {0}".format(n))
    return sum_to_one_rec(n-1) + n
  return n

# uncomment when you're ready to test
print(sum_to_one_rec(7))
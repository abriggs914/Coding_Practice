#1.
#Now that we’ve gotten our sort working let’s test it out with some new data.
#Run radix_sort on unsorted_list.
#2.
#What? IndexError? Did we forget something?
#We did! Some of the numbers that we’re sorting are going to be shorter than other numbers.
#We can fix it though! First, we should comment out the line we added to test the sort.
#Add a comment with #:
#neat_code = 20 + cool_function()
# This is a comment
#3.
#Where we defined digit to be the value of number_as_a_string at index index we need to now wrap that definition in a try block.
#Add a try block and, indented in that block, leave your original definition of digit.
#4.
#After the try block, we’ll want to handle the possibility of an IndexError. What does it mean if we get an index error here?
#It means the value for number at index is actually 0.
#Handle the exception by adding an except IndexError block, in this case assigning digit to be 0.
#5.
#Excellent! Now let’s try uncommenting the line where we sort unordered_list. Print out the results.
#6.
#Great job! We created an algorithm that:
#Takes numbers in an input list.
#Passes through each digit in those numbers, from least to most significant.
#Looks at the values of those digits.
#Buckets the input list according to those digits.
#Renders the results from that bucketing.
#Repeats this process until the list is sorted.
#And that’s what a radix sort does! Feel free to play around with the solution code, see if there’s anything you can improve about the code or a different way of writing it you want to try.
def radix_sort(to_be_sorted):
  maximum_value = max(to_be_sorted)
  max_exponent = len(str(maximum_value))
  being_sorted = to_be_sorted[:]

  for exponent in range(max_exponent):
    position = exponent + 1
    index = -position

    digits = [[] for i in range(10)]

    for number in being_sorted:
      number_as_a_string = str(number)
      try:
        digit = number_as_a_string[index]
      except IndexError:
        digit = 0      
      digit = int(digit)

      digits[digit].append(number)

    being_sorted = []
    for numeral in digits:
      being_sorted.extend(numeral)

  return being_sorted

unsorted_list = [830, 921, 163, 373, 961, 559, 89, 199, 535, 959, 40, 641, 355, 689, 621, 183, 182, 524, 1]
print(radix_sort(unsorted_list))

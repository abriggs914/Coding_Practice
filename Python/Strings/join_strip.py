#They sent over another list containing all the lines to the Audre Lorde poem, Love, Maybe. They want you to join together all of the lines into a single string that can be used to display the poem again, but this time, you’ve noticed that the list contains a ton of unnecessary whitespace that doesn’t appear in the actual poem.
#First, use .strip() on each line in the list to remove the unnecessary whitespace and save it as a new list love_maybe_lines_stripped.
#.join() the lines in love_maybe_lines_stripped together into one large multi-line string, love_maybe_full, that can be printed to display the poem.
#Each line of the poem should show up on its own line.
#Print love_maybe_full.

love_maybe_lines = ['Always    ', '     in the middle of our bloodiest battles  ', 'you lay down your arms', '           like flowering mines    ','\n' ,'   to conquer me home.    ']

love_maybe_lines_strip = ''
for i in range(len(love_maybe_lines)):
  love_maybe_lines_strip += love_maybe_lines[i].strip()
  if(i < len(love_maybe_lines)-1):
    love_maybe_lines_strip += '\n'

print(love_maybe_lines_strip)
love_maybe_lines_stripped = [line.strip() for line in love_maybe_lines]
love_maybe_full = '\n'.join(love_maybe_lines_stripped)
print(love_maybe_full)
print(love_maybe_full == love_maybe_lines_strip)


def poem_title_card(poet, title):
  return 'The poem \"{}\" is written by {}.'.format(title,poet)

print(poem_title_card("Walt Whitman", "I Hear America Singing"))

#The function poem_description is supposed to use .format() to print out some quick information about a poem, but it seems to be causing some errors currently.
#Fix the function by using keywords in the .format() method.
#Run poem_description with the following arguments and save the results to the variable my_beard_description:
#author = "Shel Silverstein"
#title = "My Beard"
#original_work = "Where the Sidewalk Ends"
#publishing_date = "1974"

def poem_description(publishing_date, author, title, original_work):
  poem_desc = "The poem {title} by {author} was originally published in {original_work} in {publishing_date}.".format(title = title, author = author, original_work = original_work, publishing_date = publishing_date)
  return poem_desc

author = "Shel Silverstein"
title = "My Beard"
original_work = "Where the Sidewalk Ends"
publishing_date = "1974"
my_beard_description = poem_description(publishing_date, author, title, original_work)

suitcase = ['shirt', 'shirt', 'pants', 'pants', 'pajamas', 'books']
#Create a new list called start containing the first 3 elements of suitcase.
start = suitcase[:3]
#Create a new list called end containing the final two elements of suitcase.
end = suitcase[-2:]

votes = ['Jake', 'Jake', 'Laurie', 'Laurie', 'Laurie', 'Jake', 'Jake', 'Jake', 'Laurie', 'Cassie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie']
#Mrs. WIlson’s class is voting for class president. She has saved each student’s vote into the list votes.
#Use count to determine how many students voted for 'Jake'. Save your answer as jake_votes.
jake_votes = votes.count('Jake')
#Use print to examine jake_votes.
print(jake_votes)


### Exercise 1 & 2 ###
addresses = ['221 B Baker St.', '42 Wallaby Way', '12 Grimmauld Place', '742 Evergreen Terrace', '1600 Pennsylvania Ave', '10 Downing St.']
# Sort addresses here:
#Use sort to sort addresses.
addresses.sort()
#Use print to see how addresses changed.
print(addresses)
### Exercise 3 ###
names = ['Ron', 'Hermione', 'Harry', 'Albus', 'Sirius']
#Remove the # in front of the line sort(names). Edit this line so that it runs without producing a NameError.
names.sort()

### Exercise 4 ###
cities = ['London', 'Paris', 'Rome', 'Los Angeles', 'New York']
sorted_cities = cities.sort()
#Use print to examine sorted_cities. Why is it not the sorted version of cities?
print(sorted_cities)


games = ['Portal', 'Minecraft', 'Pacman', 'Tetris', 'The Sims', 'Pokemon']
#Use sorted to order games and create a new list called games_sorted.
games_sorted = sorted(games)
print(games)
print(games_sorted)


inventory = ['twin bed', 'twin bed', 'headboard', 'queen bed', 'king bed', 'dresser', 'dresser', 'table', 'table', 'nightstand', 'nightstand', 'king bed', 'king bed', 'twin bed', 'twin bed', 'sheets', 'sheets', 'pillow', 'pillow']
#inventory is a list of items that are in the warehouse for Bob’s Furniture. How many items are in the warehouse?
#Save your answer to inventory_len.
inventory_len = len(inventory)
#Select the first element in inventory. Save it to the variable first.
first = inventory[0]
#Select the last item from inventory and save it to the variable last.
last = inventory[-1]
#Select items from the inventory starting at index 2 and up to, but not including, index 6.
#Save your answer to inventory_2_6.
inventory_2_6 = inventory[2:6]
#Select the first 3 items of inventory and save it to the variable first_3.
first_3 = inventory[:3]
#How many 'twin bed's are in inventory? Save your answer to twin_beds.
twin_beds = inventory.count('twin bed')
#Sort inventory using .sort().
inventory.sort()
print(inventory)


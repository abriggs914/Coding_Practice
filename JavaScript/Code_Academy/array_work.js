const groceryList = ['orange juice', 'bananas', 'coffee beans', 'brown rice', 'pasta', 'coconut oil', 'plantains'];
 /*
 push - add to end of array
 pop - remove from end of array
 shift - remove from fron of array
 unshift - add to front of array
 slice - provide a range to pull out of array
 indexof - returns the index of piven paramater
 */


groceryList.shift();
console.log(groceryList);
groceryList.unshift('popcorn');
console.log(groceryList);
console.log(groceryList.slice(1,4));
console.log(groceryList);
const pastaIndex = groceryList.indexOf('pasta');
console.log(pastaIndex);
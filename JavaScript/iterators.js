const fruits = ['mango', 'papaya', 'pineapple', 'apple'];

// Iterate over fruits below

const foo = food => {console.log('I want to eat a ' + food);}
fruits.forEach(foo);
/* => */
/*
I want to eat a mango
I want to eat a papaya
I want to eat a pineaapple
I want to eat a apple
*/

//////////////////////////////////////////////////////////////////////////

const animals = ['Hen', 'elephant', 'llama', 'leopard', 'ostrich', 'Whale', 'octopus', 'rabbit', 'lion', 'dog'];

// Create the secretMessage array below
const secretMessage = animals.map(a => {return a[0];});

console.log(secretMessage.join(''));

const bigNumbers = [100, 200, 300, 400, 500];

// Create the smallNumbers array below
const smallNumbers = bigNumbers.map(num => {return num / 100;});
console.log(smallNumbers);

/* => */
/*
HelloWorld
[ 1, 2, 3, 4, 5 ]
*/

//////////////////////////////////////////////////////////////////////////

const randomNumbers = [375, 200, 3.14, 7, 13, 852];

// Call .filter() on randomNumbers below
const smallNumbers = randomNumbers.filter(num => {return num < 250;});
console.log(smallNumbers); /*Call the .filter() method on randomNumbers to return values that are less than 250. Save them to a new array called smallNumbers, declared with const.*/

const favoriteWords = ['nostalgia', 'hyperbole', 'fervent', 'esoteric', 'serene'];


// Call .filter() on favoriteWords below
const longFavoriteWords = favoriteWords.filter(word => {return word.length > 7;});
console.log(favoriteWords);

/* => */
/*
[ 200, 3.14, 7, 13 ]
[ 'nostalgia', 'hyperbole', 'fervent', 'esoteric', 'serene' ]
*/

//////////////////////////////////////////////////////////////////////////

const animals = ['hippo', 'tiger', 'lion', 'seal', 'cheetah', 'monkey', 'salamander', 'elephant'];

const foundAnimal = animals.findIndex(a => {return a === 'elephant';});
const startsWithS = animals.findIndex(a => {return a[0] === 's';});
console.log(foundAnimal);
console.log(startsWithS);

/* => */
/*
7
3
*/

//////////////////////////////////////////////////////////////////////////

const newNumbers = [1, 3, 5, 7];
const newSum = newNumbers.reduce((accumulator, currentValue) => {
  console.log('The value of accumulator: ', accumulator);
  console.log('The value of currentValue: ', currentValue);
  return accumulator + currentValue;
}, 10);
console.log(newSum);

/* => */
/*
The value of accumulator:  10
The value of currentValue:  1
The value of accumulator:  11
The value of currentValue:  3
The value of accumulator:  14
The value of currentValue:  5
The value of accumulator:  19
The value of currentValue:  7
26
*/

//////////////////////////////////////////////////////////////////////////

const words = ['unique', 'uncanny', 'pique', 'oxymoron', 'guise'];

// Something is missing in the method call below

console.log(words.some((word) => {
  return word.length < 6;
}));

// Use filter to create a new array
const interestingWords = words.filter(word => {
  return word.length > 5;
});


// Make sure to uncomment the code below and fix the incorrect code before running it

console.log(interestingWords.every((word) => {return word.length > 5;}));

/* => */
/*
true
true
*/

//////////////////////////////////////////////////////////////////////////

const cities = ['Orlando', 'Dubai', 'Edinburgh', 'Chennai', 'Accra', 'Denver', 'Eskisehir', 'Medellin', 'Yokohama'];

const nums = [1, 50, 75, 200, 350, 525, 1000];

//  Choose a method that will return undefined
cities.forEach(city => console.log('Have you visited ' + city + '?'));

// Choose a method that will return a new array
const longCities = cities.filter(city => city.length > 7);

// Choose a method that will return a single value
const word = cities.reduce((acc, currVal) => {
  return acc + currVal[0]
}, "C");

console.log(word)

// Choose a method that will return a new array
const smallerNums = nums.map(num => num - 5);

// Choose a method that will return a boolean value
nums.every(num => num < 0);

/* => */
/*
Have you visited Orlando?
Have you visited Dubai?
Have you visited Edinburgh?
Have you visited Chennai?
Have you visited Accra?
Have you visited Denver?
Have you visited Eskisehir?
Have you visited Medellin?
Have you visited Yokohama?
CODECADEMY
*/

///////////////////////////////////////////////////////////////////////
.forEach() is used to execute the same code on every element in an array but does not change the
	array and returns undefined.
	
.map() executes the same code on every element in an array and returns a new array with the updated elements.

.filter() checks every element in an array to see if it meets certain criteria and returns a new
	array with the elements that return truthy for the criteria.
	
.findIndex() returns the index of the first element of an array which satisfies a condition in the
	callback function. It returns -1 if none of the elements in the array satisfies the condition.
	
.reduce() iterates through an array and takes the values of the elements and returns a single value.

All iterator methods takes a callback function that can be pre-defined, or a function expression,
	or an arrow function.
	
You can visit the Mozilla Developer Network to learn more about iterator methods (and all other 
	parts of JavaScript!).
//////////////////////////////////////////////////////////////////////
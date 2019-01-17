// Write your code here:
const reverseArray = arr => {
  let newArr = [];
  for (let i = 0; i < arr.length; i++){
    newArr.unshift(arr[i]);
  }
  return newArr;
}

// When you're ready to test your code, uncomment the below and run:
 
const sentence = ['sense.','make', 'all', 'will', 'This'];

console.log(reverseArray(sentence)) 
// Should print ['This', 'will', 'all', 'make', 'sense.'];

/////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function greetAliens(arr) {
  for(let i = 0; i < arr.length; i++){
  	console.log('Oh powerful ' + arr[i] + ', we humans offer our unconditional surrender!');
  }
}

// When you're ready to test your code, uncomment the below and run:

const aliens = ["Blorgous", "Glamyx", "Wegord", "SpaceKing"];

greetAliens(aliens);

/////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function convertToBaby(arr){
  let newarr =[];
  for(let i = 0; i < arr.length; i++){
    newarr[i] = 'baby ' + arr[i];
  }
  return newarr
}

// When you're ready to test your code, uncomment the below and run:
const animals = ['panda', 'turtle', 'giraffe', 'hippo', 'sloth', 'human'];

console.log(convertToBaby(animals)) 

/////////////////////////////////////////////////////////////////////////////////////////////

const numbers = [5, 3, 9, 30];

const smallestPowerOfTwo = arr => {
      let results = [];
      // The 'outer' for loop - loops through each element in the array
      for (let i = 0; i < arr.length; i++) {
            number = arr[i];

            // The 'inner' while loop - searches for smallest power of 2 greater than the given number
            let j = i;
        		i = 1;
            while (i < number) {
                  i = i * 2;
            }
            results.push(i);
        		i = j;
      }
      return results
}

console.log(smallestPowerOfTwo(numbers)) 
// Should print the returned array [ 8, 4, 16, 32 ] instead prints the returned array [8]

///////////////////////////////////////////////////////////////////////////////////////////////////

const veggies = ['broccoli', 'spinach', 'cauliflower', 'broccoflower'];

const politelyDecline = (veg) => {
      console.log('No ' + veg + ' please. I will have pizza with extra cheese.');
}

// Write your code here:

const declineEverything = arr => {
  arr.forEach(politelyDecline);
}

function accept(item){
  console.log(`Ok, I guess I will eat some ${item}.`);
}

function acceptEverything (arr) {
  arr.forEach(accept);
}


declineEverything(veggies);
acceptEverything(veggies);

/* => */
/*
No broccoli please. I will have pizza with extra cheese.
No spinach please. I will have pizza with extra cheese.
No cauliflower please. I will have pizza with extra cheese.
No broccoflower please. I will have pizza with extra cheese.
Ok, I guess I will eat some broccoli.
Ok, I guess I will eat some spinach.
Ok, I guess I will eat some cauliflower.
Ok, I guess I will eat some broccoflower.
*/

/////////////////////////////////////////////////////////////////////////////////////////////

const numbers = [2, 7, 9, 171, 52, 33, 14]

const toSquare = num => num * num

// Write your code here:

function squareNums(arr){
  return arr.map(igh => {return toSquare(igh)});
}

console.log(squareNums(numbers));

/* => */
/*
[ 4, 49, 81, 29241, 2704, 1089, 196 ]
*/

////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function shoutGreetings(arr){
  return arr.map(item => {return item.toUpperCase() + '!';});
}


// Feel free to uncomment out the code below to test your function!
const greetings = ['hello', 'hi', 'heya', 'oi', 'hey', 'yo'];

console.log(shoutGreetings(greetings))
// Should print [ 'HELLO!', 'HI!', 'HEYA!', 'OI!', 'HEY!', 'YO!' ]

/////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function sortYears(arr){
  return arr.sort().reverse();
}

// Feel free to uncomment the below code to test your function:
const years = [1970, 1999, 1951, 1982, 1963, 2011, 2018, 1922]

console.log(sortYears(years))
// Should print [ 2018, 2011, 1999, 1982, 1970, 1963, 1951, 1922 ]

//////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function justCoolStuff(a, b){
  return a.filter(a1 => {
    return b.includes(a1);});
}

// Feel free to uncomment the code below to test your function
const coolStuff = ['gameboys', 'skateboards', 'backwards hats', 'fruit-by-the-foot', 'pogs', 'my room', 'temporary tattoos'];

const myStuff = [ 'rules', 'fruit-by-the-foot', 'wedgies', 'sweaters', 'skateboards', 'family-night', 'my room', 'braces', 'the information superhighway']; 

console.log(justCoolStuff(myStuff, coolStuff))
// Should print [ 'fruit-by-the-foot', 'skateboards', 'my room' ]

/////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:
function isTheDinnerVegan(arr){
  return arr.every(item => {return item['source'] === 'plant'})
}
// Feel free to comment out the code below to test your function
const dinner = [{name: 'hamburger', source: 'meat'}, {name: 'cheese', source: 'dairy'}, {name: 'ketchup', source:'plant'}, {name: 'bun', source: 'plant'}, {name: 'dessert twinkies', source:'unknown'}];

console.log(isTheDinnerVegan(dinner))
// Should print false

///////////////////////////////////////////////////////////////////////////////////////////

const speciesArray = [ {speciesName:'shark', numTeeth:50}, {speciesName:'dog', numTeeth:42}, {speciesName:'alligator', numTeeth:80}, {speciesName:'human', numTeeth:32}];

// Write your code here:
const compareTeeth = (speciesObj1, speciesObj2) => speciesObj1.numTeeth > speciesObj2.numTeeth

const sortSpeciesByTeeth = arr => {
	//return arr.map(item1 item2 => {return arr.sort(compareTeeth(item['numTeeth']));}); 
    return arr.sort(compareTeeth);
}
// Feel free to comment out the code below when you're ready to test your function!
console.log(compareTeeth(speciesArray[0], speciesArray[1]));
console.log(sortSpeciesByTeeth(speciesArray))
/*
// Should print [ { speciesName: 'human', numTeeth: 32 },
  { speciesName: 'dog', numTeeth: 42 },
  { speciesName: 'shark', numTeeth: 50 },
  { speciesName: 'alligator', numTeeth: 80 } ]
*/

///////////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:

function findMyKeys(arr){
  if(arr.includes('keys')){
    return arr.indexOf('keys');
  }
  else{
    return -1;
  }
}
// Feel free to comment out the code below to test your function
const randomStuff = ['credit card', 'screwdriver', 'receipt', 'gum', 'keys', 'used gum', 'plastic spoon'];

console.log(findMyKeys(randomStuff))
// Should print 4

//////////////////////////////////////////////////////////////////////////////////////////////

// Write your code here:

const dogFactory = (name, breed, weight) => {
  return {
    _name: name,
    _breed: breed,
    _weight: weight,
    get name(){
      return this._name;
    },
    get breed(){
      return this._breed;
    },
    get weight(){
      return this._weight;
    },
    set name(nameIn){
      this._name = nameIn;
    },
    set breed(breedIn){
      this._breed = breedIn;
    },
    set weight(weightIn){
      this._weight = weightIn;
    },
    bark(){
      return 'ruff! ruff!';
    },
    eatTooManyTreats(){
      return ++this.weight;
    }
  }
}

const fido = dogFactory('Fido', 'German Shepard', 45);
console.log(fido.bark());
console.log(fido.eatTooManyTreats());
console.log(fido.eatTooManyTreats());

/* => */
/*
ruff! ruff!
46
47
*/
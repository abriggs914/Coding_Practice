let spaceship = {
  'Fuel Type' : 'Turbo Fuel',
  homePlanet : 'Earth',
  color: 'silver',
  'Secret Mission' : 'Discover life outside of Earth.'
};

// Write your code below
spaceship.color = 'glorious gold';
spaceship.numEngines = 8;
delete spaceship['Secret Mission'];

///////////////////////////////////////////////////////////////////////
let spaceship = {
  passengers: null,
  telescope: {
    yearBuilt: 2018,
    model: "91031-XLT",
    focalLength: 2032 
  },
  crew: {
    captain: { 
      name: 'Sandra', 
      degree: 'Computer Engineering', 
      encourageTeam() { console.log('We got this!') },
     'favorite foods': ['cookies', 'cakes', 'candy', 'spinach'] }
  },
  engine: {
    model: "Nimbus2000"
  },
  nanoelectronics: {
    computer: {
      terabytes: 100,
      monitors: "HD"
    },
    backup: {
      battery: "Lithium",
      terabytes: 50
    }
  }
}; 
let capFave = spaceship.crew.captain['favorite foods'][0]; 
spaceship.passengers = [{name: 'Space Dog'}];
let firstPassenger = spaceship.passengers[0];

////////////////////////////////////////////////////////////////////////////////

let spaceship = {
  'Fuel Type' : 'Turbo Fuel',
  homePlanet : 'Earth'
};

// Write your code below
function greenEnergy(obj) {
  obj['Fuel Type'] = 'avocado oil';
}

function remotelyDisable(obj) {
  obj['disabled'] = true;  
}

console.log('Before');
console.log(spaceship);
greenEnergy(spaceship);
remotelyDisable(spaceship);
console.log('After');
console.log(spaceship);

/* => */
/*
Before
{ 'Fuel Type': 'Turbo Fuel', homePlanet: 'Earth' }
After
{ 'Fuel Type': 'avocado oil',
  homePlanet: 'Earth',
  disabled: true }
*/

//////////////////////////////////////////////////////////////////////

let spaceship = {
    crew: {
    captain: { 
        name: 'Lily', 
        degree: 'Computer Engineering', 
        cheerTeam() { console.log('You got this!') } 
        },
    'chief officer': { 
        name: 'Dan', 
        degree: 'Aerospace Engineering', 
        agree() { console.log('I agree, captain!') } 
        },
    medic: { 
        name: 'Clementine', 
        degree: 'Physics', 
        announce() { console.log(`Jets on!`) } },
    translator: {
        name: 'Shauna', 
        degree: 'Conservation Science', 
        powerFuel() { console.log('The tank is full!') } 
        }
    }
}; 

// Write your code below
let y = 0;
for (let curr in spaceship.crew){
  switch(y){
    case 0  : console.log(`${curr}: ${spaceship.crew.captain.name}`);
      break;
    case 1  : console.log(`${curr}: ${spaceship.crew['chief officer'].name}`);
      break;
    case 2  : console.log(`${curr}: ${spaceship.crew.medic.name}`);
      break;
    case 3  : console.log(`${curr}: ${spaceship.crew.translator.name}`);
      break;
    default : console.log('SOMETHING WENT WRONG');
      break;
  }
  y++;
}

y = 0;
for (let curr in spaceship.crew){
  switch(y){
    case 0  : console.log(`${spaceship.crew.captain.name}: ${spaceship.crew.captain.degree}`);
      break;
    case 1  : console.log(`${spaceship.crew['chief officer'].name}: ${spaceship.crew['chief officer'].degree}`);
      break;
    case 2  : console.log(`${spaceship.crew.medic.name}: ${spaceship.crew.medic.degree}`);
      break;
    case 3  : console.log(`${spaceship.crew.translator.name}: ${spaceship.crew.translator.degree}`);
      break;
    default : console.log('SOMETHING WENT WRONG');
      break;
  }
  y++;
}

/* => */
/*
captain: Lily
chief officer: Dan
medic: Clementine
translator: Shauna
Lily: Computer Engineering
Dan: Aerospace Engineering
Clementine: Physics
Shauna: Conservation Science
*/

/*
Let's review what we learned in this lesson:

Objects store collections of key-value pairs.
Each key-value pair is a property—when a property is a function it is known as a method.

An object literal is composed of comma-separated key-value pairs surrounded by curly braces.

You can access, add or edit a property within an object by using dot notation or bracket notation.

We can add methods to our object literals using key-value syntax with anonymous function
	expressions as values or by using the new ES6 method syntax.
	
We can navigate complex, nested objects by chaining operators.

Objects are mutable—we can change their properties even when they're declared with const.

Objects are passed by reference— when we make changes to an object passed into a function,
	those changes are permanent.
	
We can iterate through objects using the For...in syntax.
*/
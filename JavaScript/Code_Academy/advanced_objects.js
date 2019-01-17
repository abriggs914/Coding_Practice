const robot = {
  _model: '1E78V2',
  _energyLevel: 100,
  get energyLevel () {
    if (typeof this._energyLevel === 'number'){
      return 'My current energy level is ' + this._energyLevel;
    }
    else {
      return 'System malfunction: cannot retrieve energy level';
    }
  }
};
// when using a get, I dont have use the () method tag
console.log(robot.energyLevel);

////////////////////////////////////////////////////////////////////

const robot2 = {
  _model: '1E78V2',
  _energyLevel: 100,
  _numOfSensors: 15,
  get numOfSensors(){
    if(typeof this._numOfSensors === 'number'){
      return this._numOfSensors;
    } else {
      return 'Sensors are currently down.'
    }
  },
  set numOfSensors (num) {
    if(typeof num === 'number'){
      if(num >= 0){
        this._numOfSensors = num;
      }
    }
    else{
      console.log('Pass in a number that is greater than or equal to 0');
    }
  }  
};

robot2.numOfSensors = 100;
console.log(robot2.numOfSensors);

///////////////////////////////////////////////////////////////////////////////////////

const robotFactory = (model, mobile) => {
  return {
    model : model,
    mobile : mobile,
    beep() {
      console.log('Beep Boop');
    }
  };
}

const tinCan = robotFactory('P-500', true);
tinCan.beep();

//////////////////////////////////////////////////////////////////////////////////

/*
* Destructured version of the above ^
*/

const robotFactory = (model, mobile) => {
  return {
    model,
    mobile,
    beep() {
      console.log('Beep Boop');
    },
  }
};

// To check that the property value shorthand technique worked:
const newRobot = robotFactory('P-501', false)
console.log(newRobot.model)
console.log(newRobot.mobile)

/////////////////////////////////////////////////////////////////////////////////

const robot = {
  model: '1E78V2',
  energyLevel: 100,
  functionality: {
    beep() {
      console.log('Beep Boop');
    },
    fireLaser() {
      console.log('Pew Pew');
    },
  }
};

const { functionality } = robot; /*Use destructured assignment to create a const
	variable named functionality that extracts the functionality property of robot.*/
functionality.beep(); /*Since functionality is referencing robot.functionality we
	can call the methods available to robot.functionality simply through functionality.

Take advantage of this shortcut and call the .beep() method on functionality.*/

////////////////////////////////////////////////////////////////////////////////////

const robot3 = {
	model: 'SAL-1000',
  mobile: true,
  sentient: false,
  armor: 'Steel-plated',
  energyLevel: 75
};

// What is missing in the following method call?
const robotKeys = Object.keys(robot3);
/*In main.js there is an object, robot. We'd like to grab the property names,
	otherwise known as keys, and save the keys in an array which is assigned
	to robotKeys. However, there's something missing in the method call.

Find out what we have to include by reading MDN's Object.keys() documentation.*/
console.log(robotKeys);

// Declare robotEntries below this line:
const robotEntries = Object.entries(robot3);
/*Object.entries() will also return an array, but the array will contain more
	arrays that have both the key and value of the properties in an object.

Declare a const variable named robotEntries and assign to it the entries of 
	robot by calling Object.entries().

To find how to use Object.entries(), read the documentation at MDN.*/
console.log(robotEntries);

// Declare newRobot below this line:
const newRobot = Object.assign({laserBlaster: true, voiceRecognition: true}, robot3);
/*Now what if we want another object that has the properties of robot but 
	with a few additional properties. Object.assign() sounds like a great method
	to use, but like the previous examples we should check Object.assign() 
	documentation at MDN.

Declare a const variable named newRobot. newRobot will be a new object that 
	has all the properties of robot and the properties in the following 
	object: {laserBlaster: true, voiceRecognition: true}. Make sure that you
	are not changing the robot object!*/
console.log(newRobot);

//////////////////////////////////////////////////////////////////////////////////////////////////////

const car = {
  numDoors: 4,
  isDirty: true,
  color: 'red'
}

for (let key in car) {
  console.log(key)
}

/* => */
/*
numDoors
isDirty
color
*/

//////////////////////////////////////////////////////////////////////////////////////////////////////
/*Start by creating an empty menu object.*/
const menu = {
  /*
Add a _courses property to your menu object and set its value to an empty object.
	This property will ultimately contain a mapping between each course and the 
	dishes available to order in that course.*/
  _courses: {
    /*
Create three properties inside the _courses object called appetizers, mains, and
	desserts. Each one of these should initialize to an empty array.*/
    appetizers: [],
    mains: [],
    desserts: []
  },
  /*Create getter and setter methods for the appetizers, mains, and desserts properties.*/
  get appetizers(){
    return this._courses['appetizers'];
  },
  get mains(){
    return this._courses['mains'];
  },
  get desserts(){
    return this._courses['desserts'];
  },
  set appetizers(appetizerIn){
    this._courses['appetizers'] = appetizerIn;
    
  },
  set mains(mainIn){
    this._courses['mains'] = mainIn;
    
  },
  set desserts(dessertIn){
    this._courses['desserts'] = dessertIn;
  },
/*Inside your menu object, create an empty getter method for the _courses property.*/
  get courses(){
    /*Inside the courses getter method, return an object that contains key/value 
		pairs for appetizers, mains, and desserts.*/
    return {
      appetizers: this._courses.appetizers,
      mains: this._courses.mains,
      desserts: this._courses.desserts
    };
  },
  /*
Inside the menu object, we are going to create a method called .addDishToCourse() which
	will be used to add a new dish to the specified course on the menu.

The method should take in three parameters: the courseName, the dishName , and the dishPrice.*/
  addDishToCourse(courseName, dishName, dishPrice){
    /*The .addDishToCourse() method should create an object called dish which has a name
		and price which it gets from the parameters.

The method should then push this dish object into the appropriate array in your menu's 
	_courses object based on what courseName was passed in.*/
    const dish = {
      name: dishName,
      price: dishPrice,
    }
    this._courses[courseName].push(dish);
  },
  getRandomDishFromCourse(courseName){
    const dishes = this._courses[courseName];
    const index = Math.floor(Math.random() * dishes.length);
    return dishes[index];
  },
  /*Now, we're going to need another function which will allow us to get a random dish
	from a course on the menu, which will be necessary for generating a random meal.

Create a method inside the menu object called .getRandomDishFromCourse(). It will take 
	in one parameter which is the courseName.*/
  generateRandomMeal(){
    /*There are a few steps in getting the .getRandomDishFromCourse() to work.

Retrieve the array of the given course's dishes from the menu's _courses object and store 
	in a variable called dishes.
Generate a random index by multiplying Math.random() by the length of the dishes array 
	(This will guarantee that the random number will be between 0 and the length of the array)
Round that generated number to a whole number by using Math.floor() on the result.
Return the dish located at that index in dishes.*/
    /*11.
Now that we have a way to get a random dish from a course, we can create a .generateRandomMeal()
	function which will automatically generate a three-course meal for us. The function doesn't 
	need to take any parameters.

The function should create an appetizer variable which should be the result of calling the 
	.getRandomDishFromCourse() method when we pass in an appetizers string to it.
Create a main variable and dessert variable the same way you created the appetizer
	variable, but make sure to pass in the right course type.
Calculates the total price and returns a string that contains the name of each of the dishes 
	and the total price of the meal, formatted as you like.*/
    const appetizer = this.getRandomDishFromCourse('appetizers');
    const main = this.getRandomDishFromCourse('mains');
    const dessert = this.getRandomDishFromCourse('desserts');
  	const totalPrice = appetizer.price + main.price + dessert.price;
  	return `Your meal is ${appetizer.name}, ${main.name}, ${dessert.name}. The price is ${totalPrice}.`;
  }
};

/*Now that we've finished our menu, object, let's use it to create a menu by adding some 
	appetizers, mains, and desserts with the .addDishToCourse() function. Add at least 3 dishes
	to each course (or more if you like!).*/
menu.addDishToCourse('mains', 'Pizza', 2.50);
menu.addDishToCourse('mains', 'Turkey', 6.50);
menu.addDishToCourse('mains', 'Burger', 5.50);
menu.addDishToCourse('appetizers', 'Caesar Salad', 4.25);
menu.addDishToCourse('appetizers', 'Garlic Bread', 3.25);
menu.addDishToCourse('appetizers', 'Pigs in a Blanket', 4.25);
menu.addDishToCourse('desserts', 'Ice Cream', 2.25);
menu.addDishToCourse('desserts', 'Chocolate Cake', 1.75);
menu.addDishToCourse('desserts', 'Apple Pie', 2.50);
/*Once your menu has items inside it, generate a meal by using the .generateRandomMeal() function
	on your menu, and save it to a variable called meal. Lastly, print out your meal variable to see
	what meal was generated for you.*/
const meal = menu.generateRandomMeal();
console.log(meal);
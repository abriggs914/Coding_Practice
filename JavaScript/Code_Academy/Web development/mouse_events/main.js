// These variables store the boxes on the side
let itemOne = document.getElementById('list-item-one');
let itemTwo = document.getElementById('list-item-two');
let itemThree = document.getElementById('list-item-three');
let itemFour = document.getElementById('list-item-four');
let itemFive = document.getElementById('list-item-five');
let resetButton = document.getElementById('reset-button');

// This function programs the "Reset" button to return the boxes to their default styles
let reset = function() {
  itemOne.style.width = ''
  itemTwo .style.backgroundColor = ''
  itemThree.innerHTML = 'The mouse must leave the box to change the text'
  itemFive.hidden = true;
  itemFive.style.display = 'none';
};
resetButton.onclick = reset;

// Write code for the first list item
/*In this exercise, you'll modify the list elements using mouse events. You can use the reset element that is already programmed to set the other list element back to their default styles.

First, create an event handler property on itemOne when the mouse hovers over it.*/
itemOne.onmouseover = function(){
  /*Now, assign an anonymous event handler function that changes the width of itemOne to any size greater or less than 400px.*/
  itemOne.style.width = '600px';
}

// Write code for the second list item
/*Now, create an event handler property on itemTwo when the mouse is released over the element.*/
itemTwo.onmouseup = function(){
  /*Create an event handler function that changes the background color of itemTwo when the mouse is released over the element.*/
  itemTwo.style.backgroundColor = 'red';
}

// Write code for the third list item
/*Next, create an event handler property that fires when the mouse leaves the itemThree element.*/
itemThree.onmouseout = function(){
  /*Create an anonymous event handler function that changes the text of itemThree to 'The mouse has left the element.'.*/
  itemThree.innerHTML = 'The mouse has left the element.';
}

// Write code for the fourth list item
/*Finally, create an event handler property that fires when the mouse is pressed down on itemFour.*/
itemFour.onmousedown = function(){
  /*Create an event handler function that makes the itemFive appear when the mouse is pressed down on itemFour.*/
  itemFive.style.display = 'block';
}

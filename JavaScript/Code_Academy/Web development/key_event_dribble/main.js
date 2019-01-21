let ball = document.getElementById('float-circle');

// Write your code below

/*Now it's time to create a game! Program this code to dribble the ball on the platform using any key on a keyboard. When a user presses a key down, it should lift the ball up. When the user releases the key, the ball should drop.

First, make a function named up that will raise the bottom position of the ball to '250px' above the platform element.*/
const up = () => {
  ball.style.bottom = '250px';
}

/*Next, make a function named down that will run when the ball drops to the platform element. This function should change the bottom position of the ball to '50px'.*/
const down = () => {
  ball.style.bottom = '50px';
}

/*Create an event handler property that runs the up function when a keydown event fires on the document object, or anywhere on the DOM, as the event target.*/
document.onkeydown = up;

/*Create an event handler property that runs the down function when a keyup event fires on the document.

Run your code and play around with the keyboard events to make the ball bounce on the platform. You can try keys like the space bar, letter keys or number keys!*/
document.onkeyup = down;

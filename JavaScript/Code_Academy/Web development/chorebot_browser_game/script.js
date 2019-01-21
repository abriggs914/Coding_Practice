/*Navigate to the script.js file. Create a global variable called doorImage1. Use a JavaScript DOM method to assign this global variable to the HTML element with the id of door1.*/
let doorImage1 = document.getElementById('door1');
/*Now you have three doors and the cursor changes on hover for all three; but only your first door opens. Put JavaScript to work to open those other two doors!

Go to your script.js file and create two new global variables called doorImage2 and doorImage3. Use a JavaScript DOM method to assign these global variables to the HTML elements with the id of door2 and door3 respectively.*/
let doorImage2 = document.getElementById('door2');
let doorImage3 = document.getElementById('door3');

let botDoorPath = 'https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/robot.svg';

let beachDoorPath = 'https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/beach.svg';

let spaceDoorPath = 'https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/space.svg';

let numClosedDoors = 3;

let openDoor1;
let openDoor2;
let openDoor3;

let closedDoorPath = 'https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/closed_door.svg';

let startButton = document.getElementById('start');

let currentlyPlaying = true;

const randomChoreDoorGenerator = () => {
  /* 0, 1, 2 */
  let choreDoor = Math.floor(Math.random()*numClosedDoors);
  if(choreDoor === 0){
    openDoor1 = botDoorPath;
    openDoor2 = beachDoorPath;
    openDoor3 = spaceDoorPath;
  }
  else if (choreDoor === 1){
    openDoor2 = botDoorPath;    
    openDoor3 = beachDoorPath;
    openDoor1 = spaceDoorPath;
  }
  else{
    openDoor3 = botDoorPath;  
    openDoor2 = beachDoorPath;
    openDoor1 = spaceDoorPath;  
  }
}


door1.onclick = () => {
  if(!isClicked(doorImage1) && currentlyPlaying){
  	doorImage1.src = openDoor1;
  	playDoor(doorImage1);
  }
};
door2.onclick = () => {
  if(!isClicked(doorImage2) && currentlyPlaying){
  	doorImage2.src = openDoor2;
  	playDoor(doorImage2);
  }
};
door3.onclick = () => {
  if(!isClicked(doorImage3) && currentlyPlaying){
  	doorImage3.src = openDoor3;
  	playDoor(doorImage3);
  }
};

startButton.onclick = () => {
  if(!currentlyPlaying){
  	startRound();
  }
};

const startRound = () => {
  doorImage1.src = closedDoorPath;
  doorImage2.src = closedDoorPath;
  doorImage3.src = closedDoorPath;
  numClosedDoors = 3;
  startButton.innerHTML = 'Good Luck!';
  currentlyPlaying = true;
  randomChoreDoorGenerator();
}

const isBot = door => {
  //lwt a = document.querySelector('body');
  //a.style.backgroundColor = 'red';
  if(door.src === botDoorPath){
    return true;
  }
  else{
    return false;
  }
}

const isClicked = door => {
  if(door.src === closedDoorPath){
    return false;
  }
  else{
    return true;
  }
}

const playDoor = door => {
  numClosedDoors--;
  if(numClosedDoors === 0){
     gameOver('win');
  }
  else if(isBot(door)){
    gameOver();
  }
}

const gameOver = status => {
  if(status === 'win'){
    startButton.innerHTML = 'You win! Play again?'
  }
  else{
    startButton.innerHTML = 'Game Over! Play again?';
  }
  currentlyPlaying = false;
}

startRound();
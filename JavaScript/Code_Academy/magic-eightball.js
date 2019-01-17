let tool = 'marker';

// Use short circuit evaluation to assign  writingUtensil variable below:
let writingUtensil = tool || 'pen';

console.log(`The ${writingUtensil} is mightier than the sword.`);

let userName = 'Avery';
let userQuestion = 'Will Calgary make the playoffs this year?';
let randomNumber = Math.floor(Math.random() * 8);
let eightBall = '';

userName ? console.log(`Hello, ${userName}`): console.log('Hello!');

switch(randomNumber){
  case 0 : 	eightBall = 'It is certain';
    				break;
  case 1 : 	eightBall = 'It is decidedly so';
    				break;
  case 2 : 	eightBall = 'Reply hazy try again';
    				break;
  case 3 : 	eightBall = 'Cannot predict now';
    				break;
  case 4 : 	eightBall = 'Do not count on it';
    				break;
  case 5 : 	eightBall = 'My sources say no';
    				break;
  case 6 : 	eightBall = 'Outlook not so good';
    				break;
  case 7 : 	eightBall = 'Signs point to yes';
    				break;
}

console.log(`Your name is: ${userName}, and you asked: ${userQuestion}`);
console.log(`The eightBall has spoken: ${eightBall}`);
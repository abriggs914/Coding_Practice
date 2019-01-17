const getComputerChoice = () => {
  let num = Math.floor(Math.random() * 3);
  if(num === 0){
    return 'rock';
  }
  if(num === 1){
    return 'paper';
  }
  return 'scissors'
};

const getUserChoice = userInput => {
  userInput = userInput.toLowerCase();
	if(userInput === 'rock' || userInput === 'paper' || userInput === 'scissors' || userInput === 'bomb'){
  	return userInput;
	}
	else{
		console.log('Error invalid move.');
  	return '';
	}
};

const determineWinner = (userChoice, computerChoice) => {
  if(userChoice === 'bomb'){
    return 'You Win! :)';
  }
  if(userChoice === computerChoice){
    return 'TIE';
  }
  if(userChoice === 'rock'){
    if(computerChoice === 'paper'){
      return 'Computer wins :(';
    }
    return 'You Win! :)';
  }
  if(userChoice === 'paper'){
    if(computerChoice === 'scissors'){
      return 'Computer wins :(';
    }
    return 'You Win! :)';
  }
  if(userChoice === 'scissors'){
    if(computerChoice === 'rock'){
      return 'Computer wins :(';
    }
    return 'You Win! :)';
  }
};

const playGame = () => {
  //let userChoice = getUserChoice('Rock');
  let userChoice = getUserChoice('pApER');
  //let userChoice = getUserChoice('SCISSors');
  //let userChoice = getUserChoice('BOMB');
  let computerChoice = getComputerChoice();
  console.log('userChoice: ' + userChoice);
  console.log('computerChoice: ' + computerChoice);
  console.log(determineWinner(userChoice,computerChoice));
};

//console.log(getUserChoice('RoCk'));
//console.log(getComputerChoice());
//console.log(determineWinner('rock','scissors'));
console.log('Let\'s play!');
playGame();
    
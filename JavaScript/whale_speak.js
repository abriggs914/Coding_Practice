//let input = 'This is a Silly assignment!';
let input = 'turpentine and turtles';
const vowels = ['a','e','i','o','u'];
let resultArray = [];

input.toLowerCase();
for(let i = 0; i < input.length; i++){
  for(let j = 0; j < vowels.length; j++){
  	if(vowels[j] === input[i]){
      resultArray.push(vowels[j]);
      if(input[i] === 'e' || input[i] === 'u'){
      	resultArray.push(input[i]);        
      }
      console.log(input[i]);
    }
  }
}
console.log(resultArray.join('').toUpperCase());

/*
turpentine and turtles ->
UUEEIEEAUUEE
*/
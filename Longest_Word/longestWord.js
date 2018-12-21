var fs = require("fs");
var words = fs.readFileSync("words.txt").toString();
words = words.split("\n");

// console.log(words[0]);

var badLetters = /[!@#$%^&*()-_'+t]/;
var longestAcceptableWord = "";

for(var testWord of words){
  if(testWord.length <= longestAcceptableWord.length){
    continue;
  }
  if(testWord.match(badLetters)){
    continue;
  }
  // console.log(testWord);
  longestAcceptableWord = testWord;
}

console.log(longestAcceptableWord);

// My Age
let myAge = 23;
// dog year conversion rate
let earlyYears = 2;
earlyYears = earlyYears * 10.5;
// Stores the remaining years
let laterYears = myAge - 2;
// calculating dog years
laterYears *= 4;
console.log(`early years: ${earlyYears}`);
console.log(`later years: ${laterYears}`);
// Total age in dog years
let myAgeInDogYears = earlyYears + laterYears;
// My name in lower case
let myName = 'Avery'.toLowerCase();
console.log(`My name is ${myName}. I am ${myAge} years old in human years which is ${myAgeInDogYears} years old in dog years.`);
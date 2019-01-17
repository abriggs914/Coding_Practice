// Value of Kelvin
const kelvin = 293;
// Value of Celsius
let celsius = kelvin - 273;
// Converting celsius to farenheit
// Using floor() to avoid decimals
let farenheit = Math.floor((celsius * (9/5)) + 32);

console.log(`The temperature is ${farenheit} degrees Farenheit`);

let newton = Math.floor(celsius * (33/100));

console.log(`The temperature is ${newton} degrees Newton`);
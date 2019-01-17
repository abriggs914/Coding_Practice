const indexIsSmallerThanElement = (element, index) => index < element;

const indexComp = (size, index) => index < size;

const _ = {
  clamp(number, lower, upper){
    let lowerClampedValue = Math.max(number, lower);
    let clampedValue = Math.min(lowerClampedValue, upper);
    return clampedValue;
  },
  
  inRange (number, start, end) {
    let a = typeof number; 
    let b = typeof start; 
    let c = typeof end; 
    if(a !== 'number' || b !== 'number' ){
      return false
    }
    // if no end given, set end to start and start to 0 (0 -> end)
    if (c === 'undefined'){
      end = start;
      start = 0;
    }
    //swap start and end because end < start
    if(end < start){ 
      let t = end;
      end = start;
      start = t;
    }
    return (number <= end && number >= start);
  },
  
  words (arr) {
    return arr.split(' ');
  },
  
  pad (string, len) {
    if(string.length >= len){
      return string;
    }
    let diff = len - string.length;
    let diffHalf = Math.floor(diff/2);
    diff = diff % 2;
    let padding = ' '.repeat(diffHalf);
    let oddPadding = ' '.repeat(diff);
    return padding + string + padding + oddPadding;
  },
  
  has (obj, key) {
    return (typeof obj[key] !== 'undefined');
  },
  
  invert (obj) {
    let newObj = {};
    for(item in obj){
      let originalVal = obj[item];
      newObj[originalVal] = item;
    }
  	return newObj;
  },
  
  findKey (object, predicate) {
    let truthy;
    for(obj in object){
      let value = object[obj];
      truthy = (predicate(value)? obj : undefined)
      if(truthy){
        return truthy;
      }
    }
    return truthy;
  },
  
  drop (arr, num) {
    if(typeof num === 'undefined'){
      arr.shift();
    }
    else {
    	for(let i = 0; i < arr.length && i < num; i++){
      	arr.shift();
    	}
    }
    return arr
    // or consider using slice()
  },
  
  dropWhile (arr, predicate) {
    let len = arr.length;
    	for(let i = 0; i < len && predicate(arr[i], i, arr); i++){
     		arr.shift();
        i--;
        len--;
    	}
    return arr
  },
  
  dropWhile2 (arr, predicate) {
    let dropNumber = arr.findIndex((element, index) => {
      return !predicate(element, index, arr);
    });
    let droppedArray = this.drop(arr, dropNumber);
    return droppedArray;
  },
  
  chunk (arr, size = 1) {
  	let array = [];
    let len = arr.length;
    let count = 0;
    for(let i = 0; i < size; i++){
      array.push(arr.slice(0, size));
      let j = 0;
      while(j < size){
        arr.shift();
        j++;
      }
      count += j;
    }
    if(count < len){
      array.push(arr);
    }
    return array;
  }
};


// Do not write or modify code below this line.
module.exports = _;
let allCourses = [];

const comparePreReqs = (obj1, obj2) => {
  let a = obj1.preReqs.length;
  let b = obj2.preReqs.length;
  if(a > b){
    return a > b;
  }
  // else if (a === b){
  //   return compareCourseHours(obj1,obj2);
  // }
}

const compareCourseHours = (obj1, obj2) => {return obj1.ch - obj2.ch;}

const secondSort = (arr, currSize = 0) => {
  let mini = [];
  let max = arr.length;
  let j = 0;
  console.log("currSize: ",currSize);
  console.log("Starting: ",arr);
  for(let i = 0; i < max && i < 100 && j < 20; i++){
    //console.log("arr[i]",arr[i]);
    if(arr[i].preReqs.length === currSize){
      mini.push(arr[i]);
      let temp = [];
      arr.forEach(x => {return temp.push(x);});
      //console.log("mini",mini);
      if(i === 0){
        //console.log("arr: ",arr);
        arr.shift();
        //arr.pop();
        //console.log("arr: ",arr);
        //console.log("arr.length: ",arr.length);
      }
      else{
        temp = temp.splice(i-2, max);
        arr = arr.splice(0, i);
        temp.forEach(x => {return arr.push(x);});
      }
      //console.log("temp2",temp);
      //console.log(arr);
      i--;
      max--;
      j++;
    }
  }
  if(mini.length === 0){
    return arr;
  }
  mini.sort(compareCourseHours);
  console.log("\n\n\tMINI");
  console.log(mini);
  console.log("\tMINI\n\n");
  //mini.sort(compareCourseHours);
  //mini.push(arr);
  mini.reverse();
  mini.forEach(obj => {return arr.unshift(obj);});
  // console.log("\n\n\tMINIPUSH");
  // console.log(mini);
  // console.log("\n\n\tMINIPUSH");
  // arr = mini;
  // console.log("\n\n\tarr");
  // console.log(arr);
  // console.log("\n\n\tarr");
  //return arr;
  secondSort(arr, currSize+1);
}

const sortCoursesByPreReqs = arr => {
	//return arr.map(item1 item2 => {return arr.sort(compareTeeth(item['numTeeth']));});
    return arr.sort(comparePreReqs);
}

const makeCourse = (id, courseHours, lst = []) => {
  let obj = {
    id: id,
    ch: courseHours,
    preReqs: lst,
  };
  // correctPreReqs(obj);
  allCourses.push(obj);
  return obj;
}

const print = arr => {
  for(let i = 0; i < arr.length; i++){
    console.log('id: '+ arr[i].id + ', ch: ' + arr[i].ch + ', preReqs: '+ arr[i].preReqs);
  }
}

function handler(course) {
let n = 0;
console.log(course);
  while(course.preReqs.length > n){
    // console.log('\n\n\n');
    // console.log(course.preReqs[n]);
    //   console.log('\n\n\n');
    if(course.preReqs[n].preReqs.length !== 0){
      correctPreReqs(course.preReqs[n]);
    }
    n++;
  }
}

function correctPreReqs(course) {
  //console.log(typeof course);
  if(typeof course === 'undefined'){
    console.log('\t\tundefined');
    return;
  }
  console.log(course);
  dive = false;
  //console.log(`{ id: ${course.id}, ch: ${course.ch}, `);
  console.log();
  let n = 0
  //console.log('\t\t\t\t\t\t\t\t\t\thi there\n\n\n\n\n\t');
  //console.log(course.preReqs);
  while(course.preReqs.length > n){
    handler(course.preReqs[n]);
    n++;
    //console.log('\t\t\t\t\t\t\t\t\t\thi there\n\n\n\n\n\t');
  }
}

let coursesTaken = [makeCourse('BIOL1001', 3),
		                makeCourse('CHEM1001', 3),
		                makeCourse('CHEM1006', 2),
		                makeCourse('MATH1003', 3),
		                makeCourse('PHYS1061', 3),
		                makeCourse('PHYS1091', 2),
		                makeCourse('BIOL1012', 3, [allCourses[0]]),
		                makeCourse('CHEM1012', 3, [allCourses[1]]),
                	  makeCourse('CHEM1017', 2, [allCourses[2]]),
              		  makeCourse('PHYS1092', 2, [allCourses[5]]),
              		  makeCourse('MATH1013', 3, [allCourses[3]]),
              		  makeCourse('CHEM2416', 2, [allCourses[8]]),
		                makeCourse('CHEM2421', 3, [allCourses[7]]),
		                makeCourse('CHEM2601', 3, [allCourses[7], allCourses[10]]),
		                makeCourse('ENGL1144', 3),
                    makeCourse('CS1073',4),
                    makeCourse('CS1303',4),
                    makeCourse('CS1203',3),
                    makeCourse('MATH1503',3),
                    makeCourse('INFO1103',4,[allCourses[15]]),
                    makeCourse('CS2333',4, [allCourses[15],allCourses[16]]),
                    makeCourse('CS1083',4, [allCourses[15]]),
                    makeCourse('STAT2593',3, [allCourses[10]]),
                    makeCourse('CS2253',4, [allCourses[16]]),
                    makeCourse('CS2263',4, [allCourses[21]]),
                    makeCourse('CS3997',3),
                    makeCourse('CS3853',4, [allCourses[23]]),
                    makeCourse('CS2043',4, [allCourses[21]]),
                    makeCourse('CS2383',4, [allCourses[16], allCourses[21]]),
                    makeCourse('CS2613',4, [allCourses[21]]),
                    makeCourse('CS3413',4, [allCourses[24]]),
                    makeCourse('CS3113',3, [allCourses[15], allCourses[18]]),
                    makeCourse('CS2063',4, [allCourses[27]]),
                    makeCourse('CS3383',4, [allCourses[20], allCourses[22], allCourses[28]]),
                    makeCourse('CS3613',4, [allCourses[20], allCourses[24], allCourses[29]]),
                    makeCourse('CS3873',4, [allCourses[24]]),
                    makeCourse('CS3503',4, [allCourses[19]])];

//the line below will print the courses in an object like way.
//coursesTaken.forEach(obj => {return correctPreReqs(obj);});
// console.log(allCourses.length);
// console.log(allCourses.length);
//console.log(coursesTaken);
console.log(sortCoursesByPreReqs(coursesTaken));
//print(coursesTaken);
//console.log(coursesTaken);
print(secondSort(coursesTaken, 0));
//print(coursesTaken);

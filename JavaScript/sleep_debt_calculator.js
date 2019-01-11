const getSleepHours = day => {
  let hours = 0;
  day = day.toLowerCase();
  if(day === 'sunday'){
    hours = 8;
  }
  else if(day === 'monday'){
    hours = 6;
  }
  else if(day === 'tuesday'){
    hours = 6;
  }
  else if(day === 'wednesday'){
    hours = 6;
  }
  else if(day === 'thursday'){
    hours = 6;
  }
  else if(day === 'friday'){
    hours = 6;
  }
  else if(day === 'saturday'){
    hours = 7;
  }
  return hours;
};

const getActualSleepHours = () => {
  let sleepHours = 0;
  sleepHours += getSleepHours('Sunday');
  sleepHours += getSleepHours('Monday');
  sleepHours += getSleepHours('Tuesday');
  sleepHours += getSleepHours('Wednesday');
  sleepHours += getSleepHours('Thursday');
  sleepHours += getSleepHours('Friday');
  sleepHours += getSleepHours('Saturday');
	return sleepHours;
};

const getIdealSleepHours = (ideal) => {
  // const idealHours = 6.5;
  return ideal * 7;
};

const calculateSleepDebt = () => {
  const actualHours = getActualSleepHours();
  const idealHours = getIdealSleepHours(6.5);
  let diff = actualHours - idealHours;
  if(diff < 0){
    diff = 0 - diff;
  }
  if(actualHours === idealHours){
    console.log(`user got the perfect amount of sleep, ${actualHours} hours!`);
  }
  else if(actualHours > idealHours){
    console.log(`user got more sleep than needed by ${diff} hours`);
  }
  else{
    console.log(`user should get some rest for ${diff} hours.`);    
  }
};

// console.log(getActualSleepHours());
// console.log(getIdealSleepHours(6.5));
calculateSleepDebt();
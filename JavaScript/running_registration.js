let raceNumber = Math.floor(Math.random() * 1000);
let registeredEarly = true;
let runnerAge = 18;
if(runnerAge > 18 && registeredEarly){
  raceNumber += 1000;
  console.log(`Runner: ${raceNumber}, runs at 9:30 am, in the Adult and Registered Early section.`);
}
else if(runnerAge > 18){
  console.log(`Runner: ${raceNumber}, runs at 11:00 am, in the Adult and Registered Late section.`);
}
else if (runnerAge < 18){
  console.log(`Runner: ${raceNumber}, runs at 12:30 am, in the Youth section.`);
}
else{
  console.log(`Runner: ${raceNumber}, Please see the registration desk.`);
}
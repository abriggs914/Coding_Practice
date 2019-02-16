let fs = require('fs');
let pt = require('./pokemonTypes.js')
let file = 'full_pokedex.json';

let typesList = './pokemonTypes.json';
typesList = read_json_file(typesList);

file = read_json_file(file);
//let allTypes = pt.collectTypes(file);
console.log(pt);
function read_json_file(file) {
    return JSON.parse(fs.readFileSync(file));
}

function caseNumber(moveType){
  for(let i = 0; i < typesList.length; i++){
    if(typesList[i].languages.english === moveType){
      return i;
    }
  }
  return -1;
}

function effectiveness(moveType, enemyPokemon) {
  //let enemyPokemonStrAtk = enemyPokemon.typeEffective.strongAtk;
  //let enemyPokemonStrDef = enemyPokemon.typeEffective.strongDef;
  let val = 1;
  let index = caseNumber(moveType);
  let stratk = typesList[index].typeEffective.strongAtk;
  let noEffect = typesList[index].typeEffective.noEffect;
  //console.log(typesList[index].languages);
  //console.log('stratk: ',stratk);
  for(let item in enemyPokemon){
  //console.log('val ',val);
    index = caseNumber(enemyPokemon[item]);
    let strdef = typesList[index].typeEffective.strongDef;
    //console.log('strdef: ', strdef);
    //console.log('stratk: ', stratk);
    if(stratk.includes(enemyPokemon[item])){
      val *= 2;
      continue;
    }
    if(strdef.includes(moveType)){
      //console.log('enemyPokemon[item]: ', enemyPokemon[item]);
      val *= 0.5;
      continue;
    }
    if(noEffect.includes(enemyPokemon[item])){
      val *= 0;
      break;
    }
  }
  console.log(moveType + ' move against a pokemon of types: ' + enemyPokemon + '\n\twill have effectiveness: ' + val);
  return val;
}

function genTeam(){
  let team = [];
  let rand = Math.floor(Math.random()*809);
  let teamMembers = 0;
  while(teamMembers < 6){
    let pokemon = file[rand];
    team.push(pokemon);
    rand = Math.floor(Math.random()*809);
    teamMembers++;
  }
  return team;
}

//console.log(file);
let ivySaur = file[1].type; // ivysaur = ["grass","poison"]
let charmander = file[3].type; // charmander = ["fire"]
let squirtle = file[6].type; // squirtle = ["water"]
let geodude = file[73].type; // geodude = ["ground","rock"]
console.log('ivySaur: ',ivySaur);
console.log(effectiveness("Fighting",ivySaur));
console.log('charmander: ',charmander);
console.log(effectiveness("Water",charmander));
console.log('squirtle: ',squirtle);
console.log(effectiveness("Fire",squirtle));
console.log(effectiveness("Poison",geodude));
console.log(effectiveness("Electric",geodude));
let team = genTeam();
team.forEach(i => {console.log(i.name.english);});
team.sort(pokemon => {return effectiveness("Fighting",pokemon.type)});
//team.sort(effectiveness("Fighting",team));
team.forEach(i => {console.log(i.name.english);});
team.forEach(i => {console.log(effectiveness("Fighting", i.type),i.name.english);})
//console.log(team);

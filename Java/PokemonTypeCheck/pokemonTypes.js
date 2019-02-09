let fs = require('fs');

function read_json_file(file) {
    return JSON.parse(fs.readFileSync(file));
}

function countPokemon(json){
  let count = 0;
  for(let poke in json){
    count++;
  }
  return count;
}

function collectTypes(json){
  let types = [];
  let val = countPokemon(json);
  for(let i = 0; i < val; i++){
    let eachType = json[i].type;
    for(let type in eachType){
      if(!types.includes(eachType[type])){
        types.push(eachType[type]);
      }
    }
  }
  return types;
}

function tally(obj, type, vote){
  for(let item in obj){
    //console.log(item);
    if(obj[item].type === type){
      if(vote){
        obj[item].count++;
        obj[item].original++;
      }
      else{
        obj[item].count += 0.5;
        obj[item].dual++;
      }
    }
  }
  return obj;
}

function typeCensus(json){
  let result = [];
  let types = collectTypes(json).sort();
  for(let i = 0; i < types.length; i++){
    let temp = {
      type : types[i],
      count : 0,
      original : 0,
      dual : 0
    };
    result.push(temp);
  }
  for(let i = 0; i < countPokemon(json); i++){
    let pokeTypes = json[i].type;
    let n = pokeTypes.length;
    for(let type in pokeTypes){
      //console.log(pokeTypes[type]);
      if(n == 2){
        result = tally(result, pokeTypes[type], false);
      }
      else{
        result = tally(result, pokeTypes[type], true);
      }
    }
  }
  for(let i in result){
    result[i].dual /= 2;
  }
  return result;
}

function verifyVote(obj, json){
  let count = 0;
  let secondCount = 0;
  for(let item in obj){
    count += obj[item].count;
    secondCount += obj[item].original + obj[item].dual;
  }
  console.log('count: ',count,' secondCount: ',secondCount);
  return (count == countPokemon(json) && count == secondCount);
}

let file = 'full_pokedex.json';

file = read_json_file(file);
//console.log(file);
console.log(countPokemon(file));
console.log(collectTypes(file).length);
console.log(collectTypes(file).sort());
console.log(verifyVote(typeCensus(file), file));
console.log('result: ',typeCensus(file));

let types = require('../types.js');
let file = '../full_pokedex.json';

// This doesnt work, I believe types.js needs to be converted to a class

describe("Effectiveness Tests",
  function(){
    let ivySaur = file[1].type; // ivysaur = ["grass","poison"]
    let charmander = file[3].type; // charmander = ["fire"]
    let squirtle = file[6].type; // squirtle = ["water"]
    it("should be 0.5",
      function(){
        let ans = effectiveness("Fighting",ivySaur);
        expect(ans).toBe(0.5);
      });
    });

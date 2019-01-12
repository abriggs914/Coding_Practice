let board =  ["\t###################",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t###################",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t###################",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t#     #     #     #",
              "\t###################"];

// console.log(typeof(board[2])); //[4]
// console.log(board[2].indexOf("X"));
// board[2][2] = "Q";
// board[2][3] = "R";
// board[2][4] = "S";
// board[2][5] = "T";
// printBoard();

function printBoard(){
  for(var i = 0; i < board.length; i++){
    console.log(board[i]);
  }
}

function mode(n){
  if(n % 2 == 0){
    // console.log("HEY THERE");
    board[2] =  "\t#     #     #     #";
  }
  else {
      // console.log("General Kenobi");
      board[2] =  "\t#  X  #     #     #";
  }
}

let y = "";

function loop (n) {
    let i = 0;
    while(i < n){
      i++;
      mode(i);
      // board.turn();
      // y += ".";
      // console.log(y);
      console.log("\33c");
      // console.log(n, i);
      console.log(printBoard());
      loop(n-1);
      // setTimeout(function(){loop();},250,n-1);
      if(i == 5){
        console.log(i);
      }
    }
}

loop(5);

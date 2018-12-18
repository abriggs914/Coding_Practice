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

board[2] =  "\t#  X  #     #     #";
console.log(typeof(board[2])); //[4]
console.log(board[2].indexOf("X"));
board[2][2] = "Q";
board[2][3] = "R";
board[2][4] = "S";
board[2][5] = "T";
printBoard();

function printBoard(){
  for(var i = 0; i < board.length; i++){
    console.log(board[i]);
  }
}

let y = "";

function loop (n) {
    let i = 0;
    while(i < n){
      i++;
      // board.turn();
      y += ".";
      console.log(y);
      console.log("\33c");
      console.log(printBoard());
      setTimeout(function() { loop(); },250);
    }
}

loop(100);

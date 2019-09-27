public class SimTicTacToe {

    public boolean playerGoesFirst;
    public int gameNumber;
    public int playerSymbol;
    public int computerSymbol;

    public SimTicTacToe(boolean whoGoesFirst, int playerSymbol) {
        this.playerGoesFirst = whoGoesFirst;
        this.playerSymbol = playerSymbol;

        // call playMatch on creation
        TicTacToe ttt = new TicTacToe(true, playerSymbol, -1); // hardcoded a cpu move first at the beginning
        int matchResult = playMatch(ttt);
    }

    public SimTicTacToe(boolean testModeEnabled, boolean whoGoesFirst, int playerSymbol, int[][] positionSymbol) {
        this.playerGoesFirst = whoGoesFirst;
        this.playerSymbol = playerSymbol;

        // call playMatch on creation
        TicTacToe ttt = new TicTacToe(true, playerSymbol, -1, positionSymbol); // hardcoded a cpu move first at the beginning
        int matchResult = playMatch(ttt);
    }

    public boolean getFirstPlayer() {
        return this.playerGoesFirst;
    }

    public int getPlayerSymbol() {
        return this.playerSymbol;
    }

    public int playMatch(TicTacToe ttt) {
        boolean playerPlaysFirst = this.getFirstPlayer();
        int playerSymbol = this.getPlayerSymbol();
        BoardState boardState = ttt.getBoardTree();
        ttt.expandTree(playerPlaysFirst, playerSymbol, 0, boardState);
        return 0;

    }

}
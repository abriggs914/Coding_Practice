import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.util.Random;

public class TicTacToeDriver {

    public static Scanner scn = new Scanner(System.in);

    private static boolean testModeEnabled = true;
    private static boolean quitWhenAsked = true;
    private static boolean playAgainWhenAsked = false;

    public static int maximumTestGames = 100;

    public static String whoGoesFirst() {
        System.out.println("\tWho goes first?\n\nP  -  Player\nC  -  Computer\nQ  -  Quit");
        String input = scn.nextLine().toUpperCase();
        System.out.println(input);
        while (!input.equals("P") && !input.equals("C") && !input.equals("Q")) {
            System.out.println("\tPlease enter a valid choice\n\tWho goes first?" +
                                "\n\nP  -  Player\nC  -  Computer\nQ  -  Quit");
            input = scn.nextLine().toUpperCase();
        }
        if (checkQuitOnInput(input)) {
            quitGame();
        }
        return input;
    }

    public static boolean checkQuitOnInput(String choice) {
        if (choice.equals("Q")) {
            return true;
        }
        return false;
    }

    public static void quitGame() {
        int i = 3;
        while (i > 0) {
            System.out.println("\tquitting in " + i + " ...");
            wait1Second();
            i--;
        }
        System.out.println("exiting.");
        System.exit(0);
    }

    public static void wait1Second() {
        if (!testModeEnabled) {
            try {
                TimeUnit.SECONDS.sleep(1);
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void reportPlayerSymbol(int playerSymbol) {
        char playerChar = ((playerSymbol == 1)? 'X' : 'O');
        char computerChar = ((playerChar == 'X')? 'O' : 'X');
        System.out.println("\nThe computer selected: " + computerChar + ", leaving you with " + playerChar + ".\n");
        wait1Second();
    }

    public static int[] pickSymbols(boolean playerPlaysFirst) {
        int player;
        int computer;
        if (playerPlaysFirst) {
            player = playerPickSymbol();
            if (player == -1) {
                quitGame();
            }
        }
        else {
            player = genRandomPlayerSymbol();
            reportPlayerSymbol(player);
        }
        computer = ((player == 1)? 3 : 1);
        int[] res = {player, computer};
        return res;
    }

    public static int threeOrOne(double n) {
        double half2 = 5 / 2.0;
        int newN = ((n > half2)? 3 : 1);
        return newN;
    }

    public static int genRandomPlayerSymbol() {
        Random r = new Random();
        double rDouble = (r.nextDouble() * 3.0);
        return threeOrOne(rDouble);
    }

    public static int playerPickSymbol() {
        System.out.println("\tWhich symbol?\n\nX\nO\nQ  -  Quit");
        String input = scn.nextLine().toUpperCase();
        while (!input.equals("X") && !input.equals("O") && !input.equals("Q")) {
            System.out.println("\tPlease enter a valid choice\n\tWho goes first?" +
                    "\n\nX  -  Player\nO  -  Computer\nQ  -  Quit");
            input = scn.nextLine().toUpperCase();
            System.out.println(input);
        }
        if (input.equals("X")) {
            return 1;
        }
        else if (input.equals("O")){
            return 3;
        }
        else {
            return -1;
        }
    }

    public static boolean askToPlayAgain() {
        System.out.println("\n\tWould you like to play again?\nY  -  Yes\nN  -  NO\n");
        String input = scn.nextLine().toUpperCase();
        if (testModeEnabled && quitWhenAsked) {
            if (!input.equals("Y")) {
                return false;
            }
        }
        else if (testModeEnabled && playAgainWhenAsked) {
            if (maximumTestGames > 0) {
                maximumTestGames--;
                return false;
            }
        }
        while (!input.equals("Y") && !input.equals("N")) {
            System.out.println("\n\tPlease enter a valid choice\n" +
                                "\tWould you like to play again?\nY  -  Yes\nN  -  NO\n");
            input = scn.nextLine().toUpperCase();
        }
        if (input.equals("N")){
            quitGame();
            return false;
        }
        return true;
    }

    public static void main(String[] args) {
        String firstPlayer;
        int[] symbols;
        int playerSymbol;
        int computerSymbol;
        boolean keepPlaying;
        boolean playerPlaysFirst;

//        int[][] positionSymbol = {{0, 1}, {4, 1}, {8, 1}}; // diagonal x win
//        int[][] positionSymbol = {{0, 1}, {3, 1}, {6, 1}, {2, 3}, {5, 3}}; // vertical x win
//        int[][] positionSymbol = {{0, 1}, {3, 1}, {6, 1}}; // vertical x win
//        int[][] positionSymbol = {{2, 3}, {1, 1}, {4, 3}, {6, 3}}; // diagonal o win
        int[][] positionSymbol = new int[0][0];

        // Play game
        keepPlaying = true;
        while (keepPlaying) {
            firstPlayer = whoGoesFirst();
            playerPlaysFirst = firstPlayer.equals("P");
            symbols = pickSymbols(playerPlaysFirst);
            playerSymbol = symbols[0];
            computerSymbol = symbols[1];
            if (testModeEnabled) {
                SimTicTacToe sttt = new SimTicTacToe(true, playerPlaysFirst, playerSymbol, positionSymbol);
            }
            else {
                SimTicTacToe sttt = new SimTicTacToe(playerPlaysFirst, playerSymbol);
            }
            keepPlaying = askToPlayAgain();
        }
    }

}
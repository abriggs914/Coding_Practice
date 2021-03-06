package com.example.abrig.minesweeper;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class MainActivity extends AppCompatActivity implements QuitGamePopUp.ExampleDialogListener {

    private SeekBar colSeekBar;
    private SeekBar rowSeekBar;
    private SeekBar mineSeekBar;
    private String reportTextString;
    private TextView reportTextView;
    private Button createButton;
    private Button recordsButton;

    private int numRows, numCols, numMines;
    private MineSweeperGrid mineSweeperGrid;
    public static SharedPreferences preferences;

    public String[][] grid_1_soln = {
            {" ","M","M"," ","M"},
            {"M"," ","M"," "," "},
            {" "," ","M","M","M"},
            {" "," "," "," "," "},
            {" ","M"," ","M"," "}};

    public String[][] grid_2_soln = {
            {" "," "," "," "," ","M"," "," "," ","M"," "," ","M"," "},
            {" "," "," ","M"," "," "," "," "," "," "," "," "," ","M"},
            {" ","M"," "," "," "," "," ","M"," ","M"," "," "," "," "},
            {" "," "," "," "," "," "," "," "," "," "," "," "," "," "},
            {" "," "," "," "," "," "," "," "," "," "," ","M"," "," "},
            {" "," "," "," "," "," "," ","M"," "," "," ","M"," "," "},
            {" ","M"," "," "," "," "," "," "," "," "," "," "," "," "},
            {" "," "," "," "," "," "," "," "," "," "," "," "," ","M"},
            {" "," "," ","M"," "," ","M"," "," "," "," "," "," "," "},
            {" ","M"," "," "," "," ","M"," "," "," "," "," "," "," "},
            {" ","M","M"," "," "," "," "," "," "," "," "," ","M"," "},
            {"M","M"," "," "," "," "," "," ","M"," "," "," "," ","M"},
            {" "," "," "," "," "," "," "," "," "," "," "," "," "," "},
            {"M"," "," "," "," ","M"," "," "," "," "," "," "," "," "},
            {" ","M"," "," "," "," "," "," ","M"," "," "," "," "," "},
            {"M"," "," ","M"," "," "," "," "," "," "," "," "," "," "},
            {" "," ","M","M"," "," "," "," ","M"," ","M"," "," "," "},
            {" "," "," "," "," "," "," "," "," "," ","M"," "," "," "},
            {" "," "," "," ","M"," "," "," "," "," "," ","M"," ","M"},
            {" "," "," "," "," "," "," "," "," "," "," "," ","M"," "}};

    public String[][] grid_3_soln = {
            {"M","M","M","M","M"},
            {"M"," ","M"," ","M"},
            {"M","M","M"," ","M"},
            {" "," ","M"," ","M"},
            {" "," ","M"," "," "},
            {"M","M","M"," "," "}};

//    Grid testGrid1 = new Grid(grid_3_soln);
//    public MineSweeperGrid testMineSweeper1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

//        testMineSweeper1 = new MineSweeperGrid(this, getSupportFragmentManager(), testGrid1, 0,0);
        preferences = getSharedPreferences("com.example.minesweeper", MODE_PRIVATE);
//        preferences.edit().clear().apply();
    }

    public void initPreferences() {
        ArrayList<String> keys = getKeys();
        for (String key : keys) {
            if (key.equals("score_worst")) {
                String val = Integer.toString(Integer.MAX_VALUE);
                SharedPreferencesHandler.write(key, val);
            }
            else if (key.equals("time_worst")) {
                String val = Integer.toString(Integer.MIN_VALUE);
                SharedPreferencesHandler.write(key, val);
            }
            else if (key.equals("time_best")) {
                String val = Integer.toString(Integer.MAX_VALUE);
                SharedPreferencesHandler.write(key, val);
            }
            else {
                SharedPreferencesHandler.write(key, "0");
            }
        }
    }

    public void resetPreferences() {
        preferences.edit().clear().apply();
        preferences = getSharedPreferences("com.example.minesweeper", MODE_PRIVATE);
        onResume();
    }

    @Override
    protected void onStop() {
        if (mineSweeperGrid != null) {
            MineSweeper mineSweeper = mineSweeperGrid.getMineSweeper();
            if (!mineSweeper.isGameOver()) {
                mineSweeperGrid.stopTimer();
                boolean winner = mineSweeper.checkSolution();
                int numGames = SharedPreferencesHandler.getNumGames();
                int time = mineSweeperGrid.getSecondsPast();
                int score = mineSweeperGrid.getScore();
                double searched = mineSweeper.getGameGrid().countCheckedSquares();
                // game_num, win/loss(1/0), time, score, searched
                int winLoss = ((winner) ? 1 : 0);
//            String gameString = GameHistoryParser.genHistoryString(mineSweeper, numGames, winLoss, time, score, (int) searched);
                SharedPreferencesHandler.saveGame(mineSweeper, numGames, winLoss, time, score, (int) searched);
            }
        }
        super.onStop();
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (preferences.getBoolean("firstrun", true)) {
            Log.i("MainActivity", "firstRun, setMainMenu()");

            SharedPreferencesHandler.write("firstrun", false);
            initPreferences();
            setMainMenu();
        }
        else {
            if (preferences.getBoolean("gameInProgress", false)) {
                Log.i("MainActivity", "game in progress, resuming");
                try {
                    mineSweeperGrid = SharedPreferencesHandler.loadPreviousGame(this, getSupportFragmentManager());
                    setContentView(mineSweeperGrid);
                } catch (MineSweeperException e) {
                    e.printStackTrace();
                    setMainMenu();
                }
            }
            else {
                Log.i("MainActivity","!first && !inProgress, setting MainMenu");
                setMainMenu();
            }
        }

//        System.out.println("KEY SET: " + preferences.getAll().keySet());
//        Map<String, ?> keyVals = preferences.getAll();
//        for (String s : preferences.getAll().keySet()) {
//            System.out.println("String entry: " + s + ", val: " + keyVals.get(s));
//        }
    }

    @Override
    public void applyTexts(boolean keepPlaying, boolean shuffle, boolean resetGame) {
//        System.out.println("Applying texts in Main keepPlaying: " + keepPlaying + ", resetGame: " + resetGame);
        if (shuffle) {
            resetGame = true;
        }
        if (keepPlaying) {
            return;
        }
        else {
            mineSweeperGrid.stopTimer();
            mineSweeperGrid.getMineSweeper().setGameOver(true);
            if (resetGame) {
                String[][] stringGrid = mineSweeperGrid.getMineSweeper().getOriginalGrid().getStringGrid();
                String gridString = "";
                for (String[] s : stringGrid) {
                    gridString += Arrays.toString(s) + "\n";
                }
                Grid grid = Grid.parseGrid(stringGrid);
//                System.out.println("ORIGINAL GRID BEFORE PARSING:\n" + gridString + "\nGrid\n" + grid);
                mineSweeperGrid = new MineSweeperGrid(
                        this,
                        getSupportFragmentManager(),
                        grid,
                        0,
                        0);
                if (shuffle) {
                    mineSweeperGrid.shuffleGrid();
                }
                setContentView(mineSweeperGrid);
            }
            else {
                setMainMenu();
            }
            mineSweeperGrid.handleGameOver();
        }
    }

    public void setMainMenu() {
        setContentView(R.layout.activity_main);

        rowSeekBar = findViewById(R.id.rowsSeekBar);
        colSeekBar = findViewById(R.id.columnsSeekBar);
        mineSeekBar = findViewById(R.id.minesSeekBar);
        reportTextView = findViewById(R.id.reportTextString);
        createButton = findViewById(R.id.createButton);
        recordsButton = findViewById(R.id.recordsButton);

        rowSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
              setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });

        colSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
              setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });

        mineSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });

        createButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                System.out.println("Create button clicked");
                if (numRows > 0) {
                    if (numCols > 0) {
                        if (numMines > 0) {
                            if (numMines < (numRows * numCols)) {
                                String[][] stringGrid = generateStringGrid();
                                Grid grid = new Grid(stringGrid);
//                                System.out.println("GENERATED GRID:\n" + grid);

                                mineSweeperGrid = new MineSweeperGrid(
                                        MainActivity.this,
                                        getSupportFragmentManager(),
                                        grid,
                                        0,
                                        0);

                                setContentView(mineSweeperGrid);
                                return;
                            }
                        }
                    }
                }
                Toast.makeText(MainActivity.this, "invalid inputs", Toast.LENGTH_LONG).show();
            }
        });

        recordsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.i("MainActivity","Records button clicked");
                Intent intent  = new Intent(MainActivity.this, RecordsView.class);
                startActivityForResult(intent, 0);
            }
        });
    }

    private void setReportString() {
        numRows = rowSeekBar.getProgress();
        numCols = colSeekBar.getProgress();
        numMines = mineSeekBar.getProgress();
        String plural = ((numMines == 1)? "" : "s");
        String res = numRows + "x" + numCols + ", with " + numMines + " mine" + plural + ".";
        reportTextView.setText(res);
    }

    private String[][] generateStringGrid() {
        String[][] res = new String[numRows][numCols];
        double percentage = numMines / (numRows * numCols);
        int minesPlaced = 0;
        Random rand = new Random();
        for (int r = 0; r < numRows; r++) {
            for (int c = 0; c < numCols; c++) {
                double randomNum = rand.nextDouble();
                boolean isMine = randomNum <= percentage;
                String val = Main.CHECKED;
                if (isMine && minesPlaced < numMines) {
                    val = Main.MINE;
                    minesPlaced++;
                }
                res[r][c] = val;
            }
        }
        while (minesPlaced < numMines) {
            int r = rand.nextInt(numRows);
            int c = rand.nextInt(numCols);
            String val = res[r][c];
            if (!val.equals(Main.MINE)) {
                res[r][c] = Main.MINE;
                minesPlaced++;
            }
        }
        return res;
    }

    public static ArrayList<String> getKeys(){
        return new ArrayList<>(Arrays.asList(
                "games_num",
                "games_won",
                "games_lost",
                "time_average",
                "time_best",
                "time_worst",
                "time_total",
                "score_average",
                "score_best",
                "score_worst",
                "score_total",
                "difficulty_total",
                "difficulty_average"
        ));
    }
}

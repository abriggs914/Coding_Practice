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
import java.util.Map;
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


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.preferences = getSharedPreferences("com.example.minesweeper", MODE_PRIVATE);
        preferences.edit().clear().apply();
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
    protected void onResume() {
        super.onResume();

        if (preferences.getBoolean("firstrun", true)) {

            SharedPreferencesHandler.write("firstrun", false);
            System.out.println("\n\n\n\tFIRST RUN\n\n\n");
            initPreferences();
        }
        else {
            System.out.print("\n\n\n\tNOT THE FIRST RUN\n\n\n");
        }

        System.out.println("KEY SET: " + preferences.getAll().keySet());
        Map<String, ?> keyVals = preferences.getAll();
        for (String s : preferences.getAll().keySet()) {
            System.out.println("String entry: " + s + ", val: " + keyVals.get(s));
        }


        mineSweeperGrid = new MineSweeperGrid(this, getSupportFragmentManager(), new Grid(grid_3_soln), 0, 0);
        setContentView(mineSweeperGrid);
    }

    @Override
    public void applyTexts(boolean keepPlaying, boolean resetGame) {
        System.out.println("Applying texts in Main keepPlaying: " + keepPlaying + ", resetGame: " + resetGame);
        if (keepPlaying) {
            return;
        }
        else {
            mineSweeperGrid.stopTimer();
            mineSweeperGrid.getMineSweeper().setGameOver(true);
            if (resetGame) {
                if (!mineSweeperGrid.getMineSweeper().isGameOver()) {
                    Log.e("Main 142", "don\'t keep playing, do reset. setContentView(mineSweeperGrid)");
                    mineSweeperGrid.handleGameOver();
                }
                String[][] stringGrid = mineSweeperGrid.getMineSweeper().getOriginalGrid().getStringGrid();
                String gridString = "";
                for (String[] s : stringGrid) {
                    gridString += Arrays.toString(s) + "\n";
                }
                Grid grid = Grid.parseGrid(stringGrid);
                System.out.println("ORIGINAL GRID BEFORE PARSING:\n" + gridString + "\nGrid\n" + grid);
                mineSweeperGrid = new MineSweeperGrid(
                        this,
                        getSupportFragmentManager(),
                        grid,
                        0,
                        0);
                setContentView(mineSweeperGrid);
            }
            else {
                if (!mineSweeperGrid.getMineSweeper().isGameOver()) {
                    Log.e("Main 164", "don\'t keep playing, don\'t reset. setMainMenu()");
                }
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
//                System.out.println("rowSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
//                System.out.println("rowSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
//                System.out.println("rowSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
            }
        });

        colSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
//                System.out.println("colSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
//                System.out.println("colSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
//                System.out.println("colSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
            }
        });

        mineSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
//                System.out.println("mineSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
//                System.out.println("mineSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
//                System.out.println("mineSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
            }
        });

        createButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Create button clicked");
                if (numRows > 0) {
                    if (numCols > 0) {
                        if (numMines > 0) {
                            if (numMines < (numRows * numCols)) {
                                String[][] stringGrid = generateStringGrid();
                                Grid grid = new Grid(stringGrid);
                                System.out.println("GENERATED GRID:\n" + grid);
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
                System.out.println("Records button clicked");
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

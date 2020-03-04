package com.example.abrig.minesweeper;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Arrays;
import java.util.Random;

public class MainActivity extends AppCompatActivity implements QuitGamePopUp.ExampleDialogListener {

    private MineSweeperGrid mineSweeperGrid;

    private SeekBar colSeekBar;
    private SeekBar rowSeekBar;
    private SeekBar mineSeekBar;
    private String reportTextString;
    private TextView reportTextView;
    private Button createButton;
    private Button recordsButton;

    private int numRows, numCols, numMines;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        String[][] grid_1_soln = {
                {" ","M","M"," ","M"},
                {"M"," ","M"," "," "},
                {" "," ","M","M","M"},
                {" "," "," "," "," "},
                {" ","M"," ","M"," "}};

        String[][] grid_2_soln = {
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

        String[][] grid_3_soln = {
                {"M","M","M","M","M"},
                {"M"," ","M"," ","M"},
                {"M","M","M"," ","M"},
                {" "," ","M"," ","M"},
                {" "," ","M"," "," "},
                {"M","M","M"," "," "}};

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
            if (resetGame) {
                mineSweeperGrid.stopTimer();
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
                mineSweeperGrid.stopTimer();
                setMainMenu();
            }
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
                System.out.println("rowSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                System.out.println("rowSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                System.out.println("rowSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
            }
        });

        colSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                System.out.println("colSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                System.out.println("colSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                System.out.println("colSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
            }
        });

        mineSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                System.out.println("mineSeekBar\tonProgressChanged\tseekbar: " + seekBar + ", progress: " + progress + ", fromUser: " + fromUser);
                setReportString();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                System.out.println("mineSeekBar\tonStartTrackingTouch\tseekbar: " + seekBar);
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                System.out.println("mineSeekBar\tonStopTrackingTouch\tseekbar: " + seekBar);
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
}

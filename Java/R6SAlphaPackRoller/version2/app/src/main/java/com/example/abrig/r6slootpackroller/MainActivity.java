package com.example.abrig.r6slootpackroller;

import android.annotation.SuppressLint;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;

import java.text.NumberFormat;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    public TextView percentageTextView;
    public TextView alphaPacksTextView;
    public TextView numGamesTextView;
    public TextView maxPercentageTextView;
    public TextView minPercentageTextView;
    public TextView avgPercentageTextView;
    public TextView packsPerGameTextView;
    public TextView currGamesSincePackTextView;
    public TextView maxGamesSincePackTextView;
    public TextView minGamesSincePackTextView;
    public TextView rankedStatsTextView;
    public TextView casualStatsTextView;
    public Switch rankedCasualSwitch;
    public Switch vipSwitch;
    public Button winGameButton;
    public Button loseGameButton;

    public double percentage;
    public double maxPercentage;
    public double minPercentage;
    public double avgPercentage;
    public double percentageSum;
    public double packsPerGame;
    public int gamesSinceLastPack;
    public int maxGamesForPack;
    public int minGamesForPack;
    public int rankedWins;
    public int rankedLosses;
    public int rankedAlphaPackWins;
    public int casualWins;
    public int casualLosses;
    public int casualAlphaPackWins;
    public int numGamesInt;
    public int numWins;
    public int numLosses;
    public int numAlphaPacksInt;

    final double RANKED_WIN_CHANCE = 3.0;
    final double RANKED_LOSS_CHANCE = 2.5;
    final double CASUAL_WIN_CHANCE = 2.0;
    final double CASUAL_LOSS_CHANCE = 1.5;
    final double VIP_BONUS = 0.3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize views
        percentageTextView = findViewById(R.id.percentageBox);
        alphaPacksTextView = findViewById(R.id.numAlphaPacksBox);
        numGamesTextView = findViewById(R.id.numGamesBox);
        maxPercentageTextView = findViewById(R.id.maxPercentageBox);
        minPercentageTextView = findViewById(R.id.minPercentageBox);
        avgPercentageTextView = findViewById(R.id.avgPercentageBox);
        currGamesSincePackTextView = findViewById(R.id.gamesSinceLastPackBox);
        maxGamesSincePackTextView = findViewById(R.id.mostSinceLastPackBox);
        minGamesSincePackTextView = findViewById(R.id.leastSinceLastPackBox);
        rankedStatsTextView = findViewById(R.id.rankedStatsBox);
        casualStatsTextView = findViewById(R.id.casualStatsBox);
        packsPerGameTextView = findViewById(R.id.packsPerGameBox);
        rankedCasualSwitch = findViewById(R.id.rankedCasualSwitch);
        vipSwitch = findViewById(R.id.vipSwitch);
        winGameButton = findViewById(R.id.winButton);
        loseGameButton = findViewById(R.id.lossButton);

        // Initialize values
        percentage = 0.0;
        maxPercentage = percentage;
        minPercentage = 100.0;
        avgPercentage = percentage;
        percentageSum = percentage;
        numGamesInt = 0;
        numWins = 0;
        numLosses = 0;
        rankedWins = 0;
        rankedLosses = 0;
        rankedAlphaPackWins = 0;
        casualWins = 0;
        casualLosses = 0;
        casualAlphaPackWins = 0;
        gamesSinceLastPack = 0;
        maxGamesForPack = 0;
        minGamesForPack = Integer.MAX_VALUE;
        packsPerGame = percentage;
        numAlphaPacksInt = 0;

        // Initialize results boxes in order top to bottom
        initResultTextViews();

//        For testing
//        numGamesInt = 2000;
//        numLosses = 1000;
//        numWins = 1000;
//        numGamesTextView.setText(setGames());
    }

    // Called to stringify a double value and concat a % symbol.
    public String setPercentage(double p) {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(3);
        return nf.format(p) + " %";
    }

    // Called to update max percentage roll value.
    public String setMaxPercentage() {
//        NumberFormat nf = NumberFormat.getInstance();
//        nf.setMaximumFractionDigits(4);
//        String max = nf.format(maxPercentage);
        return setPercentage(maxPercentage);
    }

    // Called to update min percentage roll value.
    public String setMinPercentage() {
//        NumberFormat nf = NumberFormat.getInstance();
//        nf.setMaximumFractionDigits(2);
//        String min = nf.format(minPercentage);
        return setPercentage(minPercentage);
    }

    // Fromats the number of games stats into a readable string.
    public String setGames() {
        String wins = Integer.toString(numWins);
        String losses = Integer.toString(numLosses);
        String games = Integer.toString(numGamesInt);
        return "{ W: " + wins + " } : { L: " + losses + "} : { T: " + games + " }";
    }

    // Creates a string containing ranked Wins, Losses and Packs won.
    public String gatherRankedStats() {
        String rankWins = Integer.toString(rankedWins);
        String rankLosses = Integer.toString(rankedLosses);
        String rankPacks = Integer.toString(rankedAlphaPackWins);
        return "{ W: " + rankWins + " } : { L: " + rankLosses + " } : { P: " + rankPacks + " }";
    }

    // Creates a string containing casual Wins, Losses and Packs won.
    public String gatherCasualStats() {
        String casWins = Integer.toString(casualWins);
        String casLosses = Integer.toString(casualLosses);
        String casPacks = Integer.toString(casualAlphaPackWins);
        return "{ W: " + casWins + " } : { L: " + casLosses + " } : { P: " + casPacks + " }";
    }

    // Called to update the current percentage value, performs a roll and either resets
    // percentage or increments it.
    public void updatePercentage(boolean gameWin) {
        Boolean rankedCasualState = rankedCasualSwitch.isChecked();
        Boolean vipState = vipSwitch.isChecked();
        double rollVal = roll() + 1.0;
        boolean alphaPackWin = false;
        if (gameWin && percentage >= rollVal) {
            alphaPackWin = true;
        }
        if (alphaPackWin) {
            checkMaxPercentage();
            checkMinPercentage();
            checkMaxGamesSincePack();
            checkMinGamesSincePack();
            gamesSinceLastPack = 0;
            incrementNumAlphaPacks();
            updateAverageWinPercentage();
            if (rankedCasualState) {
                rankedAlphaPackWins++;
                percentage = RANKED_WIN_CHANCE;
            }
            else {
                casualAlphaPackWins++;
                percentage = CASUAL_WIN_CHANCE;
            }
        }
        else {
            if (rankedCasualState) {
                percentage += ((gameWin) ? RANKED_WIN_CHANCE : RANKED_LOSS_CHANCE);
            }
            else {
                percentage += ((gameWin) ? CASUAL_WIN_CHANCE : CASUAL_LOSS_CHANCE);
            }
        }
        if (vipState) {
            percentage += VIP_BONUS;
        }
        if (percentage > 100) {
            percentage = 100.0;
        }
        percentageTextView.setText(setPercentage(percentage));
        rankedStatsTextView.setText(gatherRankedStats());
        casualStatsTextView.setText(gatherCasualStats());
    }

    // Determines if the maxGamesSincePack variable should be raised.
    @SuppressLint("DefaultLocale")
    public void checkMaxGamesSincePack() {
        if (gamesSinceLastPack > maxGamesForPack) {
            maxGamesForPack = gamesSinceLastPack;
            maxGamesSincePackTextView.setText(String.format("%d", maxGamesForPack));
        }
    }

    // Determines if the minGamesSincePack variable should be lowered.
    @SuppressLint("DefaultLocale")
    public void checkMinGamesSincePack() {
        if (gamesSinceLastPack < minGamesForPack) {
            minGamesForPack = gamesSinceLastPack;
            minGamesSincePackTextView.setText(String.format("%d", minGamesForPack));
        }
    }

    // Determines if the minPercentage variable should be lowered.
    public void checkMinPercentage() {
        if (percentage < minPercentage) {
            minPercentage = percentage;
            minPercentageTextView.setText(setMinPercentage());
        }
    }

    // Determines if the maxPercentage variable should be raised.
    public void checkMaxPercentage() {
        if (percentage > maxPercentage) {
            maxPercentage = percentage;
            maxPercentageTextView.setText(setMaxPercentage());
        }
    }

    // Simulates a roll, returning a double between 0.0 and 99.0.
    public double roll() {
        Random rand = new Random();
        int rand_num = rand.nextInt(100);
        return (double) rand_num;
    }

    // Used to increase the total number of games simulated.
    // Also increments the gamesSinceLastPack variable and updates their respective textviews.
    @SuppressLint("DefaultLocale")
    public void incrementNumGames() {
        numGamesInt++;
        gamesSinceLastPack++;
        numGamesTextView.setText(setGames());
        updatePacksPerGame();
        currGamesSincePackTextView.setText(String.format("%d", gamesSinceLastPack));
    }

    // Used to increment the numAlphaPacksInt variable, as well as update it's textview.
    @SuppressLint("DefaultLocale")
    public void incrementNumAlphaPacks() {
        numAlphaPacksInt++;
        alphaPacksTextView.setText(String.format("%d", numAlphaPacksInt));
        currGamesSincePackTextView.setText(String.format("%d", gamesSinceLastPack));
    }

    // Called to reset current textViews
    public void resetNums(View view) {
        numAlphaPacksInt = 0;
        numWins = 0;
        numLosses = 0;
        numGamesInt = 0;
        percentage = 0.0;
        maxPercentage = percentage;
        minPercentage = 100.0;
        avgPercentage = percentage;
        percentageSum = percentage;
        rankedWins = 0;
        rankedLosses = 0;
        casualWins = 0;
        casualLosses = 0;
        rankedAlphaPackWins = 0;
        casualAlphaPackWins = 0;
        maxGamesForPack = 0;
        minGamesForPack = Integer.MAX_VALUE;
        gamesSinceLastPack = 0;
        packsPerGame = percentage;
        initResultTextViews();
    }

    // Called to set all reporting textviews to their beginning values.
    @SuppressLint("DefaultLocale")
    public void initResultTextViews() {
        numGamesTextView.setText(setGames());
        percentageTextView.setText(setPercentage(percentage));
        alphaPacksTextView.setText(String.format("%d", numAlphaPacksInt));
        maxPercentageTextView.setText(setMaxPercentage());
        minPercentageTextView.setText(setMinPercentage());
        updatePacksPerGame();
        currGamesSincePackTextView.setText(String.format("%d", gamesSinceLastPack));
        maxGamesSincePackTextView.setText(String.format("%d", maxGamesForPack));
        minGamesSincePackTextView.setText(String.format("%d", minGamesForPack));
        rankedStatsTextView.setText(gatherRankedStats());
        casualStatsTextView.setText(gatherCasualStats());
        avgPercentageTextView.setText(setPercentage(avgPercentage));
    }

    // Creates a readable string of ranked and casual packs per game values
    // also sets the textview.
    public void updatePacksPerGame() {
        int totalRankGames = rankedWins + rankedLosses;
        int totalCasGames = casualWins + casualLosses;
        totalRankGames = ((totalRankGames == 0) ? 1 : totalRankGames);
        totalCasGames = ((totalCasGames == 0) ? 1 : totalCasGames);
        double rankRate = (double) rankedAlphaPackWins / (double) totalRankGames;
        double casRate = (double) casualAlphaPackWins / (double) totalCasGames;
        String rank = setPercentage(rankRate);
        String cas = setPercentage(casRate);
        String res = "{ R: " + rank + " } : { C: " + cas + " }";
        packsPerGameTextView.setText(res);
    }

    // updates the value of percentageSum and reports the new average percentage value
    // an alpha pack was won at.
    public void updateAverageWinPercentage() {
        percentageSum += percentage;
        avgPercentage = percentageSum / (double) numAlphaPacksInt;
        avgPercentageTextView.setText(setPercentage(avgPercentage));
    }

    // Called to simulate a loss
    public void gameLoss(View view) {
        Boolean rankedCasualState = rankedCasualSwitch.isChecked();
        if (rankedCasualState) {
            rankedLosses++;
        }
        else {
            casualLosses++;
        }
        numLosses++;
        incrementNumGames();
        updatePercentage(false);
    }

    // Called to simulate a win
    public void gameWin(View view) {
        Boolean rankedCasualState = rankedCasualSwitch.isChecked();
        if (rankedCasualState) {
            rankedWins++;
        }
        else {
            casualWins++;
        }
        numWins++;
        incrementNumGames();
        updatePercentage(true);
    }
}
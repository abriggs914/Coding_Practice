package com.example.abrig.r6salphapackroller;

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
    public Switch rankedCasualSwitch;
    public Switch vipSwitch;
    public Button winGameButton;
    public Button loseGameButton;

    public double percentage;
    public double maxPercentage;
    public double minPercentage;
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
        percentageTextView = (TextView) findViewById(R.id.percentageBox);
        alphaPacksTextView = (TextView) findViewById(R.id.numAlphaPacksBox);
        numGamesTextView = (TextView) findViewById(R.id.numGamesBox);
        maxPercentageTextView = (TextView) findViewById(R.id.maxPercentageBox);
        rankedCasualSwitch = (Switch) findViewById(R.id.rankedCasualSwitch);
        vipSwitch = (Switch) findViewById(R.id.vipSwitch);
        winGameButton = (Button) findViewById(R.id.winButton);
        loseGameButton = (Button) findViewById(R.id.lossButton);

        // Initialize values
        percentage = 0.0;
        maxPercentage = percentage;
        minPercentage = 100.0;
        percentageTextView.setText(setPercentage(percentage));
        maxPercentageTextView.setText(setMinMaxPercentage());
        alphaPacksTextView.setText("0");
        numGamesTextView.setText("0");
        numGamesInt = 0;
        numWins = 0;
        numLosses = 0;
        numAlphaPacksInt = 0;
    }

    // Called to stringify a double value and concat a % symbol
    public String setPercentage(double p) {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(2);
        return nf.format(p) + " %";
    }


    public String setMinMaxPercentage() {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(2);
        String min = nf.format(minPercentage);
        String max = nf.format(maxPercentage);
        return "{ MIN : " + min + " % }\n{ MAX : " + max + " % }";
    }

    public String setGames() {
        String wins = Integer.toString(numWins);
        String losses = Integer.toString(numLosses);
        String games = Integer.toString(numGamesInt);
        return "{ W: " + wins + " } : { L " + losses + "}\n{ T " + games + " }";
    }

    public void updatePercentage(boolean gameWin) {
        Boolean rankedCasualState = rankedCasualSwitch.isChecked();
        Boolean vipState = vipSwitch.isChecked();
        double rollVal = roll() + 1.0;
        boolean alphaPackWin = false;
        if (gameWin && percentage >= rollVal) {
            incrementNumAlphaPacks();
            alphaPackWin = true;
        }
        if (alphaPackWin) {
            checkMaxPercentage();
            checkMinPercentage();
            if (rankedCasualState) {
                percentage = RANKED_WIN_CHANCE;
            }
            else {
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
    }

    public void checkMinPercentage() {
        if (percentage < minPercentage) {
            minPercentage = percentage;
            maxPercentageTextView.setText(setMinMaxPercentage());
        }
    }

    public void checkMaxPercentage() {
        if (percentage > maxPercentage) {
            maxPercentage = percentage;
            maxPercentageTextView.setText(setMinMaxPercentage());
        }
    }

    public double roll() {
        Random rand = new Random();
        int rand_num = rand.nextInt(100);
        return (double) rand_num;
    }

    public void incrementNumGames() {
        numGamesInt++;
        numGamesTextView.setText(setGames());
    }

    public void incrementNumAlphaPacks() {
        numAlphaPacksInt++;
        alphaPacksTextView.setText(Integer.toString(numAlphaPacksInt));
    }

    // Called to reset current textViews
    public void resetNums(View view) {
        numAlphaPacksInt = 0;
        numWins = 0;
        numLosses = 0;
        numGamesInt = 0;
        percentage = 0.0;
        maxPercentage = percentage;
        alphaPacksTextView.setText(Integer.toString(numAlphaPacksInt));
        numGamesTextView.setText(setGames());
        percentageTextView.setText(setPercentage(percentage));
        maxPercentageTextView.setText(setMinMaxPercentage());
    }

    // Called to simulate a loss
    public void gameLoss(View view) {
        numLosses++;
        incrementNumGames();
        updatePercentage(false);
    }

    // Called to simulate a win
    public void gameWin(View view) {
        numWins++;
        incrementNumGames();
        updatePercentage(true);
    }
}

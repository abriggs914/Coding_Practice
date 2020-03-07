package com.example.abrig.minesweeper;

import android.content.SharedPreferences;
import android.graphics.Rect;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class RecordsView extends AppCompatActivity {

//    private HashMap<String, String> values;

    private TextView gamesPlayedTextView, gamesWonTextView, gamesLostTextView;
    private TextView averageTimeTextView, bestTimeTextView, worstTimeTextView;
    private TextView averageScoreTextView, bestScoreTextView, worstScoreTextView;
    private TextView difficultyRangeTextView, averageDifficultyTextView;
    private TextView topFiveTextView, lastFiveTextView;
    private ListView topFiveListView, lastFiveListView;
    private RadioButton bestTimeButton, worstTimeButton, bestScoreButton, worstScoreButton;
    private RadioGroup radioGroup;
    private FrameLayout difficultyFrameLayout;
    private RangeBar rangeBar;
//    private View viewSpace;

    public RecordsView(){}

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.records_view);

//        values = new HashMap<>();
//        setValues();

        gamesPlayedTextView = findViewById(R.id.numGamesReportTextView);
        gamesWonTextView = findViewById(R.id.gamesWonReportTextView);
        gamesLostTextView = findViewById(R.id.gamesLostReportTextView);

        averageTimeTextView = findViewById(R.id.averageTimeReportTextView);
        bestTimeTextView = findViewById(R.id.bestTimeReportTextView);
        worstTimeTextView = findViewById(R.id.worstTimeReportTextView);

        averageScoreTextView = findViewById(R.id.averageScoreReportTextView);
        bestScoreTextView = findViewById(R.id.bestScoreReportTextView);
        worstScoreTextView = findViewById(R.id.worstScoreReportTextView);

        topFiveTextView = findViewById(R.id.top5ReportTextView);
        lastFiveTextView = findViewById(R.id.last5ReportTextView);

        topFiveListView = findViewById(R.id.top5ListView);
        lastFiveListView = findViewById(R.id.last5ListView);

        bestTimeButton = findViewById(R.id.bestTimeRadioButton);
        worstTimeButton = findViewById(R.id.worstTimeRadioButton);
        bestScoreButton = findViewById(R.id.bestScoreRadioButton);
        worstScoreButton = findViewById(R.id.worstScoreRadioButton);

        difficultyRangeTextView = findViewById(R.id.difficultyReportTextView);
        averageDifficultyTextView = findViewById(R.id.averageDifficultyReportTextView);
        difficultyFrameLayout = findViewById(R.id.difficultyFrameLayout);

        radioGroup = findViewById(R.id.radioGroup); //new RadioGroup(this);

        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                updateTopFiveList();
            }
        });

        init();
    }

    public void updateLastFiveList() {
        ArrayList<String> arr = getLast5Games();
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this, R.layout.activity_list_view, R.id.textView, arr);
        lastFiveListView.setAdapter(arrayAdapter);
    }

    public void updateTopFiveList() {
        // TODO
        ArrayList<String> arr;
        arr = new ArrayList<>(getBestTimeGames());
        int buttonId = radioGroup.getCheckedRadioButtonId();
        if (buttonId == R.id.bestTimeRadioButton) { //bestTimeButton.isActivated()) {
            System.out.println("bestTime is selected");
//            arr = new ArrayList<>(getBestTimeGames());
        }
        else if(buttonId == R.id.worstTimeRadioButton) { // worstTimeButton.isActivated()) {
            System.out.println("worstTime is selected");
//            arr = new ArrayList<>(getWorstTimeGames());
        }
        else if(buttonId == R.id.bestScoreRadioButton) { // bestScoreButton.isActivated()) {
            System.out.println("bestScore is selected");
//            arr = new ArrayList<>(getBestScoreGames());
        }
        else if (buttonId == R.id.worstScoreRadioButton) {
            System.out.println("worstScore is selected");
        }
        else {
            System.out.println("none selected");
        }
//            arr = new ArrayList<>(getWorstScoreGames());
//        }

        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this, R.layout.activity_list_view, R.id.textView, arr);
        topFiveListView.setAdapter(arrayAdapter);
    }

    public ArrayList<String> getBestTimeGames() {
        // TODO
        ArrayList<String> gamesList = SharedPreferencesHandler.getGamesStringList();
        PriorityQueue<String> top5Games = new PriorityQueue<>();
        System.out.println("GAMESLIST: " + gamesList);
        for (String game : gamesList) {
            if (top5Games.size() < 5) {
                top5Games.add(game);
            }
            else {
                // do the priority shuffling
//                for (String s : top5Games) {
//                    if ()
//                }
            }
        }
        ArrayList<String> res = new ArrayList<>();
        String message = "Best games:";
        for (String game : top5Games) {
            System.out.println("game: " + game);
            Game g = GameHistoryParser.getGameFromString(game);
            res.add(g.toString());
            message += ("\n\t" + g);
        }
        System.out.println(message);
        return res;
    }

    public ArrayList<String> getWorstTimeGames() {
        // TODO
        return null;
    }
    public ArrayList<String> getBestScoreGames() {
        // TODO
        return null;
    }
    public ArrayList<String> getWorstScoreGames() {
        // TODO
        return null;
    }
    public ArrayList<String> getLast5Games() {
        ArrayList<String> gamesList = SharedPreferencesHandler.getGamesStringList();
        gamesList.clear();
        gamesList.addAll(Arrays.asList("This", "part", "hasn\'t", "been", "done", "yet"));
        return gamesList;
    }

//    public void setValues() {
//        SharedPreferences prefs = MainActivity.preferences;
//        Map<String, ?> map = prefs.getAll();
//        ArrayList<String> keys = MainActivity.getKeys();
//        for(String key : keys) {
//            String val;
//            try {
//                val = (String) map.get(key);
//            }
//            catch (Exception e) {
//                System.out.println("key: " + key + " is null.");
//                val = null;
//            }
//            if (val == null) {
//                val = "0";
//            }
////            this.values.put(key, val);
//            System.out.println("key: " + key + ", val: " + val);
//        }
//    }

    private void init() {
        rangeBar = new RangeBar(this, 1, 100, difficultyRangeTextView);
        FrameLayout.LayoutParams lparams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT);
        rangeBar.setLayoutParams(lparams);
//        rangeBar.setPaletteSelection(1);
        rangeBar.setShowNumbers(true);
        rangeBar.setShowTicks(true);

        difficultyFrameLayout.addView(rangeBar);

        setFields();
    }

    public void setFields() {
        gamesPlayedTextView.setText(String.valueOf(SharedPreferencesHandler.getNumGames()));
        gamesWonTextView.setText(String.valueOf(SharedPreferencesHandler.getWonGames()));
        gamesLostTextView .setText(String.valueOf(SharedPreferencesHandler.getLostGames()));

        averageTimeTextView.setText(Utilities.parseTime(SharedPreferencesHandler.getAverageTime()));
        bestTimeTextView.setText(Utilities.parseTime(SharedPreferencesHandler.getBestTime()));
        worstTimeTextView .setText(Utilities.parseTime(SharedPreferencesHandler.getWorstTime()));

        averageScoreTextView.setText(String.valueOf(SharedPreferencesHandler.getAverageScore()));
        bestScoreTextView.setText(String.valueOf(SharedPreferencesHandler.getBestScore()));
        worstScoreTextView.setText(String.valueOf(SharedPreferencesHandler.getWorstScore()));

        int[] range = rangeBar.getRange();
        difficultyRangeTextView.setText(("range: " + Utilities.keyify(range[0], range[1])));
        averageDifficultyTextView.setText(String.valueOf(SharedPreferencesHandler.getAverageDifficulty()));

        topFiveTextView.setText(String.valueOf(SharedPreferencesHandler.getTopFiveString()));
        lastFiveTextView.setText(String.valueOf(SharedPreferencesHandler.getLastFiveString()));

        updateLastFiveList();
    }

}

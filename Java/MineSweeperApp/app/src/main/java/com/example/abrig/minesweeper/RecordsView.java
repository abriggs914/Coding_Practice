package com.example.abrig.minesweeper;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.ArrayAdapter;
import android.widget.FrameLayout;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import com.example.abrig.minesweeper.Game.GameNumberComparator;

import java.util.ArrayList;
import java.util.Collections;
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
                updateTopNList(SharedPreferencesHandler.getGamesList(RecordsView.this).size());
            }
        });

        difficultyRangeTextView.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                updateTopNList(100);
            }
        });

        init();
    }

    public void updateLastNList(int n) {
        ArrayList<Game> originalGames = SharedPreferencesHandler.getGamesList(RecordsView.this);
        ArrayList<Game> difficultyGames = new ArrayList<>();
        int[] range = rangeBar.getRange();
        for (Game g : originalGames) {
            if (Utilities.inRange(range[0], g.getDifficulty(), range[1])) {
                difficultyGames.add(g);
            }
        }
        ArrayList<String> arr = getLastNGames(n, difficultyGames);
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this, R.layout.activity_list_view, R.id.textView, arr);
        lastFiveListView.setAdapter(arrayAdapter);
    }

    public void updateTopNList(int n) {
        // TODO
        ArrayList<String> arr;
        int buttonId = radioGroup.getCheckedRadioButtonId();
        String message = "Top " + n + " game" + ((n == 0)? "" :"s");
        ArrayList<Game> originalGames = SharedPreferencesHandler.getGamesList(RecordsView.this);
        ArrayList<Game> difficultyGames = new ArrayList<>();
        int[] range = rangeBar.getRange();
        for (Game g : originalGames) {
            if (Utilities.inRange(range[0], g.getDifficulty(), range[1])) {
                difficultyGames.add(g);
            }
        }
        System.out.println("originalGames: " + originalGames);
        System.out.println("difficultyGames" + Utilities.keyify(range[0], range[1]) + ": " + difficultyGames);

        if (buttonId == R.id.bestTimeRadioButton) { //bestTimeButton.isActivated()) {
            System.out.println("bestTime is selected");
            message += " by best time";
            arr = new ArrayList<>(getBestTimeGames(n, difficultyGames));
        }
        else if(buttonId == R.id.worstTimeRadioButton) { // worstTimeButton.isActivated()) {
            System.out.println("worstTime is selected");
            message += " by worst time";
            arr = new ArrayList<>(getWorstTimeGames(n, difficultyGames));
        }
        else if(buttonId == R.id.bestScoreRadioButton) { // bestScoreButton.isActivated()) {
            System.out.println("bestScore is selected");
            message += " by best score";
            arr = new ArrayList<>(getBestScoreGames(n, difficultyGames));
        }
        else if (buttonId == R.id.worstScoreRadioButton) {
            System.out.println("worstScore is selected");
            message += " by worst score";
            arr = new ArrayList<>(getWorstScoreGames(n, difficultyGames));
        }
        else {
            arr = new ArrayList<>();
            System.out.println("none selected");
        }
        message += ", difficulty range " + rangeBar.getStringRange() + ":";

//        for (String)

        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this, R.layout.activity_list_view, R.id.textView, arr);
        topFiveListView.setAdapter(arrayAdapter);
        topFiveTextView.setText(message);
    }

    public ArrayList<String> getBestTimeGames(int n, ArrayList<Game> gamesList) {
        ArrayList<String> res = new ArrayList<>();
        if (n == 0 || gamesList.size() == 0) {
            return res;
        }
        n = Math.max(0, Math.min(n, gamesList.size()));
        PriorityQueue<Game> queue = new PriorityQueue<>(gamesList.size(), new Game.GameTimeComparator());
        queue.addAll(gamesList);
        System.out.println("Queue ("+queue.size()+"): " + queue);
        int t = queue.size();
        for (int i = 0; i < Math.min(n, t); i++) {
            Game g = queue.poll();
            System.out.println("\ti: " + i + ", t: " + t + ", n: " + n + "queue.size(): " + queue.size() + ", (i >= t - n): " + (i >= (t - n)) + ", game: " + g);
//            if (i >= (t - 5)) {
                res.add(g.toString());
//            }
        }
        return res;
    }

    public ArrayList<String> getWorstTimeGames(int n, ArrayList<Game> gamesList) {
        ArrayList<String> res = new ArrayList<>();
        if (n == 0 || gamesList.size() == 0) {
            return res;
        }
//        ArrayList<Game> gamesList = SharedPreferencesHandler.getGamesList();
        n = Math.max(0, Math.min(n, gamesList.size()));
        PriorityQueue<Game> queue = new PriorityQueue<>(gamesList.size(), new Game.GameTimeComparator());
        queue.addAll(gamesList);
        System.out.println("Queue ("+queue.size()+"): " + queue);
        int t = queue.size();
        for (int i = 0; i < t; i++) {
            Game g = queue.poll();
            System.out.println("\ti: " + i + ", t: " + t + ", n: " + n + "queue.size(): " + queue.size() + ", (i >= t - n): " + (i >= (t - n)) + ", game: " + g);
            if (i >= (t - n)) {
                res.add(g.toString());
            }
        }
        Collections.reverse(res);
        return res;
    }

    public ArrayList<String> getBestScoreGames(int n, ArrayList<Game> gamesList) {
        ArrayList<String> res = new ArrayList<>();
        if (n == 0 || gamesList.size() == 0) {
            return res;
        }
//        ArrayList<Game> gamesList = SharedPreferencesHandler.getGamesList();
        n = Math.max(0, Math.min(n, gamesList.size()));
        PriorityQueue<Game> queue = new PriorityQueue<>(gamesList.size(), new Game.GameScoreComparator());
        queue.addAll(gamesList);
        System.out.println("Queue ("+queue.size()+"): " + queue);
        int t = queue.size();
        for (int i = 0; i < t; i++) {
            Game g = queue.poll();
            System.out.println("\ti: " + i + ", t: " + t + ", n: " + n + "queue.size(): " + queue.size() + ", (i >= t - n): " + (i >= (t - n)) + ", game: " + g);
            if (i >= (t - n)) {
                res.add(g.toString());
            }
        }
        Collections.reverse(res);
        return res;
    }

    public ArrayList<String> getWorstScoreGames(int n, ArrayList<Game> gamesList) {
        ArrayList<String> res = new ArrayList<>();
        if (n == 0 || gamesList.size() == 0) {
            return res;
        }
//        ArrayList<Game> gamesList = SharedPreferencesHandler.getGamesList();
        n = Math.max(0, Math.min(n, gamesList.size()));
        PriorityQueue<Game> queue = new PriorityQueue<>(gamesList.size(), new Game.GameScoreComparator());
        queue.addAll(gamesList);
        System.out.println("Queue ("+queue.size()+"): " + queue);
        int t = queue.size();
        for (int i = 0; i < Math.min(n, t); i++) {
            Game g = queue.poll();
            System.out.println("\ti: " + i + ", t: " + t + ", n: " + n + "queue.size(): " + queue.size() + ", (i >= t - n): " + (i >= (t - n)) + ", game: " + g);
//            if (i >= (t - 5)) {
                res.add(g.toString());
//            }
        }
        return res;
    }

    public ArrayList<String> getLastNGames(int n, ArrayList<Game> gamesList) {
        ArrayList<String> res = new ArrayList<>();
        if (n == 0 || gamesList.size() == 0) {
            return res;
        }
        n = Math.max(0, Math.min(n, SharedPreferencesHandler.getGamesList(RecordsView.this).size()));
//        ArrayList<Game> gamesList = SharedPreferencesHandler.getGamesList();
        PriorityQueue<Game> queue = new PriorityQueue<>(gamesList.size(), new GameNumberComparator());
        queue.addAll(gamesList);
        System.out.println("Queue ("+queue.size()+"): " + queue);
        int t = queue.size();
        for (int i = 0; i < t; i++) {
            Game g = queue.poll();
            System.out.println("\ti: " + i + ", t: " + t + "queue.size(): " + queue.size() + ", (i >= t - 5): " + (i >= (t - 5)) + ", game: " + g);
            if (i >= (t - n)) {
                res.add(g.toString());
            }
        }
        Collections.reverse(res);
        return res;
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
        rangeBar.setPaletteSelection(1);
        rangeBar.setShowNumbers(true);
        rangeBar.setShowTicks(true);
        rangeBar.setMajorMinor(true);
        rangeBar.setMajorMinorRatio(0.25);

        difficultyFrameLayout.addView(rangeBar);

//        // game_num, win/loss(1/0), time, score, searched
//        String gameString2 = "2,  1,  800,  100,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString3 = "3,  0,  500,  55,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString4 = "4,  1,  850,  100,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString5 = "5,  0,  300,  13,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString6 = "6,  0,  15,  85,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString7 = "7,  1,  601,  100,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
//        String gameString8 = "8,  0,  99,  5,  0, [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]], [[0, 0, 77, 0, 0][0, 0, 0, 0, 0][0, 0, 80, 0, 0][0, 77, 80, 0, 0][0, 77, 0, 80, 0][0, 0, 0, 0, 80]]";
////        Game game1 = GameHistoryParser.getGameFromString(gameString1);
////        System.out.println("game1: " + game1);
//        SharedPreferencesHandler.write("game #00002", gameString2);
//        SharedPreferencesHandler.write("game #00003", gameString3);
//        SharedPreferencesHandler.write("game #00004", gameString4);
//        SharedPreferencesHandler.write("game #00005", gameString5);
//        SharedPreferencesHandler.write("game #00006", gameString6);
//        SharedPreferencesHandler.write("game #00007", gameString7);
//        SharedPreferencesHandler.write("game #00008", gameString8);

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

        topFiveTextView.setText(String.valueOf(SharedPreferencesHandler.getTopNGamesString(RecordsView.this,100)));
        lastFiveTextView.setText(String.valueOf(SharedPreferencesHandler.getLastNGamesString(RecordsView.this,100)));

        updateLastNList(SharedPreferencesHandler.getGamesList(RecordsView.this).size());
    }

}

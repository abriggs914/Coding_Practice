package com.example.cluenotebook;

import android.content.Context;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

public class PlayerEntry extends AppCompatActivity {

    private int numPlayerEntries;
    private ArrayList<Player> players;
    private ArrayList<PersonE> selectedColours;

    private Button quitButton;
    private Button addButton;
    private LinearLayout playerEntryLayout;

    private class Widget extends LinearLayout {

        private EditText nameEntry;
        private LinearLayout listView;
        private int selectedColourIdx;

        @RequiresApi(api = Build.VERSION_CODES.O)
        public Widget(Context context) {
            super(context);
            this.selectedColourIdx = -1;
//            this.setStyle("-fx-border-color: black");
            this.setPadding(5, 5, 5, 5);
            this.setBackgroundColor(Color.rgb(0, 0, 0));

            nameEntry = new EditText(context);
            nameEntry.setHint("Enter a name");

            listView = new LinearLayout(context);
//            listView.setBackgroundColor(Color.argb(1, 0.65, 0.65, 0.65));
            listView.setBackgroundColor(Color.rgb(0.65f, 0.65f, 0.65f));

            ArrayList<View> remainingColours = remainingColours();
            LinearLayout firstCol = new LinearLayout(context);
            LinearLayout secondCol = new LinearLayout(context);
            firstCol.setOrientation(VERTICAL);
            secondCol.setOrientation(VERTICAL);
            for (int i = 0; i < remainingColours.size(); i++) {
                View v = remainingColours.get(i);
                if (i < 3) {
                    firstCol.addView(v);
//            ArrayAdapter<TextView> adapter = new ArrayAdapter<TextView>(this, R.layout.activity_list_view, R.id.textView, arr);
                }
                else {
                    secondCol.addView(v);
                }
            }
            firstCol.setMinimumWidth(listView.getWidth() / 2);
            secondCol.setMinimumWidth(listView.getWidth() / 2);
            listView.addView(firstCol);
            listView.addView(secondCol);
            View[] views = new View[] {nameEntry, listView};
            for (View v : views) {
                this.addView(v);
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.player_entry);

        this.numPlayerEntries = 2;
        this.selectedColours = new ArrayList<>();

        quitButton = findViewById(R.id.player_entry_quit_button);
        addButton = findViewById(R.id.addPlayer);
        playerEntryLayout = findViewById(R.id.player_entry_layout);

        addButton.setOnClickListener(v -> {
            if (numPlayerEntries < 6) {
                numPlayerEntries++;
                createPlayerEntry();
            }
        });

        quitButton.setOnClickListener(v -> {
//            TODO collect each player info
            finish();
        });
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void createPlayerEntry() {
//        LinearLayout layout = new LinearLayout(this);
//        EditText nameEntry = new EditText(this);
//        nameEntry.setHint("Enter a name");
////        sd
//
//        ListView listView = new ListView(this);
//        View[] views = new View[] {nameEntry};
//        for (View v : views) {
//            layout.addView(v);
//        }

//        playerEntryLayout.addView(layout);
        playerEntryLayout.addView(new Widget(this));
    }

    public ArrayList<View> remainingColours() {
        ArrayList<View> arr = new ArrayList<>();
        for (PersonE p : PersonE.values()) {
            if (!selectedColours.contains(p)) {
                LinearLayout linearLayout = new LinearLayout(this);
                ImageView token = new ImageView(this);
                token.setImageResource(p.drawableID);
//                token.setScaleType(ImageView.ScaleType.FIT_XY);
//                TODO fix the height and widths of images icons, to they dont stretch the layout
                token.setMaxWidth(60);
                token.setMaxHeight(60);
                TextView txt = new TextView(this);
                txt.setText(p.colour);
                txt.setTextColor(Color.parseColor(p.colour));
                linearLayout.addView(token);
                linearLayout.addView(txt);
                arr.add(linearLayout);
            }
        }
        return arr;
    }
}

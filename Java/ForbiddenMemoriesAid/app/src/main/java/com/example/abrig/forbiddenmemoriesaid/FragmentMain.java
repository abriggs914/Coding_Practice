package com.example.abrig.forbiddenmemoriesaid;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.Toast;

public class FragmentMain extends AppCompatActivity {
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        CardIndexer cardIndexer = new CardIndexer();
//        cardIndexer.initCombosTable();
//        setContentView(R.layout.fragment_main);

//        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
//        setSupportActionBar(toolbar);
        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
//        mSectionsPagerAdapter = new MainActivity.SectionsPagerAdapter(getSupportFragmentManager());

        // Set up the ViewPager with the sections adapter.
//        mViewPager = (ViewPager) findViewById(R.id.container);
//        mViewPager.setAdapter(mSectionsPagerAdapter);

//        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
//        fab.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
//                        .setAction("Action", null).show();
//            }
//        });

    }

    public void method1(View view){
//        Runnable runnable = new Runnable() {
//            @Override
//            public void run() {
                AutoCompleteTextView textView = findViewById(R.id.autocomplete_cardList);
                String[] cards = getResources().getStringArray(R.array.cardList);
                ArrayAdapter<String> adapter =
                        new ArrayAdapter<String>(FragmentMain.this, android.R.layout.simple_list_item_1, cards);
                textView.setAdapter(adapter);
                String line = "Hey there";
                Toast.makeText(FragmentMain.this, line, Toast.LENGTH_LONG).show();
//            }
//        };
//        Thread myThread = new Thread(runnable);
//        myThread.start();

    }
}

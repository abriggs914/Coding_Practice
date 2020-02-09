package com.example.abrig.spendinglog;

import android.app.Application;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private Button resetPreferencesButton;

    public static SharedPreferences prefs = null;
    public static FragmentTransaction transaction;
    public static TransactionHandler TH;
//    private TextView mTextMessage;

    private final BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
//                    mTextMessage.setText(R.string.title_home);
                    resetPreferencesButton.setVisibility(View.INVISIBLE);
                    openFragment(TransactionView.newInstance("", ""));
                    return true;
                case R.id.navigation_dashboard:
//                    mTextMessage.setText(R.string.title_dashboard);
                    resetPreferencesButton.setVisibility(View.INVISIBLE);
                    openFragment(EntityView.newInstance("", ""));
                    return true;
                case R.id.navigation_notifications:
//                    mTextMessage.setText(R.string.title_notifications);
                    resetPreferencesButton.setVisibility(View.INVISIBLE);
                    openFragment(UserView.newInstance("", ""));
                    return true;
            }
            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prefs = getSharedPreferences("com.example.spendinglog", MODE_PRIVATE);

        // ask user to start from a new application state on launch.
        resetPreferencesButton = findViewById(R.id.resetPeferencesButton);
        resetPreferencesButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetPreferences();
            }
        });
        resetPreferences();
        //

        TH = new TransactionHandler();

//        Map<String, ?> keysValues = prefs.getAll();
//        System.out.println("CLEARING");
//        for (String s : keysValues.keySet()) {
//            Class clazz = keysValues.get(s).getClass();
//            System.out.println("Key: " + s + ", clazz: " + clazz + ", value: " + keysValues.get(s));
//        }

//        mTextMessage = (TextView) findViewById(R.id.message);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);




//        Entity me = new Entity("avery", 200000, true);
//        Entity power = new Entity("Power", Integer.MAX_VALUE);
//        Entity rent = new Entity("rent", Integer.MAX_VALUE);
//        Entity gst = new Entity("GST", Integer.MAX_VALUE);
//        TransactionHandler TH = new TransactionHandler();
//        boolean t1 = TH.tryTransaction(me, power, 10005, true, "");
//        boolean t2 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t3 = TH.tryTransaction(me, power, 10005, true, "");
//        boolean t4 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t5 = TH.tryTransaction(gst, me, 14700, true, "");
//        boolean t6 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t7 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t8 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t9 = TH.tryTransaction(me, rent, 37550, true, "");
//        boolean t10 = TH.tryTransaction(me, rent, 37550, true, "");
//
//        System.out.println("Transactions: \n" + t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5);
//        System.out.println(t6 + "\n" + t7 + "\n" + t8 + "\n" + t9 + "\n" + t10);
//        System.out.println(me.getTransactions());
//        System.out.println(me.getCustomerStats());
//        Utilities.createCSV(me.getTransactions());


//        prefs.edit().putBoolean("firstrun", true).apply();
    }

    public void resetPreferences() {
        prefs.edit().clear().commit();
        prefs = getSharedPreferences("com.example.spendinglog", MODE_PRIVATE);
        resetPreferencesButton.setVisibility(View.INVISIBLE);
        if (TH != null){
            TH.resetTransactionHandler();
        }
        onResume();
    }

    public void openFragment(Fragment fragment) {
        transaction = getSupportFragmentManager().beginTransaction();
        transaction.replace(R.id.container, fragment);
        transaction.addToBackStack(null);
        transaction.commit();
    }


    @Override
    protected void onResume() {
        super.onResume();

        if (prefs.getBoolean("firstrun", true)) {

            SharedPreferencesWriter.write("firstrun", false);

            System.out.print("KEY SET: " + MainActivity.prefs.getAll().keySet());
            for (String s : MainActivity.prefs.getAll().keySet()) {
                System.out.print("String entry: " + s);
            }
            System.out.println("\n\n\n\tFIRST RUN\n\n\n");
            openFragment(UserProfile.newInstance("", ""));
        }
        else {
            System.out.print("\n\n\n\tNOT THE FIRST RUN\n\n\n");
        }
    }

}

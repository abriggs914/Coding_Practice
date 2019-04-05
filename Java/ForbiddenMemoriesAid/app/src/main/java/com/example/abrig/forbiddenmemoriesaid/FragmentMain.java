package com.example.abrig.forbiddenmemoriesaid;

import android.os.Bundle;
import android.os.Looper;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.zip.Inflater;

public class FragmentMain extends Fragment {

    private final String TAG = "FragmentMainTag";
    private AutoCompleteTextView textView;

    @Nullable
    @Override
    public View onCreateView(final LayoutInflater inflater, @Nullable final ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_main, container, false);
        textView = view.findViewById(R.id.autocomplete_cardList);
        textView.setDropDownHeight(5);
//        textView.seto
        Button searchButtonSubmit = view.findViewById(R.id.submit_button);
        searchButtonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                Runnable runnable = new Runnable() {
//                    @Override
//                    public void run() {
//                        Looper.prepare();
                        View view1 = inflater.inflate(R.layout.fragment_main, container, false);
//                        AutoCompleteTextView textView = view1.findViewById(R.id.autocomplete_cardList);
                        TextView rw = view1.findViewById(R.id.resultsWindow);
                        String[] cards = getResources().getStringArray(R.array.cardList);
                        ArrayAdapter<String> adapter =
                                new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, cards);
                        textView.setAdapter(adapter);
                        String line = "Hey there";
                        line = textView.getText().toString();
                        line = "ENTRY: " + line;
                        rw.setText(line);
                        Toast.makeText(getActivity(), line, Toast.LENGTH_LONG).show();
                        Log.i(TAG, "IN THE ONCLICK METHOD line: " + line + "\n");
                        Log.i(TAG, "IN THE ONCLICK METHOD");
//                    }
//                };
//                Thread myThread = new Thread(runnable);
//                myThread.start();
            }
        });
        return view;
    }
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

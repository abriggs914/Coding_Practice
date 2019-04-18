package com.example.abrig.forbiddenmemoriesaid;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

import static com.example.abrig.forbiddenmemoriesaid.R.id.text_view_list_item;
import static com.example.abrig.forbiddenmemoriesaid.R.layout.custom_list_item;

public class FragmentMain extends Fragment {

    private final String TAG = "FragmentMainTag";
    private AutoCompleteTextView textView;
    private CardIndexer cardIndexer;
    private Card[] cardsList;

    private ArrayList<Card> inputCards;

    @Nullable
    @Override
    public View onCreateView(final LayoutInflater inflater, @Nullable final ViewGroup container, @Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        View view = inflater.inflate(R.layout.fragment_main, container, false);
        String[] listofCards = getResources().getStringArray(R.array.cardList);

        final AutoCompleteTextView textView = view.findViewById(R.id.autocomplete_cardList);
        ArrayAdapter<String> adapter;
        // Have to call getActivity() to get context.
        adapter = new ArrayAdapter<String>(getActivity(),
                custom_list_item, text_view_list_item, listofCards);
        textView.setAdapter(adapter);

        cardIndexer = MainActivity.getCardIndexer();
        cardsList = cardIndexer.cardsList;
        inputCards = new ArrayList<Card>();

        final TextView rw = view.findViewById(R.id.resultsWindow);
        Button searchButtonSubmit = view.findViewById(R.id.submit_button);
        searchButtonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String input = textView.getText().toString();
                input = deciperInput(input);
                if(input.length() > 0) {
                    Card card = getInputCard(input);
                    inputCards.add(card);
                    rw.setText(inputCards.toString());
                }
                else{
                    Toast.makeText(getActivity(), "Invalid card", Toast.LENGTH_SHORT).show();
                }
            }
        });
        return view;
    }

    private String deciperInput(String input) {
        input = input.trim();
        if(input.length() == 0) {
            return input;
        }
        else if(input.length() < 4 && input.charAt(0) != 'Z' && input.charAt(0) != 'z'){
            try{
                int x = Integer.parseInt(input);
                return Integer.toString(x-1);
            }
            catch (Exception e){
               return "";
            }
        }
        else{
            for(int i = 0; i < cardsList.length; i++){
                String temp = cardsList[i].getName().toLowerCase();
                if(input.toLowerCase().equals(temp)){
                    return Integer.toString(cardsList[i].id);
                }
            }
            return "";
        }
    }

    private Card getInputCard(String card){
        int x = Integer.parseInt(card);
        return cardIndexer.cardsList[x];
    }
        /*super.onCreate(savedInstanceState);
        View view = inflater.inflate(R.layout.fragment_main, container, false);
        textView = view.findViewById(R.id.autocomplete_cardList);
        textView.setDropDownHeight(5);

        String[] cardList = getResources().getStringArray(R.array.cardList);

        //AutoCompleteTextView editText = findViewById(R.id.actv);
        ArrayAdapter<String> adapter;
        adapter = new ArrayAdapter<String>(this, R.layout.custom_list_item, R.id.text_view_list_item, cardList);
        textView.setAdapter(adapter);
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
    }*/
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

package com.example.abrig.spendinglog;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.app.AppCompatDialogFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;
import java.util.Date;

public class InDepthEntityView extends Fragment implements AddFiltersDialog.ExampleDialogListener{

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private boolean edited;

    private String currentFilterString;

    private String name;
    private String idString;
    private boolean allowedOverDraft;
    private int bankedMoney;
    private int sentMoney;
    private int receivedMoney;
    private int largestTransactionAmount;
    private int leastTransactionAmount;
    private int avgTransactionAmount;
    private double earliestTransaction;
    private double latestTransaction;
    private double avgTransactionTime;
    private Date firstTransactionDate;
    private Date lastTransactionDate;

    private FragmentManager supportFragmentManager;
    private boolean quitGameResponse, shuffleGridResponse, resetGame, gameOverHandled;

    private ImageButton inDepthBackButton;
    private ImageButton addFilterButton;
    private ListView filterListView;

    private PieChart pieChart;
    private PieData pieData;
    private PieDataSet pieDataSet;
    private ArrayList pieEntries;
    private ArrayList PieEntryLabels;

    private Entity comparingEntity;

    public InDepthEntityView() {
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment HomeFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static InDepthEntityView newInstance(String param1, String param2) {
        InDepthEntityView fragment = new InDepthEntityView();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        String s = "Filter on create:\n\t" + MainActivity.TH.getCurrentFilterString();
        Toast.makeText(getActivity(), s, Toast.LENGTH_SHORT).show();
        this.currentFilterString = MainActivity.TH.getCurrentFilterString();
        this.supportFragmentManager = getChildFragmentManager();
        // Inflate the layout for this fragment
        edited = false;
        final View view = inflater.inflate(R.layout.in_depth_entity_view, container, false);

        pieChart = view.findViewById(R.id.pieChart);
        inDepthBackButton = (ImageButton) view.findViewById(R.id.inDepthBackButton);
        addFilterButton = view.findViewById(R.id.addFilterButton);
        filterListView = view.findViewById(R.id.filtersListView);

        getEntries();
        pieDataSet = new PieDataSet(pieEntries, "Pie Entries");
        pieData = new PieData(pieDataSet);
        pieChart.setData(pieData);
        pieDataSet.setColors(ColorTemplate.JOYFUL_COLORS);
        pieDataSet.setSliceSpace(2f);
        pieDataSet.setValueTextColor(Color.WHITE);
        pieDataSet.setValueTextSize(10f);
        pieDataSet.setSliceSpace(5f);
//        saveButton = view.findViewById(R.id.saveButton);
//        closeButton = view.findViewById(R.id.closeButton);
//        overdraftSwitch = view.findViewById(R.id.allowedOverDraftSwitch);
//        nameEditText = view.findViewById(R.id.nameEditText);
//        bankedEditText = view.findViewById(R.id.bankedEditText);

        // TODO: finish arrayAdapter
//        ArrayAdapter<View> filtersAdapter = new ;
//        filterListView.setAdapter(filtersAdapter);

        inDepthBackButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("in depth image button clicked");
                closeFragment();
            }
        });

        addFilterButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showFragment(getActivity(), new Bundle(), new AddFiltersDialog());
            }
        });

        filterListView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
                System.out.println("Trying to remove item # (" + position + "), id: (" + id + ")");
                char[] newFilter = currentFilterString.toCharArray();
                newFilter[position] = '9';
                MainActivity.TH.setInDepthFilters(new String(newFilter));
                return false;
            }
        });

        return view;
    }

    public void closeFragment() {
        getFragmentManager().popBackStack();
    }

    private void getEntries() {
        pieEntries = new ArrayList<>();
        pieEntries.add(new PieEntry(2f, 0));
        pieEntries.add(new PieEntry(4f, 1));
        pieEntries.add(new PieEntry(6f, 2));
        pieEntries.add(new PieEntry(8f, 3));
        pieEntries.add(new PieEntry(8f, "LABEL"));
        pieEntries.add(new PieEntry(7f, 4));
        pieEntries.add(new PieEntry(3f, 5));
        pieEntries.add(new PieEntry(18f, 6));
    }

    // show filter alert dialog pop-up
    public void showFragment(Activity activity, Bundle bundle, AppCompatDialogFragment fragmentClass) {
        FragmentTransaction ft = ((AppCompatActivity) activity).getSupportFragmentManager().beginTransaction();
        fragmentClass.setArguments(bundle);
        fragmentClass.show(ft, null);
        fragmentClass.setTargetFragment(this, 0);
    }

    public void updateFilterList() {
        String activeFilters = MainActivity.TH.getCurrentFilterString();
    }

//     After dialog window is closed control resumes here with passed values
    @Override
    public void applyTexts(String filterString) {
        MainActivity.TH.setInDepthFilters(filterString);
//        System.out.println("\n\tCurrentFilterString: {" + currentFilterString + "}\n\tfilterString (InDepthEntityView): {" + filterString + "}\n");
        Toast.makeText(getActivity(), ("filterString InDepth: {" + filterString + "}"), Toast.LENGTH_LONG).show();
        updateFilterList();
    }
}
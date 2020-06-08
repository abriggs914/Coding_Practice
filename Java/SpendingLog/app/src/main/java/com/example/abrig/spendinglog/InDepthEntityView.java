package com.example.abrig.spendinglog;

import android.app.Activity;
import android.app.Application;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.app.AppCompatDialogFragment;
import android.view.GestureDetector;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.DatePicker;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;
import java.util.Arrays;
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

    private View view;
    private ArrayList<View> views;
    private ImageButton inDepthBackButton;
    private ImageButton addFilterButton;

    private TextView entityTitle;
    private Spinner entitySpinner;
    private TextView senderTitle;
    private Spinner senderSpinner;
    private TextView recipientTitle;
    private Spinner recipientSpinner;
    private TextView startDateTitle;
    private DatePicker startDatePicker;
    private TextView endDateTitle;
    private DatePicker endDatePicker;
    private TextView amountRangeTitle;
    private FrameLayout amountRangeFrame;
    private RangeBar rangeBar;
    private FrameLayout moneyAmountFrameLayout;

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
        this.view = view;

        pieChart = view.findViewById(R.id.pieChart);
        inDepthBackButton = (ImageButton) view.findViewById(R.id.inDepthBackButton);
        addFilterButton = view.findViewById(R.id.addFilterButton);

        entityTitle = view.findViewById(R.id.entityFilterTitleTextView);
        entitySpinner = view.findViewById(R.id.entityFilterDropDown);
        senderTitle = view.findViewById(R.id.senderFilterTitleTextView);
        senderSpinner = view.findViewById(R.id.senderFilterDropDown);
        recipientTitle = view.findViewById(R.id.recipientFilterTitleTextView);
        recipientSpinner = view.findViewById(R.id.recipientFilterDropDown);
        startDateTitle = view.findViewById(R.id.startDateFilterTitleTextView);
        startDatePicker = view.findViewById(R.id.startDatePicker);
        endDateTitle = view.findViewById(R.id.endDateFilterTitleTextView);
        endDatePicker = view.findViewById(R.id.endDatePicker);
        amountRangeTitle = view.findViewById(R.id.amountTitleTextView);
        amountRangeFrame = view.findViewById(R.id.amountFrameLayout);

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

        // old code for de-selecting a current filter from the listView approach.
        // the listView approach won't work due to the getView method in ArrayAdapter
        // only returns a string of the object, instead of inflating it's view.
//        filterListView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
//            @Override
//            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
//                System.out.println("Trying to remove item # (" + position + "), id: (" + id + ")");
//                char[] newFilter = currentFilterString.toCharArray();
//                newFilter[position] = '9';
//                MainActivity.TH.setInDepthFilters(new String(newFilter));
//                return false;
//            }
//        });

        views = new ArrayList<>(
                Arrays.asList(
                        entityTitle,
                        entitySpinner,
                        senderTitle,
                        senderSpinner,
                        recipientTitle,
                        recipientSpinner,
                        startDateTitle,
                        startDatePicker,
                        endDateTitle,
                        endDatePicker,
                        amountRangeTitle,
                        amountRangeFrame
                ));
        init();
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
//        ArrayList<View> filterViews = new ArrayList<>();
//        filterViews.add(entitySpinner);
        // entity
        for (int i = 0; i < views.size(); i += 2) {
            // TODO this doesn't work due to the number of views in the views list. It needs to be 16 long not 12
            int titleIdx = i / 2;
            int widgetIdx = titleIdx + 1;
            System.out.print("views.size(): " + views.size() + ", i: " + i + ", titleIdx: " + titleIdx + ", widgetIdx: " + widgetIdx);

            if (activeFilters.charAt(titleIdx) == '1') {
                views.get(titleIdx).setVisibility(View.VISIBLE);
                views.get(widgetIdx).setVisibility(View.VISIBLE);
                System.out.println(" IS 1");
            }
            else {
                views.get(titleIdx).setVisibility(View.INVISIBLE);
                views.get(widgetIdx).setVisibility(View.INVISIBLE);
                System.out.println(" ISNT 1");
            }
        }
//        if (activeFilters.charAt(0) == '1') {
//            entityTitle.setVisibility(View.VISIBLE);
//            entitySpinner.setVisibility(View.VISIBLE);
//        }

//        ArrayAdapter<View> filtersAdapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_list_item_1, filterViews);
//        filterListView.setAdapter(filtersAdapter);
    }

    private void init() {
        initEntity();
        initDates();
        initRangeBar();

        for (View v: views) {
            v.setVisibility(View.INVISIBLE);
        }

//        Toast.makeText(getActivity(), "INIT RANGEBAR: " + rangeBar.getStringRange(), Toast.LENGTH_SHORT).show();
//        setFields();
    }

    public void initEntity() {
        ArrayList<Entity> entitiesList = MainActivity.TH.getEntities();
        ArrayAdapter<Entity> entitiesAdapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_list_item_1, entitiesList);
        entitySpinner.setAdapter(entitiesAdapter);
        ArrayAdapter<Entity> senderAdapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_list_item_1, entitiesList);
        senderSpinner.setAdapter(senderAdapter);
        ArrayAdapter<Entity> recipientAdapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_list_item_1, entitiesList);
        recipientSpinner.setAdapter(recipientAdapter);
    }

    public void initDates() {
        Date[] dates = MainActivity.TH.getFirstLastTransactionDates();
        Date firstDate = dates[0];
        Date lastDate = dates[1];
        int[] first = new int[] {
                DateHandler.getYear(firstDate),
                DateHandler.getMonth(firstDate),
                DateHandler.getDay(firstDate),
        };
        int[] last = new int[] {
                DateHandler.getYear(lastDate),
                DateHandler.getMonth(lastDate),
                DateHandler.getDay(lastDate),
        };
        startDatePicker.updateDate(first[0], first[1], first[2]);
        endDatePicker.updateDate(last[0], last[1], last[2]);
    }

    public void initRangeBar() {
        rangeBar = new RangeBar(getActivity(), 1, 100);
        FrameLayout.LayoutParams lparams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT);
        rangeBar.setLayoutParams(lparams);
        rangeBar.setPaletteSelection(1);
        rangeBar.setShowNumbers(true);
        rangeBar.setShowTicks(true);
        rangeBar.setMajorMinor(true);
        rangeBar.setMajorMinorRatio(0.25);

        amountRangeFrame.addView(rangeBar);
    }

//     After dialog window is closed control resumes here with passed values
    @Override
    public void applyTexts(String filterString) {
        MainActivity.TH.setInDepthFilters(filterString);
//        System.out.println("\n\tCurrentFilterString: {" + currentFilterString + "}\n\tfilterString (InDepthEntityView): {" + filterString + "}\n");
        Toast.makeText(getActivity(), ("filterString InDepth: {" + currentFilterString + "}"), Toast.LENGTH_LONG).show();
        updateFilterList();
    }

    class AndroidGestureDetector implements GestureDetector.OnGestureListener, GestureDetector.OnDoubleTapListener {

        @Override
        public boolean onDown(MotionEvent e) {
            return false;
        }

        @Override
        public void onShowPress(MotionEvent e) {
        }

        @Override
        public boolean onSingleTapUp(MotionEvent e) {
            return false;
        }

        @Override
        public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
            return false;
        }

        @Override
        public void onLongPress(MotionEvent e) {
            System.out.println("On long press");
//            Grid grid = mineSweeper.getGameGrid();
//            int xpos = (int) e.getX();
//            int ypos = (int) e.getY();
//            if (!mineSweeper.isGameOver()) {
//                if (Utilities.inRange(getGridWidthSpace(), xpos, getWidth())) {
//                    if (Utilities.inRange(getGridHeightSpace(), ypos, getHeight())) {
//                        int[] rowCol = getRowColFromTap(xpos, ypos);
//                        int row = rowCol[0];
//                        int col = rowCol[1];
//                        int val = grid.getValueAt(row, col);
//                        boolean status = grid.getCheckStatusAt(row, col);
//                        switch (e.getAction()) {
//                            case MotionEvent.ACTION_DOWN:
//                                if (status) {
//                                    if (val == Utilities.POSSIBLE.charAt(0)) {
//                                        try {
//                                            mineSweeper.resetPossibleMine(row, col);
//                                        } catch (MineSweeperException e1) {
//                                        }
//                                    }
//                                }
//                                else {
//                                    mineSweeper.setPossibleMine(row, col);
//                                }
//                                break;
//                        }
//                        invalidate();
//                    }
//                }
//            }
        }

        @Override
        public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
            return false;
        }

        @Override
        public boolean onSingleTapConfirmed(MotionEvent e) {
            System.out.println("OnSingleTapConfirmed");
//            Grid grid = mineSweeper.getGameGrid();
//            int xpos = (int) e.getX();
//            int ypos = (int) e.getY();
//            boolean xRange = Utilities.inRange(getGridWidthSpace(), xpos, getWidth());
//            boolean yRange = Utilities.inRange(getGridHeightSpace(), ypos, getHeight());
//            if (!mineSweeper.isGameOver()) {
//                if (xRange) {
//                    if (yRange) {
//                        switch (e.getAction()) {
//                            case MotionEvent.ACTION_DOWN:
//                                int[] rowCol = getRowColFromTap(xpos, ypos);
//                                int row = rowCol[0];
//                                int col = rowCol[1];
//                                int val = grid.getValueAt(row, col);
//                                boolean status = grid.getCheckStatusAt(row, col);
//                                try {
//                                    if (status) {
//                                        Grid subGrid = mineSweeper.subGrid(grid, row - 1, row + 1, col - 1, col + 1);
//                                        Grid subGridSoln = mineSweeper.subGrid(mineSweeper.getSolnGrid(), row - 1, row + 1, col - 1, col + 1);
//                                        int subGridMines = subGrid.count(Utilities.MINE) + subGrid.count(Utilities.POSSIBLE);
//                                        int subGridSolnMines = subGridSoln.count(Utilities.MINE);
//                                        if (subGridMines == subGridSolnMines && val < 9) {
//                                            // all mines in the 3x3 grid are marked
//                                            mineSweeper.setSurroundingChecked(row, col);
//                                        } else {
//                                            animatedKeys = new ArrayList<>(grid.getUncheckedSurrounding(row, col));
//                                        }
//                                    } else {
//                                        boolean success = mineSweeper.selectSquare(row, col, true);
//                                    }
//                                } catch (MineSweeperException ignored) { }
//                                invalidate();
//                                break;
//                        }
//                    }
//                }
//            }
//            if (Utilities.inRange(0, ypos, getGridHeightSpace())) {
//                // check main button press
//                if (Utilities.inRange(80, ypos, 205)) {
//                    if (Utilities.inRange(50, xpos, 250)) {
//                        startQuitGame();
//                    }
//                }
//
//                // check reset smiley
//                if (Utilities.inRange(55, ypos, 205)) {
//                    if (Utilities.inRange(475, xpos, 625)) {
//                        startQuitGame();
//                    }
//                }
//            }
            return false;
        }

        @Override
        public boolean onDoubleTap(MotionEvent e) {
            return false;
        }

        @Override
        public boolean onDoubleTapEvent(MotionEvent e) {
            return false;
        }
    }
}
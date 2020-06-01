package com.example.abrig.spendinglog;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Switch;
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

        this.supportFragmentManager = getFragmentManager();
        // Inflate the layout for this fragment
        edited = false;
        final View view = inflater.inflate(R.layout.in_depth_entity_view, container, false);
//        Toast.makeText(getContext(), "Editing profile information...", Toast.LENGTH_SHORT).show();

        pieChart = view.findViewById(R.id.pieChart);
        inDepthBackButton = (ImageButton) view.findViewById(R.id.inDepthBackButton);
        addFilterButton = view.findViewById(R.id.addFilterButton);

        getEntries();
        pieDataSet = new PieDataSet(pieEntries, "");
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

                AddFiltersDialog popUp = new AddFiltersDialog();
                popUp.show(supportFragmentManager, "Quit?");

                applyTexts(quitGameResponse, shuffleGridResponse, resetGame);
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

    // After dialog window is closed control resumes here with passed values
    @Override
    public void applyTexts(boolean keepPlaying, boolean shuffle, boolean resetGame) {
        if (shuffle) {
            resetGame = true;
        }
        if (keepPlaying) {
            return;
        }
        else {
            return;
//            mineSweeperGrid.stopTimer();
//            mineSweeperGrid.getMineSweeper().setGameOver(true);
//            if (resetGame) {
//                String[][] stringGrid = mineSweeperGrid.getMineSweeper().getOriginalGrid().getStringGrid();
//                Grid grid = Grid.parseGrid(stringGrid);
//                try {
//                    mineSweeperGrid = new MineSweeperGrid(
//                            this,
//                            getSupportFragmentManager(),
//                            grid,
//                            0,
//                            0);
//                    if (shuffle) {
//                        mineSweeperGrid.shuffleGrid();
//                    }
//                    setContentView(mineSweeperGrid);
//                }
//                catch (MineSweeperException e) {
//                    e.printStackTrace();
//                    setMainMenu();
//                }
//            }
//            else {
//                setMainMenu();
//            }
//            mineSweeperGrid.handleGameOver();
        }
    }
}
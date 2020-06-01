package com.example.abrig.spendinglog;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.util.List;

public class TransactionEditing extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

//    private String name; // = MainActivity.prefs.getString("user_name", "user");
//    private boolean allowedOverDraft;
//    private String bankedMoneyString;
//    private int bankedMoney;
//
//    private TextView senderTextView;
//    private TextView receiverTextView;
//    private TextView balanceTextview;
//    private TextView oneTimeTextView;
//    private TextView occurringTextView;
//
//    private Switch oneTimeSwitch;
//    private EditText balanceEntryEditText;
//    private AutoCompleteTextView senderAutoTextView;
//    private AutoCompleteTextView receiverAutoTextView;
////    private AutoCompleteTextView occurringAutoTextView;
//
//    private Button saveButton;
//    private Button viewAllButton;
//    private Button clearFormButton;
//    private Spinner occurringDropDown;

    private ListView transactionsListView;

    private TextView selectedTextView;
    private TextView selectedReportTextView;
    private TextView totalTextview;
    private TextView totalReportTextView;

    private Button deleteButton;
    private Button selectAllButton;
    private Button clearSelectedButton;
    private Button closeButton;

    public TransactionEditing() {
    }

    // TODO: Rename and change types and number of parameters
    public static TransactionEditing newInstance(String param1, String param2) {
        TransactionEditing fragment = new TransactionEditing();
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
        // Inflate the layout for this fragment
        final View view = inflater.inflate(R.layout.transaction_editing_view, container, false);

        transactionsListView = view.findViewById(R.id.transactionEditListView);
        deleteButton = view.findViewById(R.id.transactionEditDeleteButton);
        selectAllButton = view.findViewById(R.id.transactionEditSelectAllButton);
        clearSelectedButton = view.findViewById(R.id.transactionEditClearSelectedButton);
        closeButton = view.findViewById(R.id.transactionEditCloseButton);
        selectedTextView = view.findViewById(R.id.transactionEditSelectedNumTextView);
        selectedReportTextView = view.findViewById(R.id.transactionEditSelectedReportTextView);
        totalTextview = view.findViewById(R.id.transactionEditTotalTextView);
        totalReportTextView = view.findViewById(R.id.transactionEditTotalReportTextView);

        final List<Transaction> transactionsList = MainActivity.TH.getTransactions();
        final ArrayAdapter<Transaction> entitiesAdapter = new ArrayAdapter<>(getActivity(), android.R.layout.simple_list_item_multiple_choice, transactionsList);
        System.out.println("transactionList: " + transactionsList);
        transactionsListView.setAdapter(entitiesAdapter);
        transactionsListView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);

        totalReportTextView.setText(Integer.toString(transactionsList.size()));
        selectedReportTextView.setText("0");

        transactionsListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                int n = transactionsListView.getCheckedItemCount();
                selectedReportTextView.setText(Integer.toString(n));
            }
        });

        transactionsListView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
                return false;
            }
        });

        deleteButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("delete button clicked");
//                ArrayList<Transaction> transactions = MainActivity.TH.getTransactions();
//                ArrayList<Entity> entitiesToRemove = new ArrayList<>();
//                for (Entity e : entitiesList) {
////                    int position = entitiesAdapter.getPosition(e);
////                    Entity e = entitiesAdapter.getItem(position);
//                    boolean valid = false;
//                    int position = entitiesAdapter.getPosition(e);
//                    if (transactionsListView.isItemChecked(position)) {
//                        valid = MainActivity.TH.ensureValidDelete(e);
//                        if (valid) {
//                            entitiesToRemove.add(e);
//                        }
//                        else {
//                            Toast.makeText(getContext(), "Unable to delete entity \"" + e + "\" due to\nthem being involved in a past transaction.", Toast.LENGTH_SHORT).show();
//                            transactionsListView.setItemChecked(position, false);
//                        }
//                    }
//                }
//                for (Entity e : entitiesToRemove) {
//                    System.out.println("deleting: " + e);
//                    entitiesAdapter.remove(e);
//                    MainActivity.TH.removeUser(e);
//                }
//                entitiesAdapter.notifyDataSetChanged();
//                int n = transactionsListView.getCheckedItemCount();
//                selectedReportTextView.setText(Integer.toString(n));
//                totalReportTextView.setText(Integer.toString(entitiesAdapter.getCount()));
            }
        });

        selectAllButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("select all button clicked");
                for(Transaction t : transactionsList) {
                    int position = entitiesAdapter.getPosition(t);
                    transactionsListView.setItemChecked(position, true);
                }
                entitiesAdapter.notifyDataSetChanged();
                int n = transactionsListView.getCheckedItemCount();
                selectedReportTextView.setText(Integer.toString(n));
            }
        });

        clearSelectedButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("clear selected button clicked");
                for(Transaction t : transactionsList) {
                    int position = entitiesAdapter.getPosition(t);
                    transactionsListView.setItemChecked(position, false);
                }
                entitiesAdapter.notifyDataSetChanged();
                selectedReportTextView.setText("0");
            }
        });

        closeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("close button clicked");
                getFragmentManager().popBackStack();
            }
        });
        return view;
    }
}
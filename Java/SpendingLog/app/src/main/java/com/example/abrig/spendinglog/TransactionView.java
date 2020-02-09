package com.example.abrig.spendinglog;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.widget.AdapterView;
import android.widget.AutoCompleteTextView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Map;


import static com.example.abrig.spendinglog.R.id.transactionOccurringSpinner;
import static com.example.abrig.spendinglog.R.id.transactionSenderAutoTextView;
import static com.example.abrig.spendinglog.R.id.transactionReceiverAutoTextView;

public class TransactionView extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private String name; // = MainActivity.prefs.getString("user_name", "user");
    private boolean allowedOverDraft;
    private String bankedMoneyString;
    private int bankedMoney;

    private TextView senderTextView;
    private TextView receiverTextView;
    private TextView balanceTextview;
    private TextView oneTimeTextView;
    private TextView occurringTextView;

    private Switch oneTimeSwitch;
    private EditText balanceEntryEditText;
    private AutoCompleteTextView senderAutoTextView;
    private AutoCompleteTextView receiverAutoTextView;
//    private AutoCompleteTextView occurringAutoTextView;

    private Button saveButton;
    private Button viewAllButton;
    private Button clearFormButton;
    private Spinner occurringDropDown;


    final String[] occurringList = new String[] {
            "custom",
            "hourly",
            "daily",
            "nightly",
            "weekly",
            "bi-weekly",
            "monthly",
            "bi-monthly",
            "yearly",
            "bi-yearly"
    };

    public TransactionView() {
    }

    // TODO: Rename and change types and number of parameters
    public static TransactionView newInstance(String param1, String param2) {
        TransactionView fragment = new TransactionView();
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

    public ArrayList<Entity> getEntities() {
        ArrayList<Entity> res = new ArrayList<>();
        Map<String, ?> keyVals = MainActivity.prefs.getAll();
        for (String key : keyVals.keySet()) {
            if (key.contains("entity_entry_")) {
                System.out.println("            entity key: " + key);
                Entity e = Utilities.getEntity((String) keyVals.get(key));
                res.add(e);
            }
            else {
                System.out.println("    regular key: " + key);
            }
        }
        return res;
    }

    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        final View view = inflater.inflate(R.layout.transaction_view, container, false);

        oneTimeSwitch = view.findViewById(R.id.transactionOnetimeSwitch);
        balanceEntryEditText = view.findViewById(R.id.transactionAmountEditText);
        senderAutoTextView = (AutoCompleteTextView) view.findViewById(transactionSenderAutoTextView);
        receiverAutoTextView = (AutoCompleteTextView) view.findViewById(transactionReceiverAutoTextView);
//        occurringAutoTextView = (AutoCompleteTextView) view.findViewById(transactionOccurringAutoTextView);
        occurringTextView = view.findViewById(R.id.transactionOccurringTextView);
        occurringDropDown = view.findViewById(R.id.transactionOccurringSpinner);
        saveButton = view.findViewById(R.id.transactionSaveButton);
        viewAllButton = view.findViewById(R.id.viewAllTransactionsButton);
        clearFormButton = view.findViewById(R.id.transactionClearFormButton);

        ArrayList<Entity> entities = getEntities();
        final String[] entitiesList = new String[entities.size()];
        for (int i = 0; i < entities.size(); i++) {
            String n = entities.get(i).getName();
            entitiesList[i] = n;
        }

        ArrayAdapter<String> entitiesAdapter1 = new ArrayAdapter<String>(
                getActivity(), android.R.layout.select_dialog_item, entitiesList);
        ArrayAdapter<String> entitiesAdapter2 = new ArrayAdapter<String>(
                getActivity(), android.R.layout.select_dialog_item, entitiesList);
        ArrayAdapter<String> entitiesAdapter3 = new ArrayAdapter<String>(
                getActivity(), android.R.layout.select_dialog_item, occurringList);

        senderAutoTextView.setAdapter(entitiesAdapter1);
        receiverAutoTextView.setAdapter(entitiesAdapter2);
//        occurringAutoTextView.setAdapter(entitiesAdapter3);

        senderAutoTextView.setThreshold(1);
        receiverAutoTextView.setThreshold(1);
//        occurringAutoTextView.setThreshold(1);

        // turned on by using the one time switch
//        occurringAutoTextView.setVisibility(View.INVISIBLE);
        occurringDropDown.setVisibility(View.INVISIBLE);
        occurringTextView.setVisibility(View.INVISIBLE);

        clearFormButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                oneTimeSwitch.setChecked(false);
                balanceEntryEditText.getText().clear();
                senderAutoTextView.getText().clear();
                receiverAutoTextView.getText().clear();
//                occurringAutoTextView.getText().clear();
            }
        });

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                int senderIndex = senderAutoTextView.getText().toString();
//                int receiverIndex = receiverAutoTextView.getListSelection();
                String senderEntry = senderAutoTextView.getText().toString();
                String receiverEntry = receiverAutoTextView.getText().toString();
                String occurringEntry = occurringDropDown.getSelectedItem().toString();
                boolean oneTime = oneTimeSwitch.isChecked();
                int amount = Utilities.parseMoney(balanceEntryEditText.getText().toString());
                System.out.println("entitiesList: " + Arrays.toString(entitiesList));
                System.out.println("occuringList: " + Arrays.toString(occurringList));
                System.out.println("senderEntry: " + senderEntry + ", receiverEntry: " + receiverEntry + ", oneTime: " + oneTime + ", amount: " + Utilities.dollarify(amount));
                Entity sender = MainActivity.TH.getEntityEntry(senderEntry);
                Entity receiver = MainActivity.TH.getEntityEntry(receiverEntry);
                String occurring = validateOccurringInput(occurringEntry);
                System.out.println("TransactionView Save button clicked");
                boolean transactionSuccess = MainActivity.TH.tryTransaction(
                        sender, receiver, amount, oneTime, occurring
                );
                if (transactionSuccess) {
                    Toast.makeText(getContext(), "Transaction successful!", Toast.LENGTH_LONG).show();
                    String senderKey = Utilities.getKey(sender);
                    String receiverKey = Utilities.getKey(receiver);
                    System.out.println("overwriting " + senderKey);
                    System.out.println("overwriting " + receiverKey);
                    SharedPreferencesWriter.write(senderKey, sender.serializeEntry());
                    SharedPreferencesWriter.write(receiverKey, receiver.serializeEntry());
//                    MainActivity.prefs.edit().putString(senderKey, sender.serializeEntry()).commit();
//                    MainActivity.prefs.edit().putString(receiverKey, receiver.serializeEntry()).commit();
                    if (senderKey.equals("entity_entry_User")) {
//                        MainActivity.prefs.edit().putInt("user_banked_amount", sender.getBankedMoney()).commit();
                        SharedPreferencesWriter.write("user_banked_amount", sender.getBankedMoney());
                    }
                    if (receiverKey.equals("entity_entry_User")) {
//                        MainActivity.prefs.edit().putInt("user_banked_amount", receiver.getBankedMoney()).commit();
                        SharedPreferencesWriter.write("user_banked_amount", receiver.getBankedMoney());
                    }
                }
                else {
                    Toast.makeText(getContext(), "Transaction failed.", Toast.LENGTH_LONG).show();
                }
            }
        });

        viewAllButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ArrayList<Transaction> transactions = MainActivity.TH.getTransactions();
                System.out.println("TransactionView view all button clicked");
                System.out.println("Transactions: " + transactions);
                SharedPreferencesWriter.printPrefs();

                FragmentTransaction ft = getFragmentManager().beginTransaction();
                ft.replace(R.id.container, TransactionEditing.newInstance("", ""));
                ft.addToBackStack(null);
                ft.commit();
//                String spacer = ">>";
//                String res = spacer;
//                String nowString = new Date().toString();
//                String[] spl = nowString.split(" ");
//                for (String s : spl) {
//                res += nowString + spacer + "Avery Briggs" + spacer + "NB Power" + spacer + "99999" + spacer + "false" + spacer + spacer;
//                }
//                System.out.println("String created: " + res);
//                ArrayList<Transaction> transactions = Utilities.parseTransactions(res);
//                System.out.println("parsed as: " + transactions);
            }
        });

        oneTimeSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                System.out.println("one time switch status : " + isChecked);
                if (isChecked) {
//                    occurringAutoTextView.setVisibility(View.VISIBLE);
                    occurringDropDown.setVisibility(View.VISIBLE);
                    occurringTextView.setVisibility(View.VISIBLE);
                    occurringDropDown.setVisibility(View.VISIBLE);
                }
                else {
//                    occurringAutoTextView.setVisibility(View.INVISIBLE);
                    occurringDropDown.setVisibility(View.INVISIBLE);
                    occurringTextView.setVisibility(View.INVISIBLE);
                    occurringDropDown.setVisibility(View.INVISIBLE);
                }
            }
        });

        List<String> list = Arrays.asList(occurringList);
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_item, list);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        occurringDropDown.setAdapter(dataAdapter);
        occurringDropDown.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
//                occurringAutoTextView.setText(occurringList[position]);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });


//        nameEntryEditText = view.findViewById(R.id.entityNameEditText);
//        balanceEntryEditText = view.findViewById(R.id.entityBalanceEditText);
//        overdraftSwitch = view.findViewById(R.id.entityOverdraftSwitch);
//        saveButton = view.findViewById(R.id.entitySaveButton);
//        viewAllButton = view.findViewById(R.id.viewAllEntitiesButton);
//        clearFormButton = view.findViewById(R.id.entityFormClearButton);
//
//        saveButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                System.out.println("Saving a new Entity");
//                int entityNum = MainActivity.TH.getNumEntities();
//                String name = Utilities.titlifyName(nameEntryEditText.getText().toString());
//                String balanceInput = balanceEntryEditText.getText().toString();
//                int balance = ((balanceInput.length() == 0)?
//                        Utilities.parseMoney(balanceEntryEditText.getText().toString()) : Integer.MAX_VALUE);
//                boolean overdraft = overdraftSwitch.isChecked();
//                String key = "entity_entry_";
//                if (name.length() == 0 || name.length() > 30) {
//                    name = "entity_" + entityNum;
//                    key += entityNum;
//                }
//                else {
//                    key += name;
//                }
//                Entity e = new Entity(name, balance, overdraft);
//                MainActivity.TH.addUser(e);
//                MainActivity.prefs.edit().putString(key, e.serializeEntry()).commit();
//            }
//        });
//
//        clearFormButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                nameEntryEditText.getText().clear();
//                balanceEntryEditText.getText().clear();
//                overdraftSwitch.setChecked(false);
//            }
//        });

        return view;
    }

    private String validateOccurringInput(String occurringEntry) {
        for (String s : occurringList) {
            if (s.equals(occurringEntry)) {
                return s;
            }
        }
        return "NA";
    }
}

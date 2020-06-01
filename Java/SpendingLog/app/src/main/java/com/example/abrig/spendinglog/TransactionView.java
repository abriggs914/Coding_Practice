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

import java.math.BigDecimal;
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
    private TextView transactionTypeTextView;
    private TextView occurringTextView;
    private TextView customOccurringTextView;
    private TextView customOccurringTimesTextView;
    private TextView customTransactionTypeTextView;

    private Switch oneTimeSwitch;
    private EditText balanceEntryEditText;
    private EditText customOccurringEditText;
    private EditText customTransactionTypeEditText;
    private AutoCompleteTextView senderAutoTextView;
    private AutoCompleteTextView receiverAutoTextView;
    private Spinner transactionTypeDropDown;
//    private AutoCompleteTextView occurringAutoTextView;

    private Button saveButton;
    private Button viewAllButton;
    private Button clearFormButton;
    private Spinner occurringDropDown;
    private Spinner customOccurringDropDown;

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
        occurringTextView = view.findViewById(R.id.transactionOccurringTextView);
        transactionTypeTextView = view.findViewById(R.id.transactionTypeTextView);
        transactionTypeDropDown = view.findViewById(R.id.transactionTypeSpinner);
        customTransactionTypeEditText = view.findViewById(R.id.customTransactionTypeEditText);
        customTransactionTypeTextView = view.findViewById(R.id.customTransactionTypeTextView);
        customOccurringTextView = view.findViewById(R.id.customOccurringTextView);
        customOccurringTimesTextView = view.findViewById(R.id.customOccurringTimesTextView);
        occurringDropDown = view.findViewById(R.id.transactionOccurringSpinner);
        customOccurringDropDown = view.findViewById(R.id.customOccurringSpinner);
        customOccurringEditText = view.findViewById(R.id.customOccurringEditText);
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

        clearFormButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                clearForm();
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
                String transactionTypeString = (String) transactionTypeDropDown.getSelectedItem();
                boolean oneTime = oneTimeSwitch.isChecked();
                int amount = Utilities.parseMoney(balanceEntryEditText.getText().toString());
                System.out.println("entitiesList: " + Arrays.toString(entitiesList));
                System.out.println("occuringList: " + Arrays.toString(OccurringOptions.getValues()));
                System.out.println("senderEntry: " + senderEntry + ", receiverEntry: " + receiverEntry + ", oneTime: " + oneTime + ", amount: " + Utilities.dollarify(amount));
                Entity sender = MainActivity.TH.getEntityEntry(senderEntry);
                Entity receiver = MainActivity.TH.getEntityEntry(receiverEntry);
                TransactionType transactionType = MainActivity.TH.getTransactionTypeEntry(transactionTypeString);
                String occurring = validateOccurringInput(occurringEntry);
                System.out.println("TransactionView Save button clicked");
                boolean transactionSuccess = MainActivity.TH.tryTransaction(
                        sender, receiver, amount, oneTime, occurring, transactionType
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
                    showOccurring();
                }
                else {
//                    occurringAutoTextView.setVisibility(View.INVISIBLE);
                    hideOccurring();
                    hideCustomOccurring();
                }
            }
        });

        List<String> list = Arrays.asList(OccurringOptions.getValues());
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_item, list);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        occurringDropDown.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (position == 9) {
                    showCustomOccurring();
                }
                else {
                    hideCustomOccurring();
                }
//                occurringAutoTextView.setText(occurringList[position]);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {hideCustomOccurring();}
        });

//        List<String> list = Arrays.asList(occurringList);
        ArrayAdapter<String> customOccurringAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_item, CustomOccurringOptions.getValues());
        customOccurringAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        ArrayList<TransactionType> transactionTypesList = TransactionType.getTypes();
//        if (!transactionTypesList.contains())

        final String[] transactionTypesNameList = new String[transactionTypesList.size()];
        for (int i = 0; i < transactionTypesList.size(); i++) {
            String n = transactionTypesList.get(i).getName();
            transactionTypesNameList[i] = n;
        }

        List<String> typesList = Arrays.asList(transactionTypesNameList);
        ArrayAdapter<String> transactionTypeAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_item, typesList);
        transactionTypeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        transactionTypeDropDown.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (position == 1) {
                    showCustomTransactionType();
                }
                else {
                    hideCustomTransactionType();
                }
//                occurringAutoTextView.setText(occurringList[position]);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {hideCustomTransactionType();}
        });

        // final set-up before showing
        senderAutoTextView.setAdapter(entitiesAdapter1);
        receiverAutoTextView.setAdapter(entitiesAdapter2);

        senderAutoTextView.setThreshold(1);
        receiverAutoTextView.setThreshold(1);

        occurringDropDown.setAdapter(dataAdapter);
        customOccurringDropDown.setAdapter(customOccurringAdapter);

        transactionTypeDropDown.setAdapter(transactionTypeAdapter);
//        transactionTypeDropDown.setSelection(-1);

        hideCustomTransactionType();
        hideCustomOccurring();
        hideOccurring();

        return view;
    }

    private String validateOccurringInput(String occurringEntry) {
        OccurringOptions[] values = OccurringOptions.values();
        for (int i = 0; i < values.length; i++) {
            OccurringOptions o = values[i];
            String s = o.name;
            if (s.equals(occurringEntry)) {
                if (o == OccurringOptions.CUSTOM) {
                    return validateCustomOccurring();
                }
                else {
                    return s;
                }
            }
        }
        return "NA";
    }

    public String validateCustomOccurring() {
        String res = "";
        String editTextEntry = customOccurringEditText.getText().toString();
        int customEntry = customOccurringDropDown.getSelectedItemPosition();
        String customInput = CustomOccurringOptions.getValues()[customEntry];
        boolean isNum = Utilities.checkDec(editTextEntry);
        double num = 0.0;
        if (isNum) {
            num = Double.parseDouble(editTextEntry);
            if (num == 1) {
                res += "once";
            }
            else if (num == 2) {
                res += "twice";
            }
            else {
                res += Utilities.twoDecimals(num);
            }
            res += " per " + customInput;
        }
        System.out.println("GENERATED STRING: " + res);
        return res;
    }

    public void showCustomTransactionType() {
        customTransactionTypeEditText.setVisibility(View.VISIBLE);
        customTransactionTypeTextView.setVisibility(View.VISIBLE);
    }

    public void hideCustomTransactionType() {
        customTransactionTypeEditText.setVisibility(View.INVISIBLE);
        customTransactionTypeTextView.setVisibility(View.INVISIBLE);
    }

    public void hideOccurring() {
        occurringDropDown.setVisibility(View.INVISIBLE);
        occurringTextView.setVisibility(View.INVISIBLE);
//        occurringDropDown.setVisibility(View.INVISIBLE);
    }

    public void showOccurring() {
        occurringDropDown.setVisibility(View.VISIBLE);
        occurringTextView.setVisibility(View.VISIBLE);
//        occurringDropDown.setVisibility(View.VISIBLE);
    }

    public void hideCustomOccurring() {
        customOccurringDropDown.setVisibility(View.INVISIBLE);
        customOccurringTextView.setVisibility(View.INVISIBLE);
        customOccurringTimesTextView.setVisibility(View.INVISIBLE);
        customOccurringEditText.setVisibility(View.INVISIBLE);
    }

    public void showCustomOccurring() {
        customOccurringDropDown.setVisibility(View.VISIBLE);
        customOccurringTextView.setVisibility(View.VISIBLE);
        customOccurringTimesTextView.setVisibility(View.VISIBLE);
        customOccurringEditText.setVisibility(View.VISIBLE);
    }

    public void clearForm() {
        oneTimeSwitch.setChecked(false);
        balanceEntryEditText.getText().clear();
        senderAutoTextView.getText().clear();
        receiverAutoTextView.getText().clear();
        customOccurringEditText.getText().clear();
    }
}

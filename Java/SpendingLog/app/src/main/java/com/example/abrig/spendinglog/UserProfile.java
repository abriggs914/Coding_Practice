package com.example.abrig.spendinglog;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class UserProfile extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private boolean edited;

    private String name;
    private boolean allowedOverDraft;
    private String bankedMoneyString;
    private int bankedMoney;

    private Button saveButton;
    private Button closeButton;
    private Switch overdraftSwitch;
    private EditText nameEditText;
    private EditText bankedEditText;

//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.user_profile);

//        saveButton = (Button) findViewById(R.id.saveButton);
//        overdraftSwitch = (Switch) findViewById(R.id.allowedOverDraftSwitch);
//        nameEditText = (EditText) findViewById(R.id.nameEditText);
//        bankedEditText = (EditText) findViewById(R.id.bankedEditText);
//
//        saveButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                name = nameEditText.getText().toString();
//                bankedMoneyString = bankedEditText.getText().toString();
//                bankedMoney = Utilities.parseMoney(bankedMoneyString);
//                allowedOverDraft = overdraftSwitch.isChecked();
//                if (name.length() == 0 || name.length() > 29) {
//                    name = "user";
//                }
//                MainActivity.prefs.edit().putString("user_name", name).apply();
//                MainActivity.prefs.edit().putInt("user_banked_amount", bankedMoney).apply();
//                MainActivity.prefs.edit().putBoolean("user_allowed_overdraft", allowedOverDraft).apply();
//            }
//        });
//
//        if (MainActivity.prefs.contains("user_name")) {
//            nameEditText.setText(MainActivity.prefs.getString("user_name", "user"));
//        }
//        if (MainActivity.prefs.contains("user_banked_amount")) {
//            bankedEditText.setText(MainActivity.prefs.getInt("user_banked_amount", 0));
//        }
//        if (MainActivity.prefs.contains("user_allowed_overdraft")) {
//            overdraftSwitch.setChecked(MainActivity.prefs.getBoolean("user_allowed_overdraft", true));
//        }
//    }

    public UserProfile() {
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
    public static UserProfile newInstance(String param1, String param2) {
        UserProfile fragment = new UserProfile();
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

        edited = false;
        final View view = inflater.inflate(R.layout.user_profile, container, false);
        Toast.makeText(getContext(), "Editing profile information...", Toast.LENGTH_SHORT).show();

        saveButton = (Button) view.findViewById(R.id.saveButton);
        closeButton = (Button) view.findViewById(R.id.closeButton);
        overdraftSwitch = (Switch) view.findViewById(R.id.allowedOverDraftSwitch);
        nameEditText = (EditText) view.findViewById(R.id.nameEditText);
        bankedEditText = (EditText) view.findViewById(R.id.bankedEditText);

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.print("Save button clicked!");
                name = Utilities.titlifyName(nameEditText.getText().toString()).trim();
                nameEditText.setText(name);
                bankedMoneyString = bankedEditText.getText().toString();
                bankedMoney = Utilities.parseMoney(bankedMoneyString);
                allowedOverDraft = overdraftSwitch.isChecked();
                if (name.length() == 0 || name.length() > 29) {
                    name = "User";
                }

                String oldName = MainActivity.prefs.getString("user_name", "User");
                // these are left as a commit instead of apply because they are
                // essentially the three most important pieces of information in the app.
                MainActivity.prefs.edit().putString("user_name", name).commit();
                MainActivity.prefs.edit().putInt("user_banked_amount", bankedMoney).commit();
                MainActivity.prefs.edit().putBoolean("user_allowed_overdraft", allowedOverDraft).commit();

                Entity e;
                if (MainActivity.prefs.contains("entity_entry_User")) {
                    System.out.println("FOUND");
                    String entityString = (String) MainActivity.prefs.getAll().get("entity_entry_User");
                    // don't think this should be here
                    ArrayList<Transaction> transactions = Utilities.parseTransactions(entityString);
                    MainActivity.TH.addTransactions(transactions);
                    Entity t = Utilities.parseEntity(entityString);
                    e = Entity.re_initEntity(name, bankedMoney, t.getSentMoney(), t.getReceivedMoney(), allowedOverDraft);
                }
                else {
                    // create user entity for the first time
                    System.out.println("NOT FOUND");
                    e = new Entity(name, bankedMoney);
                }
                e.setName(name);
                e.setBankedMoney(bankedMoney);
                e.setAllowedOverdraft(allowedOverDraft);
                MainActivity.prefs.edit().putString("entity_entry_User", e.serializeEntry()).commit();
                MainActivity.TH.removeUser(oldName);
                MainActivity.TH.addUser(e);
                edited = false;
            }
        });

        closeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Close button clicked!");
                determineChanges();
//                System.out.println("fragment manager BEFORE: " + getFragmentManager().getFragments());
//                for (Fragment f : getFragmentManager().getFragments()) {
//                    System.out.println("fragment: " + f);
//                }
                if (edited) {
                    Toast.makeText(getContext(), "Would you like to save your changes?", Toast.LENGTH_LONG).show();
                    edited = false;
                }
                else {
                    getFragmentManager().popBackStack();
                }
//                addToBackStack().commit();
//                System.out.println("-- fragment manager AFTER: " + getFragmentManager().getFragments());
//                for (Fragment f : getFragmentManager().getFragments()) {
//                    System.out.println("fragment: " + f);
//                }
            }
        });

//        System.out.print("KEY SET: " + MainActivity.prefs.getAll().keySet());
        if (MainActivity.prefs.getAll().keySet().contains("entity_entry_User")) {
            String entityString = MainActivity.prefs.getString("entity_entry_User", "user");
            Entity e = Utilities.getEntity(entityString);

            nameEditText.setText(e.getName());
            bankedEditText.setText(Utilities.dollarify(e.getBankedMoney()));
            overdraftSwitch.setChecked(e.isAllowedOverdraft());
        }

//            double t = MainActivity.prefs.getInt("user_banked_amount", 0) / 100.0;
//            int t =
//            NumberFormat nf = NumberFormat.getInstance();
//            nf.setMaximumFractionDigits(2);
//            nf.setMinimumFractionDigits(2);
//            String s = nf.format(t);
//        if (MainActivity.prefs.getAll().keySet().contains("user_banked_amount")) {
//        }
//        if (MainActivity.prefs.getAll().keySet().contains("user_allowed_overdraft")) {
//        }

        return view;
    }

    public void determineChanges() {
        Map<String, ?> keysValues = MainActivity.prefs.getAll();
        String name = nameEditText.getText().toString();
        int balance = Utilities.parseMoney(bankedEditText.getText().toString());
        boolean overdraft = overdraftSwitch.isChecked();
        for (String s : keysValues.keySet()) {
            Class clazz = keysValues.get(s).getClass();
            System.out.println("Key: " + s + ", clazz: " + clazz + ", value: " + keysValues.get(s));
            if (clazz.equals(String.class)) {
                String value = (String) keysValues.get(s);
                if (s.equals("user_name")) {
                    if (!value.equals(name)) {
                        System.out.println("Name is different (og, new):  \"" + value + "\" vs. \"" + name + "\"");
                        edited = true;
                    }
                }
            }
            else if (clazz.equals(Integer.class)) {
                int value = (Integer) keysValues.get(s);
                if (s.equals("user_banked_amount")) {
//                    value *= 100;
                    if (value != balance) {
                        System.out.println("Balance is different (og, new):  \"" + value + "\" vs. \"" + balance + "\"");
                        edited = true;
                    }
                }
            }
            else if (clazz.equals(Boolean.class)) {
                boolean value = (Boolean) keysValues.get(s);
                if (s.equals("user_allowed_overdraft")) {
                    if (value != overdraft) {
                        System.out.println("Overdraft is different (og, new):  \"" + value + "\" vs. \"" + overdraft + "\"");
                        edited = true;
                    }
                }
            }
//            else if (clazz.equals(Float.class)) {
//
//            }
//            else if (clazz.equals(Character.class)) {
//
//            }
//            else if (clazz.equals(Integer.class)) {
//
//            }
//            else if (clazz.equals(Date.class)) {
//
//            }
//            else if (clazz.equals(Double.class)) {
//
//            }
//            System.out.print("String entry: " + s);
        }
        if (!keysValues.containsKey("user_name") || !keysValues.containsKey("user_allowed_overdraft") || !keysValues.containsKey("user_banked_amount")) {
            edited = true;
        }
    }
}

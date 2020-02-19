package com.example.abrig.spendinglog;

import android.graphics.Color;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.style.ForegroundColorSpan;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.text.NumberFormat;
import java.util.Map;
import java.util.Set;


public class UserView extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private String name = MainActivity.prefs.getString("user_name", "user");
    private boolean allowedOverDraft;
    private String bankedMoneyString;
    private int bankedMoney;

    private FloatingActionButton fab;

    private TextView nameTextView;
    private TextView nameReportTextView;
    private TextView balanceTextview;
    private TextView balanceReportTextView;
    private TextView overdraftTextView;
    private TextView overdraftReportTextView;

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

    public UserView() {
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
    public static UserView newInstance(String param1, String param2) {
        UserView fragment = new UserView();
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
        final View view = inflater.inflate(R.layout.user_view, container, false);

        nameReportTextView = view.findViewById(R.id.nameReportTextView);
        balanceReportTextView = view.findViewById(R.id.bankBalanceReportTextView);
        overdraftReportTextView = view.findViewById(R.id.overdraftReportTextView);
        fab = view.findViewById(R.id.floatingActionButton);

        Set<String> keys = MainActivity.prefs.getAll().keySet();
        if (keys.contains("entity_entry_User")) {
            Entity e = Utilities.parseEntity((String)MainActivity.prefs.getAll().get("entity_entry_User"));
            String userName = e.getName();
            Spannable userBalance = Utilities.dollarify(e.getBankedMoney());
            String userAllowedOverdraft = genOverdraftMessage(e.isAllowedOverdraft());
            nameReportTextView.setText(userName);
            int money = e.getBankedMoney();
            Spannable bankedMoney = Utilities.dollarify(money);
//            if (money < 0) {
//                Spannable wordToSpan = new SpannableString(bankedMoney);
//                wordToSpan.setSpan(new ForegroundColorSpan(Color.RED), 0, wordToSpan.length(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
//                balanceReportTextView.setText(wordToSpan);
//            }
//            else {
                balanceReportTextView.setText(bankedMoney);
//            }
            overdraftReportTextView.setText(userAllowedOverdraft);
        }
//        if (keys.contains("user_name")) {
//            nameReportTextView.setText(MainActivity.prefs.getString("user_name", "user"));
//        }
//        if (keys.contains("user_banked_amount")) {
//            double t = MainActivity.prefs.getInt("user_banked_amount", 0) / 100.0;
//            NumberFormat nf = NumberFormat.getInstance();
//            nf.setMaximumFractionDigits(2);
//            nf.setMinimumFractionDigits(2);
//            String s = "$ " + nf.format(t);
//            balanceReportTextView.setText(s);
//        }
//        if (keys.contains("user_allowed_overdraft")) {
//            boolean allowed = MainActivity.prefs.getBoolean("user_allowed_overdraft", true);
//            overdraftReportTextView.setText(message);
//        }

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                MainActivity.getUserDataAtLaunch();
                FragmentTransaction ft = getFragmentManager().beginTransaction();
                ft.replace(R.id.container, UserProfile.newInstance("", ""));
                ft.addToBackStack(null);
                ft.commit();
//                MainActivity.openFragment(UserProfile.newInstance("", ""));
            }
        });
        fab.show();

//        fab.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                Toast.makeText(getContext(), "Editing profile information...", Toast.LENGTH_SHORT).show();
//                Bundle bundle = new Bundle();
//                getFragmentManager().putFragment(bundle, "editProfile", UserProfile.newInstance("", ""));
////                MainActivity.openFragment(UserProfile.newInstance("", ""));
//            }
//        });

//        saveButton = (Button) view.findViewById(R.id.saveButton);
//        closeButton = (Button) view.findViewById(R.id.closeButton);
//        overdraftSwitch = (Switch) view.findViewById(R.id.allowedOverDraftSwitch);
//        nameEditText = (EditText) view.findViewById(R.id.nameEditText);
//        bankedEditText = (EditText) view.findViewById(R.id.bankedEditText);
//
//        saveButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                System.out.print("Save button clicked!");
//                name = Utilities.titlifyName(nameEditText.getText().toString());
//                nameEditText.setText(name);
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
//        closeButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                System.out.print("Close button clicked!");
//                getFragmentManager().popBackStack();
////                addToBackStack().commit();
//            }
//        });
//
////        System.out.print("KEY SET: " + MainActivity.prefs.getAll().keySet());
////        for (String s : MainActivity.prefs.getAll().keySet()) {
////            System.out.print("String entry: " + s);
////        }
//        if (MainActivity.prefs.getAll().keySet().contains("user_name")) {
//            nameEditText.setText(MainActivity.prefs.getString("user_name", "user"));
//        }
//        if (MainActivity.prefs.getAll().keySet().contains("user_banked_amount")) {
//            double t = MainActivity.prefs.getInt("user_banked_amount", 0) / 100.0;
//            NumberFormat nf = NumberFormat.getInstance();
//            nf.setMaximumFractionDigits(2);
//            nf.setMinimumFractionDigits(2);
//            String s = nf.format(t);
//            bankedEditText.setText(s);
//        }
//        if (MainActivity.prefs.getAll().keySet().contains("user_allowed_overdraft")) {
//            overdraftSwitch.setChecked(MainActivity.prefs.getBoolean("user_allowed_overdraft", true));
//        }

        return view;
    }

    public String genOverdraftMessage(boolean allowed) {
        String message = "Allowed";
        if (!allowed) {
            message = "Not " + message.substring(0, 1). toLowerCase() + message.substring(1);
        }
        return message;
    }
}

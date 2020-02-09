package com.example.abrig.spendinglog;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.example.abrig.spendinglog.MainActivity;
import com.example.abrig.spendinglog.R;

import java.text.NumberFormat;
import java.util.Set;

public class EntityView  extends Fragment {

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

    private TextView nameTextView;
    private EditText nameEntryEditText;
    private TextView balanceTextview;
    private EditText balanceEntryEditText;
    private TextView overdraftTextView;
    private Switch overdraftSwitch;
    private Button saveButton;
    private Button viewAllButton;
    private Button clearFormButton;

    public EntityView() {
    }

    // TODO: Rename and change types and number of parameters
    public static EntityView newInstance(String param1, String param2) {
        EntityView fragment = new EntityView();
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
        final View view = inflater.inflate(R.layout.entity_creation_view, container, false);

        nameEntryEditText = view.findViewById(R.id.entityNameEditText);
        balanceEntryEditText = view.findViewById(R.id.entityBalanceEditText);
        overdraftSwitch = view.findViewById(R.id.entityOverdraftSwitch);
        saveButton = view.findViewById(R.id.entitySaveButton);
        viewAllButton = view.findViewById(R.id.viewAllEntitiesButton);
        clearFormButton = view.findViewById(R.id.entityFormClearButton);

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Saving a new Entity");
                String entityNum = String.format("|%05d|", MainActivity.TH.getNumEntities() + 1);
                String name = Utilities.titlifyName(nameEntryEditText.getText().toString().trim());
                String balanceInput = balanceEntryEditText.getText().toString().trim();
                int balance = ((balanceInput.length() == 0)?
                        Utilities.parseMoney(balanceEntryEditText.getText().toString().trim()) : Integer.MAX_VALUE);
                boolean overdraft = overdraftSwitch.isChecked();
                String key = "entity_entry_";
                if (name.length() == 0 || name.length() > 30) {
                    name = "entity|" + entityNum + "|";
                    key +=  "entity|" + entityNum + "|";
                }
                else {
                    key += name;
                }
                String idString = TransactionHandler.genEntityID(name);
                Entity e = new Entity(name, idString, balance, overdraft);
//                MainActivity.TH.addUser(e);
                SharedPreferencesWriter.write(key, e.serializeEntry());
                MainActivity.TH.addEntity(e);
                nameEntryEditText.setText(name);
                Toast.makeText(getContext(), "Entity \"" + name + "\" created successfully!", Toast.LENGTH_SHORT).show();
            }
        });

        clearFormButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nameEntryEditText.getText().clear();
                balanceEntryEditText.getText().clear();
                overdraftSwitch.setChecked(false);
            }
        });

        viewAllButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("View all entities button clicked");
                System.out.println("entitiesList: " + MainActivity.TH.getEntities());
                SharedPreferencesWriter.printPrefs();

                FragmentTransaction ft = getFragmentManager().beginTransaction();
                ft.replace(R.id.container, EntityEditing.newInstance("", ""));
                ft.addToBackStack(null);
                ft.commit();
            }
        });

        return view;
    }
}


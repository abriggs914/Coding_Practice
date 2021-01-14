package com.example.cluenotebook.ui.main;

import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.cluenotebook.PersonE;
import com.example.cluenotebook.R;
import com.example.cluenotebook.WeaponE;

import java.util.HashMap;

/**
 * A placeholder fragment containing a simple view.
 */
public class PlaceholderFragment extends Fragment {

    private static final String ARG_SECTION_NUMBER = "section_number";
    private static ClueGame clueGame;

    private PageViewModel pageViewModel;

    public static PlaceholderFragment newInstance(int index) {
        PlaceholderFragment fragment = new PlaceholderFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        pageViewModel = new ViewModelProvider(this).get(PageViewModel.class);
        int index = 1;
        if (getArguments() != null) {
            index = getArguments().getInt(ARG_SECTION_NUMBER);
        }
        pageViewModel.setIndex(index);

        clueGame = new ClueGame();
    }

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_main, container, false);
        final TextView textView = root.findViewById(R.id.section_label);

        ////////////////////////////////////////////////  Design vars  ////////////////////////////////////////////////////

        //          People buttons
        ImageButton notebookPicturePeople_white = root.findViewById(R.id.notebook_picture_people_white);
        ImageButton notebookPicturePeople_green = root.findViewById(R.id.notebook_picture_people_green);
        ImageButton notebookPicturePeople_blue = root.findViewById(R.id.notebook_picture_people_blue);
        ImageButton notebookPicturePeople_purple = root.findViewById(R.id.notebook_picture_people_purple);
        ImageButton notebookPicturePeople_red = root.findViewById(R.id.notebook_picture_people_red);
        ImageButton notebookPicturePeople_yellow = root.findViewById(R.id.notebook_picture_people_yellow);

        HashMap<ImageButton, PersonE> peopleButtons = new HashMap<>();
        peopleButtons.put(notebookPicturePeople_white, PersonE.WHITE);
        peopleButtons.put(notebookPicturePeople_green, PersonE.GREEN);
        peopleButtons.put(notebookPicturePeople_blue, PersonE.PEACOCK);
        peopleButtons.put(notebookPicturePeople_purple, PersonE.PLUM);
        peopleButtons.put(notebookPicturePeople_red, PersonE.SCARLETT);
        peopleButtons.put(notebookPicturePeople_yellow, PersonE.MUSTARD);

        initLongClickListeners_people(peopleButtons);

        //          Weapon buttons
        ImageButton notebookPictureWeapon_axe = root.findViewById(R.id.notebook_pictures_weapons_axe);
        ImageButton notebookPictureWeapon_bat = root.findViewById(R.id.notebook_pictures_weapons_bat);
        ImageButton notebookPictureWeapon_candlestick = root.findViewById(R.id.notebook_pictures_weapons_candlestick);
        ImageButton notebookPictureWeapon_dumbbell = root.findViewById(R.id.notebook_pictures_weapons_dumbbell);
        ImageButton notebookPictureWeapon_knife = root.findViewById(R.id.notebook_pictures_weapons_knife);
        ImageButton notebookPictureWeapon_pistol = root.findViewById(R.id.notebook_pictures_weapons_pistol);
        ImageButton notebookPictureWeapon_poison = root.findViewById(R.id.notebook_pictures_weapons_poison);
        ImageButton notebookPictureWeapon_rope = root.findViewById(R.id.notebook_pictures_weapons_rope);
        ImageButton notebookPictureWeapon_trophy = root.findViewById(R.id.notebook_pictures_weapons_trophy);

        HashMap<ImageButton, WeaponE> weaponButtons = new HashMap<>();
        weaponButtons.put(notebookPictureWeapon_axe, WeaponE.AXE);
        weaponButtons.put(notebookPictureWeapon_bat, WeaponE.BAT);
        weaponButtons.put(notebookPictureWeapon_candlestick, WeaponE.CANDLESTICK);
        weaponButtons.put(notebookPictureWeapon_dumbbell, WeaponE.DUMBBELL);
        weaponButtons.put(notebookPictureWeapon_knife, WeaponE.KNIFE);
        weaponButtons.put(notebookPictureWeapon_pistol, WeaponE.PISTOL);
        weaponButtons.put(notebookPictureWeapon_poison, WeaponE.POISON);
        weaponButtons.put(notebookPictureWeapon_rope, WeaponE.ROPE);
        weaponButtons.put(notebookPictureWeapon_trophy, WeaponE.TROPHY);

        initLongClickListeners_weapons(weaponButtons);
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        pageViewModel.getText().observe(this, new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }

    public void initLongClickListeners_people(HashMap<ImageButton, PersonE> peopleButtons) {
        for (ImageButton person : peopleButtons.keySet()) {
            String colour = peopleButtons.get(person).colour;
            person.setOnLongClickListener(new View.OnLongClickListener() {
                @RequiresApi(api = Build.VERSION_CODES.N)
                @Override
                public boolean onLongClick(View v) {
                    System.out.println("Long press on " + colour + " token");
                    clueGame.seeCards(clueGame.getPersonByColour(colour));
                    System.out.println(clueGame.getClueNoteBook());
                    return false;
                }
            });
        }
    }

    public void initLongClickListeners_weapons(HashMap<ImageButton, WeaponE> peopleButtons) {
        for (ImageButton weapon : peopleButtons.keySet()) {
            String name = peopleButtons.get(weapon).name;
            weapon.setOnLongClickListener(new View.OnLongClickListener() {
                @RequiresApi(api = Build.VERSION_CODES.N)
                @Override
                public boolean onLongClick(View v) {
                    System.out.println("Long press on " + name + " token");
                    clueGame.seeCards(clueGame.getWeaponByName(name));
                    System.out.println(clueGame.getClueNoteBook());
                    return false;
                }
            });
        }
    }
}
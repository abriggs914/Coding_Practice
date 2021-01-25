package com.example.cluenotebook.ui.main;

import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.cluenotebook.ClueGame;
import com.example.cluenotebook.Person;
import com.example.cluenotebook.PersonE;
import com.example.cluenotebook.R;
import com.example.cluenotebook.Room;
import com.example.cluenotebook.RoomE;
import com.example.cluenotebook.Weapon;
import com.example.cluenotebook.WeaponE;

import java.util.HashMap;

/**
 * A placeholder fragment containing a simple view.
 */
public class PlaceholderFragment extends Fragment {

    private static View root;
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

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        root = inflater.inflate(R.layout.fragment_main, container, false);
        final TextView textView = root.findViewById(R.id.section_label);

        ////////////////////////////////////////////////  Design vars  ////////////////////////////////////////////////////

        // x's
        ImageView notebookPictureRed_x_white = root.findViewById(R.id.red_x_white);
        ImageView notebookPictureRed_x_red = root.findViewById(R.id.red_x_red);
        ImageView notebookPictureRed_x_blue = root.findViewById(R.id.red_x_blue);
        ImageView notebookPictureRed_x_green = root.findViewById(R.id.red_x_green);
        ImageView notebookPictureRed_x_yellow = root.findViewById(R.id.red_x_yellow);
        ImageView notebookPictureRed_x_purple = root.findViewById(R.id.red_x_purple);

        ImageView notebookPictureRed_x_axe = root.findViewById(R.id.red_x_axe);
        ImageView notebookPictureRed_x_bat = root.findViewById(R.id.red_x_bat);
        ImageView notebookPictureRed_x_candlestick = root.findViewById(R.id.red_x_candlestick);
        ImageView notebookPictureRed_x_dumbbell = root.findViewById(R.id.red_x_dumbbell);
        ImageView notebookPictureRed_x_knife = root.findViewById(R.id.red_x_knife);
        ImageView notebookPictureRed_x_pistol = root.findViewById(R.id.red_x_pistol);
        ImageView notebookPictureRed_x_poison = root.findViewById(R.id.red_x_poison);
        ImageView notebookPictureRed_x_rope = root.findViewById(R.id.red_x_rope);
        ImageView notebookPictureRed_x_trophy = root.findViewById(R.id.red_x_trophy);

        ImageView notebookPictureRed_x_spa = root.findViewById(R.id.red_x_spa);
        ImageView notebookPictureRed_x_theater = root.findViewById(R.id.red_x_theater);
        ImageView notebookPictureRed_x_living_room = root.findViewById(R.id.red_x_living_room);
        ImageView notebookPictureRed_x_observatory = root.findViewById(R.id.red_x_observatory);
        ImageView notebookPictureRed_x_patio = root.findViewById(R.id.red_x_patio);
        ImageView notebookPictureRed_x_hall = root.findViewById(R.id.red_x_hall);
        ImageView notebookPictureRed_x_guest_house = root.findViewById(R.id.red_x_guest_house);
        ImageView notebookPictureRed_x_kitchen = root.findViewById(R.id.red_x_kitchen);
        ImageView notebookPictureRed_x_dining_room = root.findViewById(R.id.red_x_dining_room);


        //          People buttons
        ImageButton notebookPicturePeople_white = root.findViewById(R.id.notebook_picture_people_white);
        ImageButton notebookPicturePeople_green = root.findViewById(R.id.notebook_picture_people_green);
        ImageButton notebookPicturePeople_blue = root.findViewById(R.id.notebook_picture_people_blue);
        ImageButton notebookPicturePeople_purple = root.findViewById(R.id.notebook_picture_people_purple);
        ImageButton notebookPicturePeople_red = root.findViewById(R.id.notebook_picture_people_red);
        ImageButton notebookPicturePeople_yellow = root.findViewById(R.id.notebook_picture_people_yellow);

        HashMap<ImageButton, HashMap<ImageView, PersonE>> peopleButtons = new HashMap<>();
        HashMap<ImageView, PersonE> whiteMap = new HashMap<>();
        whiteMap.put(notebookPictureRed_x_white, PersonE.WHITE);
        HashMap<ImageView, PersonE> greenMap = new HashMap<>();
        greenMap.put(notebookPictureRed_x_green, PersonE.GREEN);
        HashMap<ImageView, PersonE> blueMap = new HashMap<>();
        blueMap.put(notebookPictureRed_x_blue, PersonE.PEACOCK);
        HashMap<ImageView, PersonE> purpleMap = new HashMap<>();
        purpleMap.put(notebookPictureRed_x_purple, PersonE.PLUM);
        HashMap<ImageView, PersonE> redMap = new HashMap<>();
        redMap.put(notebookPictureRed_x_red, PersonE.SCARLETT);
        HashMap<ImageView, PersonE> yellowMap = new HashMap<>();
        yellowMap.put(notebookPictureRed_x_yellow, PersonE.MUSTARD);

        peopleButtons.put(notebookPicturePeople_white, whiteMap);
        peopleButtons.put(notebookPicturePeople_green, greenMap);
        peopleButtons.put(notebookPicturePeople_blue, blueMap);
        peopleButtons.put(notebookPicturePeople_purple, purpleMap);
        peopleButtons.put(notebookPicturePeople_red, redMap);
        peopleButtons.put(notebookPicturePeople_yellow, yellowMap);

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

        HashMap<ImageButton, HashMap<ImageView, WeaponE>> weaponButtons = new HashMap<>();
        HashMap<ImageView, WeaponE> axeMap = new HashMap<>();
        axeMap.put(notebookPictureRed_x_axe, WeaponE.AXE);
        HashMap<ImageView, WeaponE> batMap = new HashMap<>();
        batMap.put(notebookPictureRed_x_bat, WeaponE.BAT);
        HashMap<ImageView, WeaponE> candlestickMap = new HashMap<>();
        candlestickMap.put(notebookPictureRed_x_candlestick, WeaponE.CANDLESTICK);
        HashMap<ImageView, WeaponE> dumbbellMap = new HashMap<>();
        dumbbellMap.put(notebookPictureRed_x_dumbbell, WeaponE.DUMBBELL);
        HashMap<ImageView, WeaponE> knifeMap = new HashMap<>();
        knifeMap.put(notebookPictureRed_x_knife, WeaponE.KNIFE);
        HashMap<ImageView, WeaponE> pistolMap = new HashMap<>();
        pistolMap.put(notebookPictureRed_x_pistol, WeaponE.PISTOL);
        HashMap<ImageView, WeaponE> poisonMap = new HashMap<>();
        poisonMap.put(notebookPictureRed_x_poison, WeaponE.POISON);
        HashMap<ImageView, WeaponE> ropeMap = new HashMap<>();
        ropeMap.put(notebookPictureRed_x_rope, WeaponE.ROPE);
        HashMap<ImageView, WeaponE> trophyMap = new HashMap<>();
        trophyMap.put(notebookPictureRed_x_trophy, WeaponE.TROPHY);

        weaponButtons.put(notebookPictureWeapon_axe, axeMap);
        weaponButtons.put(notebookPictureWeapon_bat, batMap);
        weaponButtons.put(notebookPictureWeapon_candlestick, candlestickMap);
        weaponButtons.put(notebookPictureWeapon_dumbbell, dumbbellMap);
        weaponButtons.put(notebookPictureWeapon_knife, knifeMap);
        weaponButtons.put(notebookPictureWeapon_pistol, pistolMap);
        weaponButtons.put(notebookPictureWeapon_poison, poisonMap);
        weaponButtons.put(notebookPictureWeapon_rope, ropeMap);
        weaponButtons.put(notebookPictureWeapon_trophy, trophyMap);

        initLongClickListeners_weapons(weaponButtons);

        // room buttons
        ImageButton notebookPicture_spa = root.findViewById(R.id.notebook_picture_room_spa);
        ImageButton notebookPicture_theater = root.findViewById(R.id.notebook_picture_room_theater);
        ImageButton notebookPicture_living_room = root.findViewById(R.id.notebook_picture_room_living_room);
        ImageButton notebookPicture_observatory = root.findViewById(R.id.notebook_picture_room_observatory);
        ImageButton notebookPicture_patio = root.findViewById(R.id.notebook_picture_room_patio);
        ImageButton notebookPicture_hall = root.findViewById(R.id.notebook_picture_room_hall);
        ImageButton notebookPicture_guest_house = root.findViewById(R.id.notebook_picture_room_guest_house);
        ImageButton notebookPicture_kitchen = root.findViewById(R.id.notebook_picture_room_kitchen);
        ImageButton notebookPicture_dining_room = root.findViewById(R.id.notebook_picture_room_dining_room);

        HashMap<ImageButton, HashMap<ImageView, RoomE>> roomButtons = new HashMap<>();
        HashMap<ImageView, RoomE> spaMap = new HashMap<>();
        spaMap.put(notebookPictureRed_x_spa, RoomE.SPA);
        HashMap<ImageView, RoomE> theaterMap = new HashMap<>();
        theaterMap.put(notebookPictureRed_x_theater, RoomE.THEATER);
        HashMap<ImageView, RoomE> livingRoomMap = new HashMap<>();
        livingRoomMap.put(notebookPictureRed_x_living_room, RoomE.LIVING_ROOM);
        HashMap<ImageView, RoomE> observatoryMap = new HashMap<>();
        observatoryMap.put(notebookPictureRed_x_observatory, RoomE.OBSERVATORY);
        HashMap<ImageView, RoomE> patioMap = new HashMap<>();
        patioMap.put(notebookPictureRed_x_patio, RoomE.PATIO);
        HashMap<ImageView, RoomE> hallMap = new HashMap<>();
        hallMap.put(notebookPictureRed_x_hall, RoomE.HALL);
        HashMap<ImageView, RoomE> guestHouseMap = new HashMap<>();
        guestHouseMap.put(notebookPictureRed_x_guest_house, RoomE.GUEST_HOUSE);
        HashMap<ImageView, RoomE> kitchenMap = new HashMap<>();
        kitchenMap.put(notebookPictureRed_x_kitchen, RoomE.KITCHEN);
        HashMap<ImageView, RoomE> diningRoomMap = new HashMap<>();
        diningRoomMap.put(notebookPictureRed_x_dining_room, RoomE.DINING_ROOM);

        roomButtons.put(notebookPicture_spa, spaMap);
        roomButtons.put(notebookPicture_theater, theaterMap);
        roomButtons.put(notebookPicture_living_room, livingRoomMap);
        roomButtons.put(notebookPicture_observatory, observatoryMap);
        roomButtons.put(notebookPicture_patio, patioMap);
        roomButtons.put(notebookPicture_hall, hallMap);
        roomButtons.put(notebookPicture_guest_house, guestHouseMap);
        roomButtons.put(notebookPicture_kitchen, kitchenMap);
        roomButtons.put(notebookPicture_dining_room, diningRoomMap);

        initLongClickListeners_rooms(roomButtons);

        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        pageViewModel.getText().observe(this, new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        return root;
    }

    private void markClueElement(View view, ImageButton imageButton, ImageView x) {
        System.out.println("View: " + root);
        if (x.getVisibility() == View.VISIBLE) {
            x.setVisibility(View.INVISIBLE);
        }
        else {
            x.setVisibility(View.VISIBLE);
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void initLongClickListeners_people(HashMap<ImageButton, HashMap<ImageView, PersonE>> peopleButtons) {
        for (ImageButton person : peopleButtons.keySet()) {
            for (ImageView x : peopleButtons.get(person).keySet()) {
                String colour = peopleButtons.get(person).get(x).colour;
                Person p = (Person) ClueGame.getPersonByColour(colour);
                person.setOnLongClickListener(new View.OnLongClickListener() {
                    @Override
                    public boolean onLongClick(View v) {
                        System.out.println("Long press on " + colour + " token");
                        if (clueGame.stillInPlay(p)) {
                            clueGame.seeCards(p);
                        }
                        else {
                            clueGame.addCardBack(p);
                        }
                        markClueElement(v, person, x);
                        System.out.println(clueGame);
                        return false;
                    }
                });
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void initLongClickListeners_weapons(HashMap<ImageButton, HashMap<ImageView, WeaponE>> weaponButtons) {
        for (ImageButton weapon : weaponButtons.keySet()) {
            for (ImageView x : weaponButtons.get(weapon).keySet()) {
                String name = weaponButtons.get(weapon).get(x).name;
                Weapon w = (Weapon) ClueGame.getWeaponByName(name);
                weapon.setOnLongClickListener(new View.OnLongClickListener() {
                    @Override
                    public boolean onLongClick(View v) {
                        System.out.println("Long press on " + name + " token");
                        if (clueGame.stillInPlay(w)) {
                            clueGame.seeCards(w);
                        }
                        else {
                            clueGame.addCardBack(w);
                        }
                        markClueElement(v, weapon, x);
                        System.out.println(clueGame);
                        return false;
                    }
                });
            }
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void initLongClickListeners_rooms(HashMap<ImageButton, HashMap<ImageView, RoomE>> roomButtons) {
        for (ImageButton room : roomButtons.keySet()) {
            for (ImageView x : roomButtons.get(room).keySet()) {
                String name = roomButtons.get(room).get(x).name;
                Room r = (Room) ClueGame.getRoomByName(name);
                room.setOnLongClickListener(new View.OnLongClickListener() {
                    @Override
                    public boolean onLongClick(View v) {
                        System.out.println("Long press on " + name + " token\nroom: " + r);
                        if (clueGame.stillInPlay(r)) {
                            clueGame.seeCards(r);
                        }
                        else {
                            clueGame.addCardBack(r);
                        }
                        markClueElement(v, room, x);
                        System.out.println(clueGame);
                        return false;
                    }
                });
            }
        }
    }
}
package com.example.cluenotebook;

import android.content.Context;
import android.os.Build;
import android.view.View;
import android.widget.ImageButton;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import com.example.cluenotebook.ClueElement;
import com.example.cluenotebook.ClueNoteBook;
import com.example.cluenotebook.MainActivity;
import com.example.cluenotebook.Person;
import com.example.cluenotebook.R;
import com.example.cluenotebook.Room;
import com.example.cluenotebook.Weapon;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import static android.text.TextUtils.join;

@RequiresApi(api = Build.VERSION_CODES.N)
public class ClueGame {

    public static ArrayList<String> peopleStr = new ArrayList<String>(Arrays.asList("Mustard", "Plum", "Scarlett", "Peacock", "White", "Green"));
    public static ArrayList<String> weaponStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
    public static ArrayList<String> roomStr = new ArrayList<String>(Arrays.asList("Spa", "Theater", "Living Room", "Observatory", "Patio", "Hall", "Guest House", "Kitchen", "Dining Room"));
    public static ClueElement[] ORIG_people = peopleStr.stream().map(Person::NewPerson).toArray(Person[]::new);
    public static ClueElement[] ORIG_weapons = weaponStr.stream().map(Weapon::NewWeapon).toArray(Weapon[]::new);
    public static ClueElement[] ORIG_rooms = roomStr.stream().map(Room::NewRoom).toArray(Room[]::new);

    private int turnNumber;
    private ClueNoteBook clueNoteBook;
    private ArrayList<ClueStatusPoint> statusPoints;

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

     public ClueGame() {
         init();
     }

     public void init() {
         this.clueNoteBook = new ClueNoteBook(ORIG_people, ORIG_weapons, ORIG_rooms);
         this.statusPoints = new ArrayList<>();
         this.turnNumber = 0;
     }

    public void createClueStatusPoint() {
         ArrayList<ClueElement> people = clueNoteBook.getPeople();
         ArrayList<ClueElement> weapons = clueNoteBook.getWeapons();
         ArrayList<ClueElement> rooms = clueNoteBook.getRooms();
        // TODO need to add hints/suspected card owners to the constructor call. just use the object. at most it will be a list of length = nPlayers * 5-6 turns
         ClueStatusPoint statusPoint = new ClueStatusPoint(turnNumber, people, weapons, rooms);
         this.statusPoints.add(statusPoint);
    }

    public void incrementTurnNumber() {
         this.turnNumber++;
    }

    public void seeCards(ClueElement... clues) {
         this.clueNoteBook.seeCards(clues);
    }

    public void addCardBack(ClueElement... clues) {
        this.clueNoteBook.addCardBack(clues);
    }

    public boolean stillInPlay(ClueElement... clues) {
         for (ClueElement clue : clues) {
             boolean person = clueNoteBook.getPeople().contains(clue);
             boolean weapon = clueNoteBook.getWeapons().contains(clue);
             boolean room = clueNoteBook.getRooms().contains(clue);
             if (!(person || weapon || room)) {
                 return false;
             }
         }
         return true;
    }

    public ArrayList<ClueElement> getRemainingPeople() {
         return this.clueNoteBook.getPeople();
    }

    public ArrayList<ClueElement> getRemainingWeapons() {
         return this.clueNoteBook.getWeapons();
    }

    public ArrayList<ClueElement> getRemainingRooms() {
         return this.clueNoteBook.getRooms();
    }

    public ArrayList<ArrayList<ClueElement>> remainingGuessCombos() {
         ArrayList<ArrayList<ClueElement>> comboList = new ArrayList<>();
         for (ClueElement p : getRemainingPeople()) {
             for (ClueElement w : getRemainingWeapons()) {
                 for (ClueElement r : getRemainingRooms()) {
                     comboList.add(new ArrayList<>(Arrays.asList(p, w, r)));
                 }
             }
         }
         return comboList;
    }

    public ClueNoteBook getClueNoteBook() {
        return clueNoteBook;
    }

    public static ClueElement getPersonByColour(String colour) {
        // Mustard, Plum, Scarlett, Peacock, White, Green
        String str = colour.toLowerCase();
        String name = null;
        for (PersonE personE : PersonE.values()) {
            if (personE.colour.equals(str)) {
                name = personE.name;
                break;
            }
        }
        int i = ((name != null)? peopleStr.indexOf(name) : -1);
        return ((i >= 0)? ORIG_people[i] : null);
    }

    public static ClueElement getWeaponByName(String weapon) {
        // "Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"
        int i = weaponStr.indexOf(weapon);
        return ((i >= 0)? ORIG_weapons[i] : null);
    }

    public static ClueElement getRoomByName(String room) {
        // "Spa", "Theater", "Living Room", "Observatory", "Patio", "Hall", "Guest House", "Kitchen", "Dining Room"
        int i = roomStr.indexOf(room);
        return ((i >= 0)? ORIG_rooms[i] : null);
    }

    @Override
    public String toString() {
         ArrayList<ArrayList<ClueElement>> combos = remainingGuessCombos();
        return clueNoteBook + "\n" + join("\n", combos) + "\nSize: " + combos.size();
    }
}

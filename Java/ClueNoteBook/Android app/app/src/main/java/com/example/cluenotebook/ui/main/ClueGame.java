package com.example.cluenotebook.ui.main;

import android.content.Context;
import android.os.Build;
import android.view.View;
import android.widget.ImageButton;

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

@RequiresApi(api = Build.VERSION_CODES.N)
public class ClueGame {

    ArrayList<String> peopleStr = new ArrayList<String>(Arrays.asList("Mustard", "Plum", "Scarlett", "Peacock", "White", "Green"));
    ArrayList<String> weaponStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
    ArrayList<String> roomStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
    ClueElement[] ORIG_people = peopleStr.stream().map(Person::NewPerson).toArray(Person[]::new);
    ClueElement[] ORIG_weapons = weaponStr.stream().map(Weapon::NewWeapon).toArray(Weapon[]::new);
    ClueElement[] ORIG_rooms = roomStr.stream().map(Room::NewRoom).toArray(Room[]::new);

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

    public ClueElement getPersonByColour(String colour) {
         // Mustard, Plum, Scarlett, Peacock, White, Green
         switch (colour.toLowerCase()) {
             case "white" : return ORIG_people[4];
             case "green" : return ORIG_people[5];
             case "blue" : return ORIG_people[3];
             case "purple" : return ORIG_people[1];
             case "red" : return ORIG_people[2];
             case "yellow": return ORIG_people[0];
             default: return null;
         }
    }

    public ClueElement getWeaponByName(String weapon) {
         // "Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"
        switch (weapon.toLowerCase()) {
            case "axe" : return ORIG_weapons[0];
            case "bat" : return ORIG_weapons[5];
            case "candlestick" : return ORIG_weapons[3];
            case "dumbbell" : return ORIG_weapons[7];
            case "knife" : return ORIG_weapons[6];
            case "poison": return ORIG_weapons[4];
            case "pistol": return ORIG_weapons[1];
            case "rope": return ORIG_weapons[2];
            case "trophy": return ORIG_weapons[8];
            default: return null;
        }
    }

    public ClueNoteBook getClueNoteBook() {
        return clueNoteBook;
    }
}

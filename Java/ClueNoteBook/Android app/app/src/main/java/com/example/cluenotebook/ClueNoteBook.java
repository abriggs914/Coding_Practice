package com.example.cluenotebook;

import android.os.Build;

import androidx.annotation.RequiresApi;

import java.util.*;

public class ClueNoteBook {

	private static ArrayList<ClueElement> people;
	private static ArrayList<ClueElement> weapons;
	private static ArrayList<ClueElement> rooms;
	private static ArrayList<ClueElement> history;

	public ClueNoteBook(ClueElement[] peopleIn, ClueElement[] weaponsIn, ClueElement[] roomsIn) {
		people = new ArrayList<>(Arrays.asList(peopleIn));
		weapons = new ArrayList<>(Arrays.asList(weaponsIn));
		rooms = new ArrayList<>(Arrays.asList(roomsIn));
		history = new ArrayList<>();
	}

	public void removeClueElement(ClueElement clueElement, ArrayList<ClueElement> lst) {
		if (lst.contains(clueElement)) {
			System.out.println(clueElement + " was revealed");
			history.add(clueElement);
		}
		else if (history.contains(clueElement)){
			System.out.println(clueElement + " has already been revealed");
		}
		else {
			System.out.println("ClueElement " + clueElement + " not recognized");
		}
	}

	public void seeCards(ClueElement... clues) {
		for (ClueElement clue : clues) {
			Class clazz = clue.getClass();
			ClueElement clueElement = clue;
			if (clazz.equals(Person.class)) {
				removeClueElement(clueElement, people);
				people.remove(clueElement);
			} else if (clazz.equals(Weapon.class)) {
				removeClueElement(clueElement, weapons);
				weapons.remove(clueElement);
			} else if (clazz.equals(Room.class)) {
				removeClueElement(clueElement, rooms);
				rooms.remove(clueElement);
			} else {
				System.out.println("ERROR");
			}
		}
	}

	public ArrayList<ClueElement> getPeople() {
		return people;
	}

	public ArrayList<ClueElement> getWeapons() {
		return weapons;
	}

	public ArrayList<ClueElement> getRooms() {
		return rooms;
	}

	public ArrayList<ClueElement> getHistory() {
		return history;
	}

	@Override
	public String toString() {
		String res = "\n\tClueNotebook\nPeople: " + people;
		res += "\nWeapons: " + weapons;
		res += "\nRooms: " + rooms;
		return res;
	}

	@RequiresApi(api = Build.VERSION_CODES.N)
	public static void main(String[] args) {
		ArrayList<String> peopleStr = new ArrayList<String>(Arrays.asList("Mustard", "Plum", "Scarlett", "Peacock", "White", "Green"));
		ArrayList<String> weaponStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
		ArrayList<String> roomStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
		ClueElement[] people = peopleStr.stream().map(Person::NewPerson).toArray(Person[]::new);
		ClueElement[] weapons = weaponStr.stream().map(Weapon::NewWeapon).toArray(Weapon[]::new);
		ClueElement[] rooms = roomStr.stream().map(Room::NewRoom).toArray(Room[]::new);

		ClueNoteBook CLN = new ClueNoteBook(people, weapons, rooms);
		System.out.println("CLN: " + CLN);
		CLN.seeCards(people[1]);
		System.out.println("CLN: " + CLN);
		CLN.seeCards(people[1]);
		System.out.println("CLN: " + CLN);
		CLN.seeCards(people[1]);
		System.out.println("CLN: " + CLN);
	}

}
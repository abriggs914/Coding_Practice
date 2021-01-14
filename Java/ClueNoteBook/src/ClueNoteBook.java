import java.util.*;
import java.util.stream.Collectors;

public class ClueNoteBook {
	
	public static class ClueElement {
		
		private final String name;
		
		public ClueElement(String name) {
			this.name = name;
		}
		
		public String getName() {
			return name;
		}
	}

	public static class Person extends ClueElement{
		
		public Person(String name) {
			super(name);
		}
	
		@Override
		public String toString() {
			return "<Person::" + this.getName() + ">";
		}
		
		public static Person NewPerson(String name) {
			return new Person(name);
		}
	}

	public static class Weapon extends ClueElement{
		
		public Weapon(String name) {
			super(name);
		}
	
		@Override
		public String toString() {
			return "<Weapon::" + this.getName() + ">";
		}
	
		public static Weapon NewWeapon(String name) {
			return new Weapon(name);
		}
	}

	public static class Room extends ClueElement{
		
		public Room(String name) {
			super(name);
		}
	
		@Override
		public String toString() {
			return "<Room::" + this.getName() + ">";
		}
	
		public static Room NewRoom(String name) {
			return new Room(name);
		}
	}

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

	public static void removeClueElement(ClueElement clueElement, ArrayList<ClueElement> lst) {
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

	public static void seenCards(ClueElement... clues) {
		for (int i = 0; i < clues.length; i++) {
			Class clazz = clues[i].getClass();
			ClueElement clueElement = clues[i];
			if (clazz.equals(Person.class)) {
				removeClueElement(clueElement, people);
				people.remove(clueElement);
			}
			else if (clazz.equals(Weapon.class)) {
				removeClueElement(clueElement, weapons);
				weapons.remove(clueElement);
			}
			else if (clazz.equals(Room.class)) {
				removeClueElement(clueElement, rooms);
				rooms.remove(clueElement);
			}
			else {
				System.out.println("ERROR");
			}
		}
	}

	public static ArrayList<ClueElement> getPeople() {
		return people;
	}

	public static ArrayList<ClueElement> getWeapons() {
		return weapons;
	}

	public static ArrayList<ClueElement> getRooms() {
		return rooms;
	}

	public static ArrayList<ClueElement> getHistory() {
		return history;
	}

	@Override
	public String toString() {
		String res = "\n\tClueNotebook\nPeople: " + people;
		res += "\nWeapons: " + weapons;
		res += "\nRooms: " + rooms;
		return res;
	}

	public static void main(String[] args) {
		ArrayList<String> peopleStr = new ArrayList<String>(Arrays.asList("Mustard", "Plum", "Scarlett", "Peacock", "White", "Green"));
		ArrayList<String> weaponStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
		ArrayList<String> roomStr = new ArrayList<String>(Arrays.asList("Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"));
		ClueElement[] people = peopleStr.stream().map(Person::NewPerson).toArray(Person[]::new);
		ClueElement[] weapons = weaponStr.stream().map(Weapon::NewWeapon).toArray(Weapon[]::new);
		ClueElement[] rooms = roomStr.stream().map(Room::NewRoom).toArray(Room[]::new);

		ClueNoteBook CLN = new ClueNoteBook(people, weapons, rooms);
		System.out.println("CLN: " + CLN);
		seenCards(people[1]);
		System.out.println("CLN: " + CLN);
		seenCards(people[1]);
		System.out.println("CLN: " + CLN);
		seenCards(people[1]);
		System.out.println("CLN: " + CLN);
	}
	
	// public static <T,V> Function<V,T> create(
		// Supplier<? extends T> constructor, BiConsumer<? super T, ? super V> setter) {
			// return v -> {
				// T t=constructor.get();
				// setter.accept(t, v);
				// return t;
			// };
		// }

}
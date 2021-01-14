import java.util.*;
import java.util.stream.Collectors;

public class ClueNoteBook {
	
	public class ClueElement {
		
		private String name;
		
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
			return "Person <" + this.getName() + ">";
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
			return "Weapon <" + this.getName() + ">";
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
			return "Room <" + this.getName() + ">";
		}
	
		public static Room NewRoom(String name) {
			return new Room(name);
		}
	}

	private static Person[] people;
	private static Weapon[] weapons;
	private static Room[] rooms;

	public ClueNoteBook(Person[] people, Weapon[] weapons, Room[] rooms) {
		this.people = people;
		this.weapons = weapons;
		this.rooms = rooms;
	}
	
	@Override
	public String toString() {
		String res = "\n\tClueNotebook\nPeople: " + Arrays.toString(people);
		res += "\nWeapons: " + Arrays.toString(weapons);
		res += "\nRooms: " + Arrays.toString(rooms);
		return res;
	}

	public static void main(String[] args) {
		ArrayList<String> peopleStr = new ArrayList<String>(Arrays.asList(new String[] {"Mustard", "Plum", "Scarlett", "Peacock", "White", "Green"}));
		ArrayList<String> weaponStr = new ArrayList<String>(Arrays.asList(new String[] {"Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"}));
		ArrayList<String> roomStr = new ArrayList<String>(Arrays.asList(new String[] {"Axe", "Pistol", "Rope", "Candlestick", "Poison", "Bat", "Knife", "Dumbbell", "Trophy"}));
		Person[] people = peopleStr.stream().map(p -> {return Person.NewPerson(p);}).collect(Collectors.toList()).toArray(new Person[0]); 
		Weapon[] weapons = weaponStr.stream().map(w -> {return Weapon.NewWeapon(w);}).collect(Collectors.toList()).toArray(new Weapon[0]); 
		Room[] rooms = roomStr.stream().map(r -> {return Room.NewRoom(r);}).collect(Collectors.toList()).toArray(new Room[0]); 
		// Weapon[] weapons = new Weapon[1];
		// Room[] rooms = new Room[1];
		
		List<Person> listOfPeople = peopleStr.stream().map(p -> {return Person.NewPerson(p);}).collect(Collectors.toList());
		// List<People> l = Arrays.stream(peopleStr).map(create(People::new, Foo::setName)).collect(Collectors.toList());
		// System.out.println("people: " + l);
		ClueNoteBook CLN = new ClueNoteBook(people, weapons, rooms);
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
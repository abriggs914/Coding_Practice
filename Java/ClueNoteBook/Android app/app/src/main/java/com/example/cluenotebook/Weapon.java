package com.example.cluenotebook;

public class Weapon extends ClueElement{
		
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
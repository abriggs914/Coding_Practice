package com.example.cluenotebook;

public class Room extends ClueElement{
		
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
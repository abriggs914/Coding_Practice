package com.example.cluenotebook;

public class Person extends ClueElement{
		
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
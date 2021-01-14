package com.example.cluenotebook;

public enum PersonE {
    SCARLETT ("Scarlett", "red"),
    PLUM ("Plum", "purple"),
    GREEN ("Green", "green"),
    MUSTARD ("Mustard", "yellow"),
    PEACOCK ("Peacock", "blue"),
    WHITE ("White", "white");

    public String name;
    public String colour;

    PersonE(String name, String colour){
        this.name = name;
        this.colour= colour;
    }
}

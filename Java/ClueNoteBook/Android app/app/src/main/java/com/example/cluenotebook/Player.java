package com.example.cluenotebook;

public class Player {

    private String name;
    private String colour;

    Player(String name, String colour) {
        this.name = name;
        this.colour = colour;
    }

    public String getName() {
        return name;
    }

    public String getColour() {
        return colour;
    }
}

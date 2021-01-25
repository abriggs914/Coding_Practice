package com.example.cluenotebook;

public enum PersonE {
    SCARLETT ("Scarlett", "red", R.drawable.red_token),
    PLUM ("Plum", "purple", R.drawable.purple_token),
    GREEN ("Green", "green", R.drawable.green_token),
    MUSTARD ("Mustard", "yellow", R.drawable.yellow_token),
    PEACOCK ("Peacock", "blue", R.drawable.blue_token),
    WHITE ("White", "white", R.drawable.white_token);

    public String name;
    public String colour;
    public int drawableID;

    PersonE(String name, String colour, int drawableID){
        this.name = name;
        this.colour= colour;
        this.drawableID = drawableID;
    }
}

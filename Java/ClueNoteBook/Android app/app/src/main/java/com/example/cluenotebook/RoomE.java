package com.example.cluenotebook;

public enum RoomE {
    SPA("Spa"),
    THEATER("Theater"),
    LIVING_ROOM("Living Room"),
    OBSERVATORY("Observatory"),
    PATIO("Patio"),
    HALL("Hall"),
    GUEST_HOUSE("Guest House"),
    KITCHEN("Kitchen"),
    DINING_ROOM("Dining Room");

    public String name;

    RoomE(String name) {
        this.name = name;
    }
}

package sample;

public class Card {

    private String suitID;
    private String faceID;
    private int faceRank;

    public Card(String suit, String face) {
        this.suitID = suit;
        this.faceID = face;
        this.faceRank = calcRank();
    }

    private int calcRank() {
        try {
            return Integer.parseInt(faceID);
        }
        catch(Exception e) {
            char x = faceID.charAt(0);
            switch (x) {
                case    'A' :   return 1;
                case    'J' :   return 11;
                case    'Q' :   return 12;
                case    'K' :   return 13;
                default     :   return 0;
            }
        }
    }

}

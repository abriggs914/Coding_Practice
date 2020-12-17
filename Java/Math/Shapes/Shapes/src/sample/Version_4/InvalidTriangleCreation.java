package sample.Version_4;

public class InvalidTriangleCreation extends Throwable {
    public InvalidTriangleCreation(int code, String message) {
        System.out.println("\nInvalid Triangle creation");
        switch (code) {
            case 1	:	System.out.println("Angles do not sum to 180."); break;
            case 2	:	System.out.println("Edge length cannot be equal to 0."); break;
            case 3	:	System.out.println("Triangles cannot have more than 3 sides."); break;
            case 4	:	System.out.println("Internal angle cannot be <= 0."); break;
            case 5	:	System.out.println("Triangles cannot have more than 3 internal angles."); break;
            case 6	:	System.out.println("Given angles have more than 3 distinct joining sides."); break;
            case 7  :   System.out.println("Angle computed to be NaN"); break;
            case 8  :   System.out.println("Edge computed to be NaN"); break;
            default	:	System.out.println("Invalid Triangle creation.");
        }
        System.out.println(message + "\n");
        this.printStackTrace();
        System.out.println("\n");
    }
}
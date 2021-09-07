import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class Driver {

    private static Random rand;

    private static ArrayList<Item> itemsB;
    private static ArrayList<Item> itemsP;
    private static ArrayList<Item> itemsS;

    public static void main(String[] args) {
        System.out.println("Hello World!");
        rand = new Random();

        Item b_0001 = new ItemB("b_0001", new ArrayList<>(Arrays.asList("blue", "white")));
        Item p_0001 = new ItemP("p_0001", new ArrayList<>(Arrays.asList("white", "pink")));
        Item s_0001 = new ItemS("s_0001", new ArrayList<>(Arrays.asList("white", "purple")));

        ArrayList<Item> itemsList = new ArrayList<>(Arrays.asList(
                b_0001,
                p_0001,
                s_0001
        ));

        System.out.println("\n\tItems:\n" + itemsList);
        System.out.println("\n\trandomItemB:\n" + randomItemB());
    }

    public static Item randomItemB() {
        rand.nextInt();
        return new Item("d", new ArrayList<>());
    }
}

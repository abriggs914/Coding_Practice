import java.util.ArrayList;
import java.util.Arrays;

public class Driver {

    public static void main(String[] args) {
        System.out.println("Hello World!");

        Item b_0001 = new ItemB("b_0001", new ArrayList<>(Arrays.asList("blue", "white")));
        Item p_0001 = new ItemP("p_0001", new ArrayList<>(Arrays.asList("white", "pink")));
        Item s_0001 = new ItemS("s_0001", new ArrayList<>(Arrays.asList("white", "purple")));

        ArrayList<Item> itemsList = new ArrayList<>(Arrays.asList(
                b_0001,
                p_0001,
                s_0001
        ));

        System.out.println("\n\tItems:\n" + itemsList);
    }
}

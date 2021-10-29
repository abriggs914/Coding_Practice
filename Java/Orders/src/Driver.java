import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Random;

public class Driver {

    private static Random rand;

    private static ArrayList<Item> originalItemsList;
    private static ArrayList<Item> itemsList;
    private static ArrayList<Item> itemsB;
    private static ArrayList<Item> itemsP;
    private static ArrayList<Item> itemsS;

    public static void main(String[] args) {
        rand = new Random();

        Item b_0001 = new ItemB("b_0001", new ArrayList<>(Arrays.asList("blue", "white")));
        Item p_0001 = new ItemP("p_0001", new ArrayList<>(Arrays.asList("white", "pink")));
        Item s_0001 = new ItemS("s_0001", new ArrayList<>(Arrays.asList("white", "purple")));

        itemsList = new ArrayList<>(Arrays.asList(
                b_0001,
                p_0001,
                s_0001
        ));
        originalItemsList = new ArrayList<>(itemsList);

//        filterByColour(new ArrayList<>(Collections.singletonList("pink")));
//        filterByColour(new ArrayList<>(Collections.singletonList("purple")));
        filterByColour(new ArrayList<>(Arrays.asList("pink", "purple")));
        System.out.println("\n\tItems:\n" + itemsList);
        System.out.println("\n\trandomItemB:\n" + randomItemB());
    }

    public static void resetItemsList() {
        itemsList = new ArrayList<>(originalItemsList);
    }

    public static void filterByColour(ArrayList<String> colours_list) {
        ArrayList<Item> filtered = new ArrayList<>();
        for (Item item : itemsList) {
            ArrayList<String> itemColourList = item.getColoursList();
            for (String colour : colours_list) {
                if (itemColourList.contains(colour)) {
                    filtered.add(item);
                    break;
                }
            }
        }
        itemsList = new ArrayList<>(filtered);
    }

    public static Item randomItemB() {
        if (itemsList.size() == 0) {
            return null;
        }
        return itemsList.get(rand.nextInt(itemsList.size()));
    }
}

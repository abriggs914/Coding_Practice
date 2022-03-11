package sample;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        ArrayList<WPWEntity> entities = new ArrayList<>();
        entities.add(new WPWEntity("Avery"));

        String a = "this is a string 1";
        String b = "this is a string 2";
        String c;
        c = a;
        a = "This is a String 3";

        System.out.println("a: {" + a + "}, b: {" + b + "}, c: {" + c + "}");

        entities.get(0).setBalance(14.5);
        System.out.println("Balance: " + entities.get(0).getBalance());
        System.out.println("entities: " + entities);
    }
}

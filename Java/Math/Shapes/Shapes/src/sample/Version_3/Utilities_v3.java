package sample;

import java.text.NumberFormat;

public class Utilities_v3 {

    public static String twoDecimal(double d) {
        NumberFormat nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(2);
        nf.setMinimumFractionDigits(2);
        return nf.format(d);
    }

    /**
     * Recursively calculate the greatest common factor of 2 integers.
     * @param a Integer a.
     * @param b Integer b.
     * @return Greatest common factor.
     */
    public static int gcf(int a, int b) {
        if (b == 0) {
            return a;
        }
        else {
            return gcf(b, a % b);
        }
    }

}

package sample;

import java.util.Random;

public class RSAEncryption {

    public RSAEncryption() {

    }

    public int generatePrimeNumber() {
        Random rnd = new Random();
        double rdnN = (rnd.nextDouble() * 4000) + 1000;
        int roundN = (int) rdnN;
        System.out.println("rndN (double):\t" + rdnN + "\troundN (int):\t" + roundN);
        return roundN;
    }
}

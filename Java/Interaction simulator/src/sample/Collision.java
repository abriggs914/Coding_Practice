package sample;

import java.util.Arrays;

public class Collision {

    private String idString;
    private int idNumber;
    private Person person_A;
    private Person person_B;

    public Collision(String idString, int idNumber, Person person_a, Person person_b) {

        this.idString = idString;
        this.idNumber = idNumber;
        person_A = person_a;
        person_B = person_b;
    }

    /**
     * Calculate the final velocities of two objects after
     * a completely elastic collision.
     * @return Double array (velocityA, velocityB)
     */
    public double[] getFinalVelocities(double massA, double massB, double velA1, double velB1) {
//        System.out.print("\tvelA1: " + velA1 + ", velB1: " + velB1 + " -> ");
        double velC1 = velA1 - velB1;
        double velD2 = (2 * velC1) / (massB / massA + 1);

        double velB2 = velD2 + velB1;

        double velC2 = velC1 - (massB * (velD2 / massA));
        double velA2 = velC2 + velB1;
//        System.out.println("velA2: " + velA2 + ", velB2: " + velB2);
        return new double[] {velA2, velB2};
    }

    public Person getPerson_A() {
        return person_A;
    }

    public Person getPerson_B() {
        return person_B;
    }

    public Vector[] collide() {
        Vector a = person_A.getDirectionVector();
        Vector b = person_B.getDirectionVector();
        double massA = person_A.getMass();
        double massB = person_B.getMass();
        double[] aComponents = a.getAxisComponents();
        double[] bComponents = b.getAxisComponents();
        double[] xchange = getFinalVelocities(massA, massB, aComponents[0], bComponents[0]);
        double[] ychange = getFinalVelocities(massA, massB, aComponents[1], bComponents[1]);
        Vector v1 = Vector.combineXYComponents(xchange[0], ychange[0]);
        Vector v2 = Vector.combineXYComponents(xchange[1], ychange[1]);
        System.out.println("xchange: " + Arrays.toString(xchange) + ", ychange: " + Arrays.toString(ychange) + "\nv1: " + v1 + ", v2: " + v2);
        return new Vector[] {v1, v2};
    }

    @Override
    public String toString() {
        return "Collision " + idNumber + " between:\n\t" + person_A + ", vector: " + person_A.getDirectionVector() + "\n\t" + person_B + ", vector: " + person_B.getDirectionVector() + ".";
    }
}

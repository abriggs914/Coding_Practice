package sample.Version_4;

import java.text.NumberFormat;

import static sample.Version_4.Triangle.SIDE_A;
import static sample.Version_4.Triangle.SIDE_B;
import static sample.Version_4.Triangle.SIDE_C;
import static sample.Version_4.Triangle.ANGLE_A;
import static sample.Version_4.Triangle.ANGLE_B;
import static sample.Version_4.Triangle.ANGLE_C;

public class Utilities {

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

    public static double lawOfCosines(Triangle t, String code) {
        double a, b, c, A, B, C, x;
        Edge sideA = t.getSideA(), sideB = t.getSideB(), sideC = t.getSideC();
        Angle angleA = t.getAngleA(), angleB = t.getAngleB(), angleC = t.getAngleC();
        double res = 0;
        if (!t.attrIsKnown(code)) {
            if (t.solvable_LOC(code)) {
                a = ((t.attrIsKnown(SIDE_A))? sideA.getLength() : 0);
                b = ((t.attrIsKnown(SIDE_B))? sideB.getLength() : 0);
                c = ((t.attrIsKnown(SIDE_C))? sideC.getLength() : 0);
                A = ((t.attrIsKnown(ANGLE_A))? angleA.getAngle() : 0);
                B = ((t.attrIsKnown(ANGLE_B))? angleB.getAngle() : 0);
                C = ((t.attrIsKnown(ANGLE_C))? angleC.getAngle() : 0);
                if (code.equals(SIDE_A)){
                    //System.out.println("b^2: " + Math.pow(b, 2) + "\nc^2: " + Math.pow(c, 2) + "\n2*b*c: " + (2 * b * c) + "\ncos(A): " + Math.cos(A) + "\nMath.toDegrees(Math.cos(A)): " + Math.toDegrees(Math.cos(A)) + "\nRES_1: " + Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * Math.toDegrees(Math.cos(A)))) + "\nRES_2: " + Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * (Math.cos(A)))));
                    res = Math.sqrt(Math.pow(b, 2) + Math.pow(c, 2) - (2 * b * c * (Math.cos(A))));
                    // res = Math.sqrt(b*b + c*c - (2 * b * c * Math.cos(A)));

                }
                else if (code.equals(SIDE_B)) {
                    res = Math.sqrt(Math.pow(a, 2) + Math.pow(c, 2) - (2 * a * c * (Math.cos(B))));
                    // if (t.b != null) {
                    // res = t.b.length;
                    // }
                }
                else if (code.equals(SIDE_C)) {
                    res = Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2) - (2 * a * b * (Math.cos(C))));
                    // if (t.c != null) {
                    // // res = t.c.length;
                    // }
                }
                else if (code.equals (ANGLE_A)) {
                    res = Math.toDegrees(Math.acos((Math.pow(a, 2) - (Math.pow(b, 2) + Math.pow(c, 2))) / (-2 * b * c)));
                    // res = (Math.acos((Math.pow(a, 2) - (Math.pow(b, 2) + Math.pow(c, 2))) / (-2 * b * c)));
                    // if (t.A != null) {
                    // res = t.A.angle;
                    // }
                }
                else if (code.equals(ANGLE_B)) {
                    res = Math.toDegrees(Math.acos((Math.pow(b, 2) - (Math.pow(a, 2) + Math.pow(c, 2))) / (-2 * a * c)));
                    // res = (Math.acos((Math.pow(b, 2) - (Math.pow(a, 2) + Math.pow(c, 2))) / (-2 * a * c)));
                    // if (t.B != null) {
                    // res = t.B.angle;
                    // }
                }
                else if (code.equals(ANGLE_C)) {
                    res = Math.toDegrees(Math.acos((Math.pow(c, 2) - (Math.pow(a, 2) + Math.pow(b, 2))) / (-2 * a * b)));
                    // res = (Math.acos((Math.pow(c, 2) - (Math.pow(a, 2) + Math.pow(b, 2))) / (-2 * a * b)));
                    // if (t.C != null) {
                    // res = t.C.angle;/
                    // }
                }
                else {
                    System.out.println("INVALID code");
                }
            }
            else {
                System.out.println("UNSOLVABLE");
            }
        }
        else {
            if (code.equals(SIDE_A)) {
                res = sideA.getLength();
            }
            else if (code.equals(SIDE_B)) {
                res = sideB.getLength();
            }
            else if (code.equals(SIDE_C)) {
                res = sideC.getLength();
            }
            else if (code.equals(ANGLE_A)) {
                res = angleA.getAngle();
            }
            else if (code.equals(ANGLE_B)) {
                res = angleB.getAngle();
            }
            else if (code.equals(ANGLE_C)) {
                res = angleC.getAngle();
            }
        }
        return res;
    }

    public static double lawOfSines(Triangle t, String code) {
        // t3 doesnt solve correctly
        double a, b, c, A, B, C;
        Edge sideA = t.getSideA(), sideB = t.getSideB(), sideC = t.getSideC();
        Angle angleA = t.getAngleA(), angleB = t.getAngleB(), angleC = t.getAngleC();
        double res = 0;
        if (!t.attrIsKnown(code)) {
            if (t.solvable_LOS(code)) {
                a = ((t.attrIsKnown(SIDE_A))? sideA.getLength(): 0);
                b = ((t.attrIsKnown(SIDE_B))? sideB.getLength() : 0);
                c = ((t.attrIsKnown(SIDE_C))? sideC.getLength() : 0);
                A = ((t.attrIsKnown(ANGLE_A))? angleA.getAngle() : 0);
                B = ((t.attrIsKnown(ANGLE_B))? angleB.getAngle() : 0);
                C = ((t.attrIsKnown(ANGLE_C))? angleC.getAngle() : 0);
                Edge pairS;
                Angle pairA;
                if (t.attrIsKnown(SIDE_A, ANGLE_A)) {
                    pairS = sideA;
                    pairA = angleA;
                }
                else if (t.attrIsKnown(SIDE_B, ANGLE_B)) {
                    pairS = sideB;
                    pairA = angleB;
                }
                else if (t.attrIsKnown(SIDE_C, ANGLE_C)) {
                    pairS = sideC;
                    pairA = angleC;
                }
                else {
                    System.out.println("\n\tQUITTING EARLY\n");
                    System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
                    // System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);

                    return res;
                }
                if (code.equals(SIDE_A)) {
                    res = Math.sin(A) * (pairS.getLength() / Math.sin(pairA.getAngle()));
                }
                else if (code.equals(SIDE_B)) {
                    res = Math.sin(B) * (pairS.getLength() / Math.sin(pairA.getAngle()));
                }
                else if (code.equals(SIDE_C)) {
                    res = Math.sin(C) * (pairS.getLength() / Math.sin(pairA.getAngle()));
                }
                else if (code.equals(ANGLE_A)) {
                    // res = Math.toDegrees(Math.asin(a * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(a * (Math.sin(Math.toRadians(pairA.getAngle())) / pairS.getLength())));
                    // System.out.println("pairA.angle: " + pairA.angle + "\nMath.sin(pairA): " + Math.sin(pairA.angle) + "\nMath.toDegrees(Math.sin(pairA)): " + Math.toDegrees(Math.sin(pairA.angle)) + "\nMath.toDegrees(Math.sin(Math.toRadians(pairA))): " + Math.toDegrees(Math.sin(Math.toRadians(pairA.angle))) + "\nMath.sin(Math.toRadians(pairA))): " + Math.sin(Math.toRadians(pairA.angle)));
                    // System.out.println("¨Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48): " + Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))));
                    // System.out.println("¨Math.toDegrees(Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48)): " + Math.toDegrees(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60)))));
                    // System.out.println("¨Math.toDegrees(Math.asin(Math.toRadians(Math.sin(Math.toRadians(pairA))) / 60) * 48))): " + Math.toDegrees(Math.toRadians(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))))));
                }
                else if (code.equals(ANGLE_B)) {
                    // res = Math.toDegrees(Math.asin(b * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(b * (Math.sin(Math.toRadians(pairA.getAngle())) / pairS.getLength())));
                }
                else if (code.equals(ANGLE_C)) {
                    // res = Math.toDegrees(Math.asin(c * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(c * (Math.sin(Math.toRadians(pairA.getAngle())) / pairS.getLength())));
                }
                System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
                System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);

            }
        }
        else {
            if (code.equals(SIDE_A)) {
                res = sideA.getLength();
            }
            else if (code.equals(SIDE_B)) {
                res = sideB.getLength();
            }
            else if (code.equals(SIDE_C)) {
                res = sideC.getLength();
            }
            else if (code.equals(ANGLE_A)) {
                res = angleA.getAngle();
            }
            else if (code.equals(ANGLE_B)) {
                res = angleB.getAngle();
            }
            else if (code.equals(ANGLE_C)) {
                res = angleC.getAngle();
            }
        }
        return res;
    }

}

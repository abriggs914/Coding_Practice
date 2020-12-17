package sample.Version_3;

import javafx.collections.ObservableList;
import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;

import java.util.ArrayList;
import java.util.Arrays;

import static sample.Model_v3.*;

public class Triangle_v3 extends sample.Shape_v3 {



    public static final String SIDE_A = "a";
    public static final String SIDE_B = "b";
    public static final String SIDE_C = "c";
    public static final String ANGLE_A = "A";
    public static final String ANGLE_B = "B";
    public static final String ANGLE_C = "C";

    private String name;
    private ArrayList<sample.Side_v3> sides;
    private ArrayList<sample.Angle_v3> angles;
    private boolean onOrigin;
    private boolean placed;

    public sample.Side_v3 a, b, c;
    public sample.Angle_v3 A, B, C;
    public double ax, ay, bx, by, cx, cy;
    public Point2D intersectionAB;
    public Point2D intersectionAC;
    public Point2D intersectionBC;
    public Polygon polygon;
    public Line lineA;
    public Line lineB;
    public Line lineC;

    public Triangle_v3(String name, sample.Side_v3 a, sample.Side_v3 b, sample.Side_v3 c, sample.Angle_v3 A, sample.Angle_v3 B, sample.Angle_v3 C) {
        this.name = name;
        this.initSides(a, b, c);
        this.initAngles(A, B, C);

        this.solveRemainingTriangle();
    }

    public Triangle_v3(String name, double ax, double ay, double bx, double by, double cx, double cy, sample.Side_v3 a, sample.Side_v3 b, sample.Side_v3 c, sample.Angle_v3 A, sample.Angle_v3 B, sample.Angle_v3 C) {
        this.name = name;
        this.initPoints(ax, ay, bx, by, cx, cy);
        this.initSides(a, b, c);
        this.initAngles(A, B, C);
//        this.calcIntersections();

        this.solveRemainingTriangle();
    }

//    Polygon p = WhiteBoardModel.createTriangle(a, b, c);
    public Triangle_v3(String name, Line a, Line b, Line c) {
        this.name = name;
        this.polygon = this.createPolygon(a, b, c, Color.DARKGRAY);

        ObservableList<Double> points = this.polygon.getPoints();
        double ax = points.get(0);
        double ay = points.get(1);
        double bx = points.get(2);
        double by = points.get(3);
        double cx = points.get(4);
        double cy = points.get(5);
        this.initPoints(ax, ay, bx, by, cx, cy);

        ArrayList<sample.Side_v3> sides = this.calcSides(this.polygon, a, b, c);
        sample.Side_v3 sideA = sides.get(0);
        sample.Side_v3 sideB = sides.get(1);
        sample.Side_v3 sideC = sides.get(2);
        this.initSides(sideA, sideB, sideC);

        this.solveRemainingTriangle();
    }

    public ArrayList<sample.Side_v3> calcSides(Polygon polygon, Line a, Line b, Line c) {
        ObservableList<Double> points = this.polygon.getPoints();
        double ax = points.get(0);
        double ay = points.get(1);
        double bx = points.get(2);
        double by = points.get(3);
        double cx = points.get(4);
        double cy = points.get(5);
        Point2D aStart = new Point2D(ax, ay);
        Point2D aEnd = new Point2D(a.getEndX(), a.getEndY());
        Point2D bStart = new Point2D(bx, by);
        Point2D bEnd = new Point2D(b.getEndX(), b.getEndY());
        Point2D cStart = new Point2D(cx, cy);
        Point2D cEnd = new Point2D(c.getEndX(), c.getEndY());
        double lenA = aStart.distance(aEnd);
        double lenB = bStart.distance(bEnd);
        double lenC = cStart.distance(cEnd);
        sample.Side_v3 sideA = new sample.Side_v3("side a", lenA);
        sample.Side_v3 sideB = new sample.Side_v3("side b", lenB);
        sample.Side_v3 sideC = new sample.Side_v3("side c", lenC);
        return new ArrayList<>(Arrays.asList(sideA, sideB, sideC));
    }

    public Polygon createPolygon(Line a, Line b, Line c, Color col) {
        Point2D intersectionAB = intersectionPoint(a, b);
        Point2D intersectionAC = intersectionPoint(a, c);
        Point2D intersectionBC = intersectionPoint(b, c);
        Polygon p = new Polygon(intersectionAB.getX(), intersectionAB.getY(), intersectionAC.getX(), intersectionAC.getY(), intersectionBC.getX(), intersectionBC.getY());
        p.setFill(col);
        return p;
    }

    public void initPoints(double ax, double ay, double bx, double by, double cx, double cy) {
        this.setPointA(ax, ay);
        this.setPointB(bx, by);
        this.setPointC(cx, cy);
        this.lineA = new Line(ax, ay, bx, by);
        this.lineB = new Line(bx, by, cx, cy);
        this.lineC = new Line(cx, cy, ax, ay);
        this.intersectionAB = intersectionPoint(lineA, lineB);
        this.intersectionAC = intersectionPoint(lineA, lineC);
        this.intersectionBC = intersectionPoint(lineB, lineC);
        this.placed = true;
        this.polygon = this.createPolygon(lineA, lineB, lineC, Color.DARKGRAY);
    }

    public void calcIntersections() {

    }

    public void setPointA(double ax, double ay) {
        this.ax = ax;
        this.ay = ay;
    }

    public void setPointB(double bx, double by) {
        this.bx = bx;
        this.by = by;
    }

    public void setPointC(double cx, double cy) {
        this.cx = cx;
        this.cy = cy;
    }

    public void initSides(sample.Side_v3 a, sample.Side_v3 b, sample.Side_v3 c) {
        if (a != null) {
            this.setSideA(a);
        }
        if (b != null) {
            this.setSideB(b);
        }
        if (c != null) {
            this.setSideC(c);
        }
    }

    public void initAngles(sample.Angle_v3 A, sample.Angle_v3 B, sample.Angle_v3 C) {
        if (A != null) {
            this.setAngleA(A);
        }
        if (B != null) {
            this.setAngleB(B);
        }
        if (C != null) {
            this.setAngleC(C);
        }
    }

    // // Empty triangle
    // public Triangle(String name) {
    // this.init(name);
    // }

    // // SSS triangle
    // public Triangle(String name, Edge a, Edge b, Edge c, String code) throws InvalidTriangleCreation{
    // this.init(name);
    // this.addSides(a, b, c);
    // }

    // // AAA triangle
    // public Triangle(String name, Angle a, Angle b, Angle c, String code) throws InvalidTriangleCreation{
    // double s = a.angle + b.angle + c.angle;
    // if (s != 180) {
    // throw new InvalidTriangleCreation(1, "Sum: " + s);
    // }
    // this.init(name);
    // this.addAngles(a, b, c);
    // }

    // public Triangle(String name, Angle angle, String code) throws InvalidTriangleCreation{
    // this.init(name);
    // Edge a = angle.a;
    // Edge b = angle.b;
    // if (a != null && b != null) {
    // this.addSides(a, b);
    // }
    // Angle a1, a2;
    // a1 = new Angle("A", 0);
    // a2 = new Angle("B", 0);
    // this.setAngleA(a1);
    // this.setAngleB(a2);
    // this.addAngles(angle);
    // }

    /*
        // SAS triangle
        public Triangle(String name, Edge a, Angle b, Edge c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(a, c);
            this.addAngles(b);
        }

        // ASS triangle
        public Triangle(String name, Angle a, Edge b, Edge c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(b, c);
            this.addAngles(a);
        }

        // SSA triangle
        public Triangle(String name, Edge a, Edge b, Angle c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(a, b);
            this.addAngles(c);
        }

        // ASA triangle
        public Triangle(String name, Angle a, Edge b, Angle c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(b);
            this.addAngles(a, c);
        }

        // AAS triangle
        public Triangle(String name, Angle a, Angle b, Edge c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(c);
            this.addAngles(a, b);
        }

        // SAA triangle
        public Triangle(String name, Edge a, Angle b, Angle c) throws InvalidTriangleCreation{
            this.init(name);
            this.addSides(a);
            this.addAngles(b, c);
        }
        */
    private void init(String name) {
        this.name = name;
        this.placed = false;
        this.sides = new ArrayList<>();
        this.angles = new ArrayList<>();
    }

    public void solveRemainingTriangle() {
        ArrayList<String> toCheck = new ArrayList<>(Arrays.asList(SIDE_A, SIDE_B, SIDE_C, ANGLE_A, ANGLE_B, ANGLE_C));
        boolean loop = true;
        boolean changed = false;
        int i = 0;
        while (loop){
            String code = toCheck.get(i);
            if (!this.attrIsKnown(code)) {
//                System.out.println("code: " +  code + " is unknown");
                sample.Side_v3 s;
                sample.Angle_v3 a;
                double n;
                if (this.solvable_LOC(code)) {
                    n = lawOfCosines(this, code);;
//                    System.out.println("\n\n\t\tsolvable LOC\n\tcode:" + code + ", n: " + n + "\n");
                    changed = true;
                    switch (i) {
                        case 0	:	s = new sample.Side_v3("side a", n);
                            this.setSideA(s);
                            break;
                        case 1	:	s = new sample.Side_v3("side b", n);
                            this.setSideB(s);
                            break;
                        case 2	:	s = new sample.Side_v3("side c", n);
                            this.setSideC(s);
                            break;
                        case 3	:	a = new sample.Angle_v3("angle A", n);
                            this.setAngleA(a);
                            break;
                        case 4	:	a = new sample.Angle_v3("angle B", n);
                            this.setAngleB(a);
                            break;
                        case 5	:	a = new sample.Angle_v3("angle C", n);
                            this.setAngleC(a);
                            break;
                        default :	changed = false;
                    }
                }
                else if (this.solvable_LOS(code)) {
                    n = lawOfSines(this, code);
//                    System.out.println("\n\n\t\tsolvable LOS\n\tcode:" + code + ", n: " + n + "\n");
                    changed = true;
                    switch (i) {
                        case 0	:	s = new sample.Side_v3("side a", n);
                            this.setSideA(s);
                            break;
                        case 1	:	s = new sample.Side_v3("side b", n);
                            this.setSideB(s);
                            break;
                        case 2	:	s = new sample.Side_v3("side c", n);
                            this.setSideC(s);
                            break;
                        case 3	:	a = new sample.Angle_v3("angle A", n);
                            this.setAngleA(a);
                            break;
                        case 4	:	a = new sample.Angle_v3("angle B", n);
                            this.setAngleB(a);
                            break;
                        case 5	:	a = new sample.Angle_v3("angle C", n);
                            this.setAngleC(a);
                            break;
                        default :	changed = false;
                    }
                }
                else {
//                    System.out.println("code: " + code + " is not solvable using LOS or LOC");
                }
                if (this.solvable_AAA()) {
                    changed = true;
                    double angleA, angleB, angleC;
                    angleA = ((this.attrIsKnown(ANGLE_A))? this.A.angle : 0);
                    angleB = ((this.attrIsKnown(ANGLE_B))? this.B.angle : 0);
                    angleC = ((this.attrIsKnown(ANGLE_C))? this.C.angle : 0);
                    n = 180 - (angleA + angleB + angleC);
//                    System.out.println("\n\n\t\tsolvable AAA\n\tcode:" + code + ", n: " + n + "\n");
                    if (!this.attrIsKnown(ANGLE_A)) {
                        a = new sample.Angle_v3("angle A", n);
                        this.setAngleA(a);
                    }
                    else if (!this.attrIsKnown(ANGLE_B)) {
                        a = new sample.Angle_v3("angle B", n);
                        this.setAngleB(a);
                    }
                    else if (!this.attrIsKnown(ANGLE_C)) {
                        a = new sample.Angle_v3("angle C", n);
                        this.setAngleC(a);
                    }
                }
            }
            else {
//                System.out.println("code: " + code + " is KNOWN");
            }

            i += 1;
            if (!changed && i == toCheck.size()){
                break;
            }
            i %= toCheck.size();
            if (changed && i == 0){
                changed = false;
            }
            // System.out.println("j: " + Integer.toString(j) + " c: " + Integer.toString(c));
        }
    }

    // Logically check if the current state of this Triangle object can be solved for the given code.
    public boolean solvable_LOC(String code) {
        boolean dims = true;//(this.sides.size() + this.angles.size()) >= 3;
        boolean init = this.attrIsKnown(code);
        // System.out.println(this.toString());
        if (code.equals(SIDE_A)) {
            init |= this.b != null && this.c != null && this.A != null;
        }
        else if (code.equals(SIDE_B)) {
            init |= this.a != null && this.c != null && this.B != null;
        }
        else if (code.equals(SIDE_C)) {
            init |= this.a != null && this.b != null && this.C != null;
        }
        else if (code.equals(ANGLE_A) || code.equals(ANGLE_B) || code.equals(ANGLE_C)) {
            init |= this.a != null && this.b != null && this.c != null;
        }
        else {
            System.out.println("INVALID code");
        }
        return init;
    }

    public boolean solvable_LOS(String code) {
        boolean init = this.attrIsKnown(code);
        boolean pair = this.attrIsKnown(SIDE_A, ANGLE_A);// && (!code.equals(SIDE_A) && !code.equals(ANGLE_A));
        pair |= this.attrIsKnown(SIDE_B, ANGLE_B);// && (!code.equals(SIDE_B) && !code.equals(ANGLE_B));
        pair |= this.attrIsKnown(SIDE_C, ANGLE_C);// && (!code.equals(SIDE_C) && !code.equals(ANGLE_C));
        // Edge pairS;
        // Angle pairA;
        // if (t.attrIsKnown(SIDE_A, ANGLE_A)) {
        // pairS = t.a;
        // pairA = t.A;
        // }
        // else if (t.attrIsKnown(SIDE_B, ANGLE_B)) {
        // pairS = t.b;
        // pairA = t.B;
        // }
        // else if (t.attrIsKnown(SIDE_C, ANGLE_C)) {
        // pairS = t.c;
        // pairA = t.C;
        // }
        // System.out.println("pair: " + pair);
        if (code.equals(SIDE_A)) {
            init |= pair && this.attrIsKnown(ANGLE_A);
        }
        else if (code.equals(SIDE_B)) {
            init |= pair && this.attrIsKnown(ANGLE_B);
        }
        else if (code.equals(SIDE_C)) {
            init |= pair && this.attrIsKnown(ANGLE_C);
        }
        else if (code.equals(ANGLE_A)) {
            init |= pair && this.attrIsKnown(SIDE_A);
        }
        else if (code.equals(ANGLE_B)) {
            init |= pair && this.attrIsKnown(SIDE_B);
        }
        else if (code.equals(ANGLE_C)) {
            init |= pair && this.attrIsKnown(SIDE_C);
        }
        else {
            System.out.println("INVALID code");
        }
        return init;
    }

    public boolean solvable_AAA() {
        int c = 0;
        c += ((this.attrIsKnown(ANGLE_A))? 1 : 0);
        c += ((this.attrIsKnown(ANGLE_B))? 1 : 0);
        c += ((this.attrIsKnown(ANGLE_C))? 1 : 0);
        return c > 1;
    }

    public boolean attrIsKnown(String... codes) {
        boolean known = (codes.length > 0);
        for (int i = 0; i < codes.length; i++) {
            String code = codes[i];
            if (code.equals(SIDE_A)) {
                known &= this.a != null;
            }
            else if (code.equals(SIDE_B)) {
                known &= this.b != null;
            }
            else if (code.equals(SIDE_C)) {
                known &= this.c != null;
            }
            else if (code.equals(ANGLE_A)) {
                known &= this.A != null;
            }
            else if (code.equals(ANGLE_B)) {
                known &= this.B != null;
            }
            else if (code.equals(ANGLE_C)) {
                known &= this.C != null;
            }
            // else {
            // return false;
            // }
            // if (!known) {
            // return false;
            // }
        }
        return known;
    }

    public boolean isPlaced() {
        return this.placed;
    }

    public void addSides(sample.Side_v3... sides) throws sample.InvalidTriangleCreation_v3 {
        for (int i = 0; i < sides.length; i++) {
            if (sides[i].length <= 0) {
                throw new sample.InvalidTriangleCreation_v3(2, "Edge: <" + sides[i].length + "> is invalid");
            }
            this.sides.add(sides[i]);
            if (this.sides.size() > 3) {
                throw new sample.InvalidTriangleCreation_v3(3, "");
            }
            //int j = i % 3;
        }
        for (int i = 0; i < this.sides.size(); i++) {
            System.out.println("j: " + i);
            switch (i) {
                case 0	:	this.a = this.sides.get(i); break;
                case 1	:	this.b = this.sides.get(i); break;
                case 2	:	this.c = this.sides.get(i); break;
                default :	System.out.println("INDEX OUT OF BOUNDS");
            }
        }
        // if (this.sides.size() == 3) {
        // this.a = this.sides.get(0);
        // this.b = this.sides.get(1);
        // this.c = this.sides.get(2);
        // }
    }

    public void addAngles(sample.Angle_v3... angles) throws sample.InvalidTriangleCreation_v3 {
        double sum = 0;
        ArrayList<sample.Side_v3> sides = new ArrayList<>();
        for (int i = 0; i < this.angles.size(); i++) {
            sample.Angle_v3 angle = this.angles.get(i);
            sum += angle.angle;
            sample.Side_v3 a = angle.a;
            sample.Side_v3 b = angle.b;
            if (!sides.contains(a)) {
                sides.add(a);
            }
            if (!sides.contains(b)) {
                sides.add(b);
            }
        }
        for (int i = 0; i < angles.length; i++) {
            sample.Angle_v3 angle = angles[i];
            sample.Side_v3 a = angle.a;
            sample.Side_v3 b = angle.b;
            if (!sides.contains(a)) {
                sides.add(a);
            }
            if (!sides.contains(b)) {
                sides.add(b);
            }
            if (sides.size() > 3) {
                throw new sample.InvalidTriangleCreation_v3(6, "");
            }
            if (angle.angle <= 0) {
                throw new sample.InvalidTriangleCreation_v3(4, "Angle: <" + angle.angle + "> is invalid");
            }
            sum += angle.angle;
            this.angles.add(angle);
            if (this.angles.size() > 3) {
                throw new sample.InvalidTriangleCreation_v3(5, "");
            }
        }
        if (this.angles.size() == 3) {
            if (sum != 180) {
                throw new sample.InvalidTriangleCreation_v3(1, "Angle sum: " + sum + ", is too large");
            }
            // this.A = this.angles.get(0);
            // this.B = this.angles.get(1);
            // this.C = this.angles.get(2);
        }
        for (int i = 0; i < this.angles.size(); i++) {
            System.out.println("j: " + i);
            switch (i) {
                case 0	:	this.A = this.angles.get(i); break;
                case 1	:	this.B = this.angles.get(i); break;
                case 2	:	this.C = this.angles.get(i); break;
                default :	System.out.println("INDEX OUT OF BOUNDS");
            }
        }
    }

    public void setSideA(sample.Side_v3 a) {this.a = a;}
    public void setSideB(sample.Side_v3 b) {this.b = b;}
    public void setSideC(sample.Side_v3 c) {this.c = c;}
    public void setAngleA(sample.Angle_v3 A) {this.A = A;}
    public void setAngleB(sample.Angle_v3 B) {this.B = B;}
    public void setAngleC(sample.Angle_v3 C) {this.C = C;}

    public String toString() {
        //return "\n" + this.name + "\nsides: " + this.sides + "\nAngles: " + this.angles;
        String res = "\nName: " + this.name;
        res += "\na: " + ((this.a == null)? "null" : this.a);
        res += "\nb: " + ((this.b == null)? "null" : this.b);
        res += "\nc: " + ((this.c == null)? "null" : this.c);
        res += "\nA: " + ((this.A == null)? "null" : this.A);
        res += "\nB: " + ((this.B == null)? "null" : this.B);
        res += "\nC: " + ((this.C == null)? "null" : this.C);
        res += "\n(ax, ay): (" + this.ax + ", " + this.ay + ")";
        res += "\n(bx, by): (" + this.bx + ", " + this.by + ")";
        res += "\n(cx, cy): (" + this.cx + ", " + this.cy + ")";
        res += "\narea: " + ((this.polygon == null)? "null" : this.area());
        res += "\nperimeter: " + ((this.polygon == null)? "null" : this.perimeter());
        return res;
    }

    public static double lawOfCosines(Triangle_v3 t, String code) {
        double a, b, c, A, B, C, x;
        double res = 0;
        if (!t.attrIsKnown(code)) {
            if (t.solvable_LOC(code)) {
                a = ((t.attrIsKnown(SIDE_A))? t.a.length : 0);
                b = ((t.attrIsKnown(SIDE_B))? t.b.length : 0);
                c = ((t.attrIsKnown(SIDE_C))? t.c.length : 0);
                A = ((t.attrIsKnown(ANGLE_A))? t.A.angle : 0);
                B = ((t.attrIsKnown(ANGLE_B))? t.B.angle : 0);
                C = ((t.attrIsKnown(ANGLE_C))? t.C.angle : 0);
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
                res = t.a.length;
            }
            else if (code.equals(SIDE_B)) {
                res = t.b.length;
            }
            else if (code.equals(SIDE_C)) {
                res = t.c.length;
            }
            else if (code.equals(ANGLE_A)) {
                res = t.A.angle;
            }
            else if (code.equals(ANGLE_B)) {
                res = t.B.angle;
            }
            else if (code.equals(ANGLE_C)) {
                res = t.C.angle;
            }
        }
        return res;
    }

    public static double lawOfSines(Triangle_v3 t, String code) {
        // t3 doesnt solve correctly
        double a, b, c, A, B, C;
        double res = 0;
        if (!t.attrIsKnown(code)) {
            if (t.solvable_LOS(code)) {
                a = ((t.attrIsKnown(SIDE_A))? t.a.length : 0);
                b = ((t.attrIsKnown(SIDE_B))? t.b.length : 0);
                c = ((t.attrIsKnown(SIDE_C))? t.c.length : 0);
                A = ((t.attrIsKnown(ANGLE_A))? t.A.angle : 0);
                B = ((t.attrIsKnown(ANGLE_B))? t.B.angle : 0);
                C = ((t.attrIsKnown(ANGLE_C))? t.C.angle : 0);
                sample.Side_v3 pairS;
                sample.Angle_v3 pairA;
                if (t.attrIsKnown(SIDE_A, ANGLE_A)) {
                    pairS = t.a;
                    pairA = t.A;
                }
                else if (t.attrIsKnown(SIDE_B, ANGLE_B)) {
                    pairS = t.b;
                    pairA = t.B;
                }
                else if (t.attrIsKnown(SIDE_C, ANGLE_C)) {
                    pairS = t.c;
                    pairA = t.C;
                }
                else {
                    System.out.println("\n\tQUITTING EARLY\n");
                    System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
                    // System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);

                    return res;
                }
                if (code.equals(SIDE_A)) {
                    res = Math.sin(A) * (pairS.length / Math.sin(pairA.angle));
                }
                else if (code.equals(SIDE_B)) {
                    res = Math.sin(B) * (pairS.length / Math.sin(pairA.angle));
                }
                else if (code.equals(SIDE_C)) {
                    res = Math.sin(C) * (pairS.length / Math.sin(pairA.angle));
                }
                else if (code.equals(ANGLE_A)) {
                    // res = Math.toDegrees(Math.asin(a * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(a * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
                    // System.out.println("pairA.angle: " + pairA.angle + "\nMath.sin(pairA): " + Math.sin(pairA.angle) + "\nMath.toDegrees(Math.sin(pairA)): " + Math.toDegrees(Math.sin(pairA.angle)) + "\nMath.toDegrees(Math.sin(Math.toRadians(pairA))): " + Math.toDegrees(Math.sin(Math.toRadians(pairA.angle))) + "\nMath.sin(Math.toRadians(pairA))): " + Math.sin(Math.toRadians(pairA.angle)));
                    // System.out.println("¨Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48): " + Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))));
                    // System.out.println("¨Math.toDegrees(Math.asin((Math.sin(Math.toRadians(pairA))) / 60) * 48)): " + Math.toDegrees(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60)))));
                    // System.out.println("¨Math.toDegrees(Math.asin(Math.toRadians(Math.sin(Math.toRadians(pairA))) / 60) * 48))): " + Math.toDegrees(Math.toRadians(Math.asin((48 * (Math.sin(Math.toRadians(pairA.angle)) / 60))))));
                }
                else if (code.equals(ANGLE_B)) {
                    // res = Math.toDegrees(Math.asin(b * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(b * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
                }
                else if (code.equals(ANGLE_C)) {
                    // res = Math.toDegrees(Math.asin(c * (Math.sin(pairA.angle) / pairS.length)));
                    res = Math.toDegrees(Math.asin(c * (Math.sin(Math.toRadians(pairA.angle)) / pairS.length)));
                }
                System.out.println("\t\t\ta: " + a + "\n\t\t\tb: " + b + "\n\t\t\tc: " + c + "\n\t\t\tA: " + A + "\n\t\t\tB: " + B + "\n\t\t\tC: " + C);
                System.out.println("\tpairS: " + pairS + "\n\tpairA: " + pairA + "\n\tcode: " + code + "\n\tres: " + res);

            }
        }
        else {
            if (code.equals(SIDE_A)) {
                res = t.a.length;
            }
            else if (code.equals(SIDE_B)) {
                res = t.b.length;
            }
            else if (code.equals(SIDE_C)) {
                res = t.c.length;
            }
            else if (code.equals(ANGLE_A)) {
                res = t.A.angle;
            }
            else if (code.equals(ANGLE_B)) {
                res = t.B.angle;
            }
            else if (code.equals(ANGLE_C)) {
                res = t.C.angle;
            }
        }
        return res;
    }

    public void translate(double ax, double ay, double bx, double by, double cx, double cy) {
        this.translateCornerA(ax, ay);
    }

    public void translateCornerA(double ax, double ay) {
        // line a is untouched.

        this.initPoints(ax, ay, bx, by, cx, cy);

//        this.ax = ax;
//        this.ay = ay;
//        this.lineB.setEndX(ax);
//        this.lineB.setEndY(ay);
//        this.lineC.setStartX(ax);
//        this.lineC.setStartY(ay);


//        this.lineB = new Line(lineB.getStartX(), lineB.getStartY(), ax, ay);
//        this.lineC = new Line(ax, ay, lineC.getEndX(), lineC.getEndY());
//        Point2D aStart = new Point2D(this.lineA.getStartX(), this.lineA.getStartY());
//        Point2D aEnd = new Point2D(this.lineA.getEndX(), this.lineA.getEndY());
//        boolean hingeBStart = ((this.intersectionAB.e)) // if not start, then end
    }

    public Point2D centroid() {
        double x = (this.ax + this.bx + this.cx) / 3;
        double y = (this.ay + this.by + this.cy) / 3;
        return new Point2D(x, y);
    }

    public double area() {
        return 0.5 * this.a.length * this.b.length * Math.sin(Math.toRadians(this.C.angle));
    }

    public double perimeter() {
        return this.a.length + this.b.length + this.c.length;
    }
}

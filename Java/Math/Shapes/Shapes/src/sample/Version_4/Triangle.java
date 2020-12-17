package sample.Version_4;

import javafx.collections.ObservableList;
import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polygon;

import java.util.ArrayList;
import java.util.Arrays;

//      All Triangles are created using this form.
//
//                      B
//                    /   \
//                   /     \
//                  a       c
//                 /         \
//                /           \
//               C ---- b ---- A
//
//      Where lowercase letters indicate sides and
//      uppercase letters indicate interior angles.

public class Triangle extends Shape {


    // Codes for sin and cosine law methods
    public static final String SIDE_A = "a";
    public static final String SIDE_B = "b";
    public static final String SIDE_C = "c";
    public static final String ANGLE_A = "A";
    public static final String ANGLE_B = "B";
    public static final String ANGLE_C = "C";

    private String name;
    private Edge a, b, c;
    private Angle A, B, C;
    private Polygon polygon;
//    public double ax, ay, bx, by, cx, cy;
//    public Point2D intersectionAB;
//    public Point2D intersectionAC;
//    public Point2D intersectionBC;
//    public Line lineA;
//    public Line lineB;
//    public Line lineC;


    /*////////////////////
    //   Constructors   //
    ////////////////////*/
    public Triangle(String name, Edge a, Edge b, Edge c, Angle A, Angle B, Angle C) {
        this.name = name;
        this.initEdges(a, b, c);
        this.initAngles(A, B, C);
        this.polygon = createPolygon(a, b, c, Color.DARKGRAY);

        this.solveRemainingTriangle();
    }

    public Triangle(String name, Line a, Line b, Line c) {
        this.name = name;
        this.polygon = createPolygon(a, b, c, Color.DARKGRAY);
        this.initPoints(polygon);

        ArrayList<Edge> sides = calcSides(polygon, a, b, c);
        Edge sideA = sides.get(0);
        Edge sideB = sides.get(1);
        Edge sideC = sides.get(2);
        this.initEdges(sideA, sideB, sideC);

        this.solveRemainingTriangle();
    }

//    // Initialize sides and angles
//    public Triangle(String name, double ax, double ay, double bx, double by, double cx, double cy, Edge a, Edge b, Edge c, Angle A, Angle B, Angle C) {
//        this.name = name;
//        this.initPoints(ax, ay, bx, by, cx, cy);
//        this.initEdges(a, b, c);
//        this.initAngles(A, B, C);
////        this.calcIntersections();
//
//        this.solveRemainingTriangle();
//    }

//    Polygon p = WhiteBoardModel.createTriangle(a, b, c);

//    public void setPolygon(Polygon p) {
//
//    }

    public ArrayList<Edge> calcSides(Polygon polygon, Line a, Line b, Line c) {
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
        Edge edgeA = new Edge("edge a", ax, ay, bx, by);
        Edge edgeB = new Edge("edge b", bx, by, cx, cy);
        Edge edgeC = new Edge("edge c", cx, cy, ax, ay);
        return new ArrayList<>(Arrays.asList(edgeA, edgeB, edgeC));
    }

    public void initPoints(Polygon p) {
        ObservableList<Double> points = p.getPoints();
        double ax = points.get(0);
        double ay = points.get(1);
        double bx = points.get(2);
        double by = points.get(3);
        double cx = points.get(4);
        double cy = points.get(5);
        this.initPoints(ax, ay, bx, by, cx, cy);
    }

    public void initPoints(double ax, double ay, double bx, double by, double cx, double cy) {
//        this.setPointA(ax, ay);
//        this.setPointB(bx, by);
//        this.setPointC(cx, cy);
        this.a = setLine(this.a, new Line(ax, ay, bx, by));
        this.b = setLine(this.b, new Line(bx, by, cx, cy));
        this.c = setLine(this.c, new Line(cx, cy, ax, ay));
//        this.lineB = new Line(bx, by, cx, cy);
//        this.lineC = new Line(cx, cy, ax, ay);
        System.out.println("POINTS");
        System.out.println("(" + ax + ", " + ay + ")" + ", (" + bx + ", " + by + ")" + ", (" + cx + ", " + cy + ")");
        System.out.println("intersection point ab: " + WhiteBoardModel.intersectionPoint(a.getLine(), b.getLine()));
        System.out.println("intersection point ac: " + WhiteBoardModel.intersectionPoint(a.getLine(), c.getLine()));
        System.out.println("intersection point bc: " + WhiteBoardModel.intersectionPoint(b.getLine(), c.getLine()));
//        this.placed = true;
//        this.polygon = this.createPolygon(a, b, c, Color.DARKGRAY);
    }

    public Edge setLine(Edge e, Line l) {
        if (e == null) {
            e = new Edge("", 0, 0, 0, 0);
        }
        e.setLine(l);
        return e;
    }

    public void calcIntersections() {

    }

//    public void setPointA(double ax, double ay) {
//        this.ax = ax;
//        this.ay = ay;
//    }
//
//    public void setPointB(double bx, double by) {
//        this.bx = bx;
//        this.by = by;
//    }
//
//    public void setPointC(double cx, double cy) {
//        this.cx = cx;
//        this.cy = cy;
//    }

    public void initEdges(Edge a, Edge b, Edge c) {
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

    public void initAngles(Angle A, Angle B, Angle C) {
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
//    private void init(String name) {
//        this.name = name;
//        this.placed = false;
//        this.sides = new ArrayList<>();
//        this.angles = new ArrayList<>();
//    }

    public void solveRemainingTriangle() {
        ArrayList<String> toCheck = new ArrayList<>(Arrays.asList(SIDE_A, SIDE_B, SIDE_C, ANGLE_A, ANGLE_B, ANGLE_C));
        boolean loop = true;
        boolean changed = false;
        int i = 0;
        while (loop) {
            String code = toCheck.get(i);
            if (!this.attrIsKnown(code)) {
//                System.out.println("code: " +  code + " is unknown");
                Edge s;
                Angle angle;
                double n;
                if (this.solvable_LOC(code)) {
                    n = Utilities.lawOfCosines(this, code);
                    ;
//                    System.out.println("\n\n\t\tsolvable LOC\n\tcode:" + code + ", n: " + n + "\n");
                    changed = true;
                    switch (i) {
                        case 0:
                            s = new Edge("edge a", b.getX1(), b.getY1(), c.getX1(), c.getY1());
                            this.setSideA(s);
                            break;
                        case 1:
                            s = new Edge("edge b", c.getX1(), c.getY1(), a.getX1(), a.getY1());
                            this.setSideB(s);
                            break;
                        case 2:
                            s = new Edge("edge c", a.getX1(), a.getY1(), b.getX1(), b.getY2());
                            this.setSideC(s);
                            break;
                        case 3:
                            angle = new Angle("angle A", n);
                            this.setAngleA(angle);
                            break;
                        case 4:
                            angle = new Angle("angle B", n);
                            this.setAngleB(angle);
                            break;
                        case 5:
                            angle = new Angle("angle C", n);
                            this.setAngleC(angle);
                            break;
                        default:
                            changed = false;
                    }
                } else if (this.solvable_LOS(code)) {
                    n = Utilities.lawOfSines(this, code);
//                    System.out.println("\n\n\t\tsolvable LOS\n\tcode:" + code + ", n: " + n + "\n");
                    changed = true;
                    switch (i) {
                        case 0:
                            s = new Edge("edge a", b.getX1(), b.getY1(), c.getX1(), c.getY1());
                            this.setSideA(s);
                            break;
                        case 1:
                            s = new Edge("edge b", c.getX1(), c.getY1(), a.getX1(), a.getY1());
                            this.setSideB(s);
                            break;
                        case 2:
                            s = new Edge("edge c", a.getX1(), a.getY1(), b.getX1(), b.getY2());
                            this.setSideC(s);
                            break;
                        case 3:
                            angle = new Angle("angle A", n);
                            this.setAngleA(angle);
                            break;
                        case 4:
                            angle = new Angle("angle B", n);
                            this.setAngleB(angle);
                            break;
                        case 5:
                            angle = new Angle("angle C", n);
                            this.setAngleC(angle);
                            break;
                        default:
                            changed = false;
                    }
                } else {
//                    System.out.println("code: " + code + " is not solvable using LOS or LOC");
                }
                if (this.solvable_AAA()) {
                    changed = true;
                    double angleA, angleB, angleC;
                    angleA = ((this.attrIsKnown(ANGLE_A)) ? this.A.getAngle() : 0);
                    angleB = ((this.attrIsKnown(ANGLE_B)) ? this.B.getAngle() : 0);
                    angleC = ((this.attrIsKnown(ANGLE_C)) ? this.C.getAngle() : 0);
                    n = 180 - (angleA + angleB + angleC);
//                    System.out.println("\n\n\t\tsolvable AAA\n\tcode:" + code + ", n: " + n + "\n");
                    if (!this.attrIsKnown(ANGLE_A)) {
                        angle = new Angle("angle A", n);
                        this.setAngleA(angle);
                    } else if (!this.attrIsKnown(ANGLE_B)) {
                        angle = new Angle("angle B", n);
                        this.setAngleB(angle);
                    } else if (!this.attrIsKnown(ANGLE_C)) {
                        angle = new Angle("angle C", n);
                        this.setAngleC(angle);
                    }
                }
            } else {
//                System.out.println("code: " + code + " is KNOWN");
            }

            i += 1;
            if (!changed && i == toCheck.size()) {
                break;
            }
            i %= toCheck.size();
            if (changed && i == 0) {
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
        } else if (code.equals(SIDE_B)) {
            init |= this.a != null && this.c != null && this.B != null;
        } else if (code.equals(SIDE_C)) {
            init |= this.a != null && this.b != null && this.C != null;
        } else if (code.equals(ANGLE_A) || code.equals(ANGLE_B) || code.equals(ANGLE_C)) {
            init |= this.a != null && this.b != null && this.c != null;
        } else {
            System.out.println("INVALID code");
        }
        return init;
    }

    public boolean solvable_LOS(String code) {
        boolean init = attrIsKnown(code);
        boolean pair = attrIsKnown(SIDE_A, ANGLE_A);// && (!code.equals(SIDE_A) && !code.equals(ANGLE_A));
        pair |= attrIsKnown(SIDE_B, ANGLE_B);// && (!code.equals(SIDE_B) && !code.equals(ANGLE_B));
        pair |= attrIsKnown(SIDE_C, ANGLE_C);// && (!code.equals(SIDE_C) && !code.equals(ANGLE_C));
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
            init |= pair && attrIsKnown(ANGLE_A);
        } else if (code.equals(SIDE_B)) {
            init |= pair && attrIsKnown(ANGLE_B);
        } else if (code.equals(SIDE_C)) {
            init |= pair && attrIsKnown(ANGLE_C);
        } else if (code.equals(ANGLE_A)) {
            init |= pair && attrIsKnown(SIDE_A);
        } else if (code.equals(ANGLE_B)) {
            init |= pair && attrIsKnown(SIDE_B);
        } else if (code.equals(ANGLE_C)) {
            init |= pair && attrIsKnown(SIDE_C);
        } else {
            System.out.println("INVALID code");
        }
        return init;
    }

    public boolean solvable_AAA() {
        int c = 0;
        c += ((attrIsKnown(ANGLE_A)) ? 1 : 0);
        c += ((attrIsKnown(ANGLE_B)) ? 1 : 0);
        c += ((attrIsKnown(ANGLE_C)) ? 1 : 0);
        return c > 1;
    }

    public boolean attrIsKnown(String... codes) {
        boolean known = (codes.length > 0);
        for (int i = 0; i < codes.length; i++) {
            String code = codes[i];
            if (code.equals(SIDE_A)) {
                known &= a != null;
            } else if (code.equals(SIDE_B)) {
                known &= b != null;
            } else if (code.equals(SIDE_C)) {
                known &= c != null;
            } else if (code.equals(ANGLE_A)) {
                known &= A != null;
            } else if (code.equals(ANGLE_B)) {
                known &= B != null;
            } else if (code.equals(ANGLE_C)) {
                known &= C != null;
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

//    public boolean isPlaced() {
//        return this.placed;
//    }

//    public void addSides(Edge... edges) throws InvalidTriangleCreation{
//        for (int i = 0; i < edges.length; i++) {
//            if (edges[i].known()) {
//                throw new InvalidTriangleCreation(2, "edge: <" + sides[i].length + "> is invalid");
//            }
//            this.sides.add(sides[i]);
//            if (this.sides.size() > 3) {
//                throw new InvalidTriangleCreation(3, "");
//            }
//            //int j = i % 3;
//        }
//        for (int i = 0; i < this.sides.size(); i++) {
//            System.out.println("j: " + i);
//            switch (i) {
//                case 0	:	this.a = this.sides.get(i); break;
//                case 1	:	this.b = this.sides.get(i); break;
//                case 2	:	this.c = this.sides.get(i); break;
//                default :	System.out.println("INDEX OUT OF BOUNDS");
//            }
//        }
//        // if (this.sides.size() == 3) {
//        // this.a = this.sides.get(0);
//        // this.b = this.sides.get(1);
//        // this.c = this.sides.get(2);
//        // }
//    }
//
//    public void addAngles(Angle... angles) throws InvalidTriangleCreation{
//        double sum = 0;
//        ArrayList<Edge> sides = new ArrayList<>();
//        for (int i = 0; i < this.angles.size(); i++) {
//            Angle angle = this.angles.get(i);
//            sum += angle.angle;
//            Edge a = angle.a;
//            Edge b = angle.b;
//            if (!sides.contains(a)) {
//                sides.add(a);
//            }
//            if (!sides.contains(b)) {
//                sides.add(b);
//            }
//        }
//        for (int i = 0; i < angles.length; i++) {
//            Angle angle = angles[i];
//            Edge a = angle.a;
//            Edge b = angle.b;
//            if (!sides.contains(a)) {
//                sides.add(a);
//            }
//            if (!sides.contains(b)) {
//                sides.add(b);
//            }
//            if (sides.size() > 3) {
//                throw new InvalidTriangleCreation(6, "");
//            }
//            if (angle.angle <= 0) {
//                throw new InvalidTriangleCreation(4, "Angle: <" + angle.angle + "> is invalid");
//            }
//            sum += angle.angle;
//            this.angles.add(angle);
//            if (this.angles.size() > 3) {
//                throw new InvalidTriangleCreation(5, "");
//            }
//        }
//        if (this.angles.size() == 3) {
//            if (sum != 180) {
//                throw new InvalidTriangleCreation(1, "Angle sum: " + sum + ", is too large");
//            }
//            // this.A = this.angles.get(0);
//            // this.B = this.angles.get(1);
//            // this.C = this.angles.get(2);
//        }
//        for (int i = 0; i < this.angles.size(); i++) {
//            System.out.println("j: " + i);
//            switch (i) {
//                case 0	:	this.A = this.angles.get(i); break;
//                case 1	:	this.B = this.angles.get(i); break;
//                case 2	:	this.C = this.angles.get(i); break;
//                default :	System.out.println("INDEX OUT OF BOUNDS");
//            }
//        }
//    }

    public void setSideA(Edge a) {
        this.a = a;
    }

    public void setSideB(Edge b) {
        this.b = b;
    }

    public void setSideC(Edge c) {
        this.c = c;
    }

    public void setAngleA(Angle A) {
        this.A = A;
    }

    public void setAngleB(Angle B) {
        this.B = B;
    }

    public void setAngleC(Angle C) {
        this.C = C;
    }

    public Edge getSideA() {
        return a;
    }

    public Edge getSideB() {
        return b;
    }

    public Edge getSideC() {
        return c;
    }

    public Angle getAngleA() {
        return A;
    }

    public Angle getAngleB() {
        return B;
    }

    public Angle getAngleC() {
        return C;
    }

    public String getBorder() {
        StringBuilder res = new StringBuilder("\n");
        for (int i = 0; i < 50; i++) {
            res.append("#");
        }
        return res + "\n";
    }

//    public void translate(double ax, double ay, double bx, double by, double cx, double cy) {
//        this.translateCornerA(ax, ay);
//    }

    public void translateCornerA(double ax, double ay) {
        // line a is untouched.

        b.setX2(ax);
        b.setY2(ay);
        c.setX1(ax);
        c.setY1(ay);

//        this.initPoints(ax, ay, bx, by, cx, cy);

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

    public void translateCornerB(double bx, double by) {
        // line b is untouched.
        a.setX1(bx);
        a.setY1(by);
        c.setX2(bx);
        c.setY2(by);
    }

    public void translateCornerC(double cx, double cy) {
        // line c is untouched.
        a.setX2(cx);
        a.setY2(cy);
        b.setX1(cx);
        b.setY1(cy);
    }

    /**
     * Get the edge with the largest length, indicating the base of the triangle.
     *
     * @return base edge.
     */
    public Edge getBase() {
        Edge e = ((a.getLength() >= b.getLength()) ? a : b);
        return ((e.getLength() >= c.getLength()) ? e : c);
    }

    /**
     * Calculate the center point of the triangle.
     *
     * @return Point2d marking the center.
     */
    public Point2D centroid() {
        double x = (this.a.getX1() + this.b.getX1() + this.c.getX1()) / 3;
        double y = (this.a.getY1() + this.b.getY1() + this.c.getY1()) / 3;
        return new Point2D(x, y);
    }

    /**
     * Calculate the area of the triangle.
     *
     * @return area.
     */
    public double area() {
        return 0.5 * this.a.getLength() * this.b.getLength() * Math.sin(Math.toRadians(this.C.getAngle()));
    }

    /**
     * Calculate the perimeter of the triangle.
     *
     * @return perimeter
     */
    public double perimeter() {
        return this.a.getLength() + this.b.getLength() + this.c.getLength();
    }

    public Polygon getPolygon() {
        return polygon;
    }

    public static Polygon createPolygon(Edge a, Edge b, Edge c, Color col) {
        return createPolygon(a.getLine(), b.getLine(), c.getLine(), col);
    }

    public static Polygon createPolygon(Line a, Line b, Line c, Color col) {
        Point2D intersectionAB = WhiteBoardModel.intersectionPoint(a, b);
        Point2D intersectionAC = WhiteBoardModel.intersectionPoint(a, c);
        Point2D intersectionBC = WhiteBoardModel.intersectionPoint(b, c);
//        System.out.println("a: " + a);
//        System.out.println("b: " + b);
//        System.out.println("c: " + c);
//        assert intersectionAB != null : "AB is NULL {" + intersectionAB + "}";
//        assert intersectionAC != null : "AC is NULL {" + intersectionAC + "}";
//        assert intersectionBC != null : "BC is NULL {" + intersectionBC + "}";
        Polygon p = new Polygon(intersectionAB.getX(), intersectionAB.getY(), intersectionAC.getX(), intersectionAC.getY(), intersectionBC.getX(), intersectionBC.getY());
        p.setFill(col);
        return p;
    }


    public String toString() {
        //return "\n" + this.name + "\nsides: " + this.sides + "\nAngles: " + this.angles;
        String res = getBorder() + "Name: " + name;
        res += "\na: " + ((a == null) ? "null" : a);
        res += "\nb: " + ((b == null) ? "null" : b);
        res += "\nc: " + ((c == null) ? "null" : c);
        res += "\nA: " + ((A == null) ? "null" : A);
        res += "\nB: " + ((B == null) ? "null" : B);
        res += "\nC: " + ((C == null) ? "null" : C);
        res += "\n(ax, ay): (" + a.getX1() + ", " + a.getY1() + ")";
        res += "\n(bx, by): (" + b.getX1() + ", " + b.getY1() + ")";
        res += "\n(cx, cy): (" + c.getX1() + ", " + c.getY1() + ")";
        res += "\narea: " + ((polygon == null) ? "null" : area());
        res += "\nperimeter: " + ((polygon == null) ? "null" : perimeter());
        return res + getBorder();
    }
}

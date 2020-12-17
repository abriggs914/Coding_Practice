package sample;

import javafx.geometry.Point2D;
import sample.Version_3.Triangle_v3;

public class Vector_v3 {

    public boolean pointsSet;
    public double x1;
    public double y1;
    public double x2;
    public double y2;
    public double angle;
    public double speed;
    public Vector_v3 xComponent;
    public Vector_v3 yComponent;
    public Point2D p1;
    public Point2D p2;

    public Vector_v3(double x1, double y1, double x2, double y2, double speed, double angle) {
        System.out.println("\t\tVector(double x1, double y1, double x2, double y2, double speed, double angle)");
//        this.setPoints(x1, y1, x2, y2);
//        this.speed = speed;
//        this.angle = angle;
        this.init(x1, y1, x2, y2, speed, angle);
    }

    public Vector_v3(double speed, double angle) {
        System.out.println("\tVector(double speed, double angle)");
        if (angle > 90 && speed > 0) {
            speed *= -1;
        }
        else if (speed < 0) {
            speed *= -1;
        }
        double[] components = getAxisComponents();
        double x = components[0];
        double y = components[1];
        this.init(0, 0, x, y, speed, angle);
//        new Vector(0, 0, x, y, speed, angle);


    }

    public Vector_v3(double x1, double y1, double x2, double y2) {
        System.out.println("\tVector(double x1, double y1, double x2, double y2)");
        double speed = this.calcSpeed(x1, y1, x2, y2);
        double angle = this.calcAngle(x1, y1, x2, y2);
        this.init(x1, y1, x2, y2, speed, angle);
//        new Vector(x1, y1, x2, y2, speed, angle);
    }

    public Vector_v3(Point2D pt) {
        System.out.println("Vector(Point2D)");
        this.initWithPoints(0, 0, pt.getX(), pt.getY());
//        new Vector(0, 0, pt.getX(), pt.getY());
    }

    public void init(double x1, double y1, double x2, double y2, double speed, double angle) {
        this.setPoints(x1, y1, x2, y2);
        this.speed = speed;
        this.angle = angle;
    }

    public void initWithPoints(double x1, double y1, double x2, double y2) {
        double speed = this.calcSpeed(x1, y1, x2, y2);
        double angle = this.calcAngle(x1, y1, x2, y2);
        this.init(x1, y1, x2, y2, speed, angle);
    }

    public void setPoints(double x1, double y1, double x2, double y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
        this.p1 = new Point2D(x1, y1);
        this.p2 = new Point2D(x2, y2);
    }

    public double calcSpeed(double x1, double y1, double x2, double y2) {
        return new Point2D(x1, y1).distance(new Point2D(x2, y2));
    }

    public double calcAngle(double x1, double y1, double x2, double y2) {
        double xd = Math.abs(x2 - x1);
        double yd = Math.abs(y2 - y1);
        double h = Math.sqrt((yd * yd) + (xd * xd));
        sample.Side_v3 a = new sample.Side_v3("side a", xd);
        sample.Side_v3 b = new sample.Side_v3("side b", yd);
        sample.Side_v3 c = new sample.Side_v3("side c", h);
        Triangle_v3 t = new Triangle_v3("", a, b, c, null, null, null);
        t.solveRemainingTriangle();
        return t.B.angle;
    }

    public static Vector_v3 combineXYComponents(double velX, double velY) {
        double angle = Math.toDegrees(Math.atan(Math.abs(velY / velX)));
        double speed = Math.sqrt((velX * velX) + (velY * velY));
        System.out.println("\tvelX: " + velX + ", velY: " + velY + ", speed: " + speed + ", angle: " + angle);
        if (velY < 0) {
            angle += 180;
        }

        if (velX > 0 && velY < 0) {
            angle += 90;
        }
        else if (velX < 0 && velY > 0) {
            angle += 90;
        }

        if (angle > 90 && speed > 0) {
            speed *= -1;
        }
        System.out.println("\tspeed: " + speed + ", angle: " + angle);
        return new Vector_v3(speed, angle);
    }

    /**
     * Calculate the individual x and y component vectors from a
     * given speed vector and the angle from the origin of direction.
     * @return Vector array {x-component, y-component}
     */
    public Vector_v3[] calcAxisComponents() {
        double speed = Math.abs(this.speed);
        double angle = Math.toRadians(this.angle);
        double xSpeed = Math.cos(angle) * speed;
        double ySpeed = Math.sin(angle) * speed;
        double xAngle = 0, yAngle = 90;
        if (xSpeed < 0) {
            xAngle = 180;
        }
        if (ySpeed < 0) {
            yAngle = 270;
        }
//        System.out.println("ySpeed: " + ySpeed + ", xSpeed: " + xSpeed + ", yAngle: " + yAngle + ", xAngle: " + xAngle);
        Vector_v3 xVector = new Vector_v3(xSpeed, xAngle);
        Vector_v3 yVector = new Vector_v3(ySpeed, yAngle);
        return new Vector_v3[] {xVector, yVector};
    }

    public double[] getAxisComponents() {
        double speed = Math.abs(this.speed);
        double angle = Math.toRadians(this.angle);
        double xSpeed = Math.cos(angle) * speed;
        double ySpeed = Math.sin(angle) * speed;
        return new double[] {xSpeed, ySpeed};
    }

    private void setComponents() {
        Vector_v3[] components = this.calcAxisComponents();
        this.xComponent = components[0];
        this.yComponent = components[1];
    }

    public Vector_v3 getXComponent() {
        if (this.xComponent == null || this.yComponent == null) {
            this.setComponents();
        }
        return xComponent;
    }

    public Vector_v3 getYComponent() {
        if (this.xComponent == null || this.yComponent == null) {
            this.setComponents();
        }
        return yComponent;
    }

    @Override
    public String toString() {
        String res =  speed + " m/s @ " + sample.Utilities_v3.twoDecimal(angle) + " degrees.";
        res += "\n(x1, y1): (" + x1 + ", " + y1 + ")" + "\n(x2, y2): (" + x2 + ", " + y2 + ")";
        res += "\np1: " + p1;
        res += "\np2: " + p2;
        return res;
    }

    // compute the angle of the right_angled triangle formed from a
    // given center point and cordinates x and y.
    // Quadrants are specified to the 2D coordinate system where right
    // is positive x direction and down is positive y direction.
    public static double computeAngle(double cx, double cy, double x, double y) {
        double opp = Math.abs(y - cy);
        double adj = Math.abs(x - cx);
        if (adj == 0) {
            adj = 1;
        }
        double angle = Math.toDegrees(Math.atan(opp / adj));
        double deltaX = x - cx;
        double deltaY = y - cy;
        // Quadrant 2 - Cartesian 3
        if (deltaX < 0 && deltaY >= 0){
            angle = 180 - angle; //(90 - angle) + 90;
        }
	    // Quadrant 3 - Cartesian 2
        if (deltaY < 0 && deltaX < 0){
            angle += 180;
        }
        // Quadrant 4 - Cartesian 1
        if (deltaY < 0 && deltaX >= 0){
            angle = 360 - angle; //(90 - angle) + 270;
        }
        return angle;
    }

    public static int cartesianQuadrant(Vector_v3 v) {
          double angle = computeAngle(v.p1.getX(), v.p1.getY(), v.p2.getX(), v.p2.getY());
          System.out.println("\t\tangle: " + angle);
//        double angle = v.angle;
          if (angle > 0 && angle <= 90) {
              return 1;
          }
          else if (angle <= 180) {
              return 2;
          }
          else if (angle <= 270) {
              return 3;
          }
          else {
              return 4;
          }
    }
}

package sample;

public class Vector {

    private double angle;
    private double speed;
    private Vector xComponent;
    private Vector yComponent;

    public Vector() {

    }

    public Vector(double speed, double angle) {
        if (angle > 90 && speed > 0) {
            speed *= -1;
        }
        else if (speed < 0) {
            this.speed *= -1;
        }
        this.speed = speed;
        this.angle = angle;
    }

    /**
     * Calculate the individual x and y component vectors from a
     * given speed vector and the angle from the origin of direction.
     * @return Vector array {x-component, y-component}
     */
    public Vector[] calcAxisComponents() {
        double speed = Math.abs(this.getSpeed());
        double angle = Math.toRadians(this.getAngle());
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
        Vector xVector = new Vector(xSpeed, xAngle);
        Vector yVector = new Vector(ySpeed, yAngle);
        return new Vector[] {xVector, yVector};
    }

    public double getAngle() {
        return angle;
    }

    public void setAngle(double angle) {
        angle = angle % 360;
        if (angle > 90 && speed > 0) {
            this.speed *= -1;
        }
        else if (angle <= 90 && speed < 0) {
            this.speed *= -1;
        }
        this.angle = angle;
    }

    public double getSpeed() {
        return speed;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public double[] getAxisComponents() {
        double speed = Math.abs(this.getSpeed());
        double angle = Math.toRadians(this.getAngle());
        double xSpeed = Math.cos(angle) * speed;
        double ySpeed = Math.sin(angle) * speed;
        return new double[] {xSpeed, ySpeed};
    }

    public static Vector combineXYComponents(double velX, double velY) {
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
        return new Vector(speed, angle);
    }

    private void setComponents() {
        Vector[] components = this.calcAxisComponents();
        this.xComponent = components[0];
        this.yComponent = components[1];
    }

    public Vector getXComponent() {
        if (this.xComponent == null || this.yComponent == null) {
            this.setComponents();
        }
        return xComponent;
    }

    public Vector getYComponent() {
        if (this.xComponent == null || this.yComponent == null) {
            this.setComponents();
        }
        return yComponent;
    }

    public static Vector combineComponents(Vector xVector, Vector yVector) {
        double velX = xVector.getSpeed();
        double velY = yVector.getSpeed();
//        double degX = Math.toRadians(xVector.getAngle());
//        double degY = Math.toRadians(yVector.getAngle());
        double angle = Math.toDegrees(Math.atan(Math.abs(velY / velX)));
        double speed = Math.sqrt((velX * velX) + (velY * velY));
        if (angle > 90 && speed > 0) {
            speed *= -1;
        }
        return new Vector(speed, angle);
    }

    public static Vector combineSpeeds(double velX, double velY) {
        double angle = Math.toDegrees(Math.atan(Math.abs(velY / velX)));
        double speed = Math.sqrt((velX * velX) + (velY * velY));
        if (angle > 90 && speed > 0) {
            speed *= -1;
        }
        return new Vector(speed, angle);
    }

    public static Vector addAngle(Vector v, double angle) {
        double a = ((v.getAngle()) + angle) % 360;
        double s = v.getSpeed();
        return new Vector(s, a);
    }


    public void bounceXDirection() {
//        this.setSpeed(-1 * speed);
        this.setAngle(((360 - angle) + 180) % 360);
        setComponents();
    }


    public void bounceYDirection() {
//        this.setSpeed(-1 * speed);
//        double axisAngle = 180;
        this.setAngle(360 - angle);
        setComponents();
    }

    public void flipDirection() {
        this.setSpeed(-1 * speed);
        this.setAngle((180 + angle) % 360);
    }

    @Override
    public String toString() {
        return speed + " m/s @ " + Utilities.twoDecimal(angle) + " degrees.";
    }
}

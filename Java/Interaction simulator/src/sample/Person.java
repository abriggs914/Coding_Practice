package sample;

import javafx.scene.Group;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.text.Text;

import java.util.ArrayList;
import java.util.Date;

public class Person {

    private static Color HEALTHY_COLOR = Color.rgb(4, 196, 46);
    private static Color CURED_CIRCLE_COLOR = Color.rgb(4, 180, 196);
    private static Color CURED_BORDER_COLOR = Color.rgb(245, 219, 22);
    private static Color DEAD_COLOR = Color.DARKGRAY;

    private String idString;
    private int idNumber;
    private boolean isMale;
//    private int directionDegree;
//    private double directionSpeed;
    private Vector directionVector;
    private boolean isInfected;
    private boolean isAlive;
    private boolean isMoveable;
    private boolean isCured;
    private Disease disease;
    private Circle circle;
    private Group stackPane;
    private ArrayList<Collision> collisions;
    private double secondsInfected;
    private double lifeTime;
    private double lifeSpan;
    private double ageAtDeath;
    private double mass;
    private double layoutX;
    private double layoutY;
    private Date simStart;
    private Date simEnd;
    private String causeOfDeath;
    private ArrayList<Line> path;
    private ArrayList<Disease> diseaseHistory;

    public Person(String idString, int idNumber, boolean isMale, double age, double lifeSpan, double mass, double layoutX, double layoutY) {
        this.simStart = Model.getCurrentDate();
        this.idString = idString;
        this.idNumber = idNumber;
        this.isMale = isMale;
        this.lifeTime = age;
        this.lifeSpan = lifeSpan;
        this.mass = mass;
        this.layoutX = layoutX;
        this.layoutY = layoutY;
        this.isAlive = true;
        this.isCured = false;
        this.collisions = new ArrayList<>();
        this.path = new ArrayList<>();
        this.diseaseHistory = new ArrayList<>();
        this.secondsInfected = 0;
    }

    public Circle getCircle() {
        return circle;
    }

    public Group getCircleStack() {
        return stackPane;
    }

    public void updateCircle() {
        this.circle.setStrokeWidth(2);
        if (this.isInfected) {
            Color infectedColor = disease.getColor();
            this.circle.setStroke(infectedColor);
            this.circle.setFill(infectedColor);
        }
        if (!this.isAlive) {
            this.circle.setStroke(DEAD_COLOR);
            this.circle.setFill(DEAD_COLOR);
        }
        else if (this.isCured) {
            this.circle.setStroke(CURED_BORDER_COLOR);
            this.circle.setFill(CURED_CIRCLE_COLOR);
        }
        else if (!this.isInfected){
            this.circle.setStroke(HEALTHY_COLOR);
            this.circle.setFill(HEALTHY_COLOR);
        }
    }

    public void setCircle(int diameter, double x, double y) {
        this.layoutX = x;
        this.layoutY = y;
        this.circle = new Circle(diameter);
        this.stackPane = new Group();
        this.circle.setStrokeWidth(2);
        if (this.isInfected) {
            Color infectedColor = disease.getColor();
            this.circle.setStroke(infectedColor);
            this.circle.setFill(infectedColor);
        }
        if (!this.isAlive) {
            this.circle.setStroke(DEAD_COLOR);
            this.circle.setFill(DEAD_COLOR);
        }
        else if (this.isCured) {
            this.circle.setStroke(CURED_BORDER_COLOR);
            this.circle.setFill(CURED_CIRCLE_COLOR);
        }
        else if (!this.isInfected){
            this.circle.setStroke(HEALTHY_COLOR);
            this.circle.setFill(HEALTHY_COLOR);
        }
        this.circle.setCenterX(x);
        this.circle.setCenterY(y);

        this.stackPane.setLayoutX(circle.getLayoutX());
        this.stackPane.setLayoutY(circle.getLayoutY());

        this.stackPane.getChildren().add(circle);
        if (Model.isShowDirectionVectors()) {
            Group g = getDirectionVectorLine();
            this.stackPane.getChildren().add(g);
        }
        if (Model.isShowPersonIds()) {
            Text t = getIdTextLabel();
            this.stackPane.getChildren().add(t);
        }
    }

    public String getIdString() {
        return idString;
    }

    public int getIdNumber() {
        return idNumber;
    }

    public Text getIdTextLabel() {
        Text t = new Text(Integer.toString(idNumber));
        t.setLayoutX(this.circle.getCenterX() - (this.circle.getRadius() / 2));
        t.setLayoutY(this.circle.getCenterY() + (this.circle.getRadius() / 2));
        return t;
    }

    public Group getDirectionVectorLine() {
        Vector[] components = directionVector.calcAxisComponents();
        double xSpeed = components[0].getSpeed();
        double ySpeed = components[1].getSpeed();
        double xAngle = components[0].getAngle();
        double yAngle = components[1].getAngle();
        int scalar = 2;
        Line l = new Line(
                circle.getCenterX(),
                circle.getCenterY(),
                circle.getCenterX() + (scalar * xSpeed),
                circle.getCenterY() + (scalar * ySpeed)
        );

        double angle = directionVector.getAngle();
        double speed = directionVector.getSpeed();
        Vector upVector = new Vector((0.35 * speed), (((angle + 180) % 360) + 135));
        Vector downVector = new Vector((0.35 * speed), (((angle + 180) % 360) + 225));
        Vector[] upComponents = upVector.calcAxisComponents();
        Vector[] downComponents = downVector.calcAxisComponents();
        Line up = new Line(
                circle.getCenterX() + (scalar * xSpeed),
                circle.getCenterY() + (scalar * ySpeed),
                (circle.getCenterX() + (scalar * xSpeed)) - (scalar * upComponents[0].getSpeed()),
                (circle.getCenterY() + (scalar * ySpeed)) - (scalar * upComponents[1].getSpeed()));
        Line down = new Line(
                circle.getCenterX() + (scalar * xSpeed),
                circle.getCenterY() + (scalar * ySpeed),
                (circle.getCenterX() + (scalar * xSpeed)) - (scalar * downComponents[0].getSpeed()),
                (circle.getCenterY() + (scalar * ySpeed)) - (scalar * downComponents[1].getSpeed()));

        Line x = new Line(
                circle.getCenterX() - (scalar * 12),
                circle.getCenterY(),
                circle.getCenterX() + (scalar * 12),
                circle.getCenterY());
        Line y = new Line(
                circle.getCenterX(),
                circle.getCenterY() - (scalar * 12),
                circle.getCenterX(),
                circle.getCenterY() + (scalar * 12));
        x.setStrokeWidth(1.0);
        y.setStrokeWidth(1.0);
        x.setFill(Color.GREEN);
        y.setFill(Color.GREEN);
        l.setStroke(Color.ORANGE);
        up.setStroke(Color.BLUE);
        down.setStroke(Color.BLUE);
        l.setStrokeWidth(2.0);
        up.setStrokeWidth(2.0);
        down.setStrokeWidth(2.0);

        Group g = new Group(x, y, l, up, down);
        return g;
    }

    public Vector getDirectionVector() {
        return directionVector;
    }

    public void setDirectionVector(Vector directionVector) {
        this.directionVector = new Vector(directionVector.getSpeed(), directionVector.getAngle());
    }

    public boolean isInfected() {
        return isInfected;
    }

    public void setInfected(boolean infected) {
        this.isInfected = infected;
    }

    public Disease getDisease() {
        return disease;
    }

    public void setDisease(Disease disease) {
        this.disease = disease;
    }

    public ArrayList<Collision> getCollisions() {
        return collisions;
    }

    public void setCollisions(ArrayList<Collision> collisions) {
        this.collisions = collisions;
    }

    public double getMass() {
        return mass;
    }

    public double getLifeTime() {
        return lifeTime;
    }

    public void setLifeTime(double lifeTime) {
        this.lifeTime = lifeTime;
    }

    public double getSecondsInfected() {
        return secondsInfected;
    }

    public void setSecondsInfected(double secondsInfected) {
        this.secondsInfected = secondsInfected;
    }

    public boolean isAlive() {
        return isAlive;
    }

    public void setAlive(boolean alive) {
        isAlive = alive;
        if (!alive) {
            this.setMoveable(false);
        }
    }

    public boolean isMoveable() {
        return isMoveable;
    }

    public void setMoveable(boolean moveable) {
        this.isMoveable = moveable;
    }

    public boolean isCured() {
        return isCured;
    }

    public void setCured(boolean cured) {
        this.isCured = cured;
    }

    public ArrayList<Line> getPath() {
        return path;
    }

    public void addPath(Line line) {
        this.path.add(line);
    }

    public void setCoordinates(double x, double y) {
        this.layoutX = x;
        this.layoutY = y;
        this.circle.setCenterX(x);
        this.circle.setCenterY(y);
        this.stackPane.getChildren().clear();
        this.stackPane.setLayoutX(circle.getLayoutX());
        this.stackPane.setLayoutY(circle.getLayoutY());

        this.stackPane.getChildren().add(circle);
        if (Model.isShowDirectionVectors()) {
            Group g = getDirectionVectorLine();
            this.stackPane.getChildren().add(g);
        }
        if (Model.isShowPersonIds()) {
            Text t = getIdTextLabel();
            this.stackPane.getChildren().add(t);
        }
    }

    public double getLayoutX() {
        return layoutX;
    }

    public void setLayoutX(double layoutX) {
        this.layoutX = layoutX;
    }

    public double getLayoutY() {
        return layoutY;
    }

    public void setLayoutY(double layoutY) {
        this.layoutY = layoutY;
    }

    public double getLifeSpan() {
        return lifeSpan;
    }

    public void setLifeSpan(double lifeSpan) {
        this.lifeSpan = lifeSpan;
    }

    public void age() {
        if (isAlive) {
            this.lifeTime += 1.0;
            if (isInfected) {
                this.secondsInfected += 1.0;
                checkInfectedSurvival();
                if (this.secondsInfected > this.disease.getInfectiousPeriod()) {
                    Model.setCured(this);
                }
            }
            checkNaturalCauses();
        }
    }

    public void onDeath(String cause) {
        setAlive(false);
        setCauseOfDeath(cause);
        setSimEnd(Model.getCurrentDate());
        Model.setDeath(this);
    }

    private void checkInfectedSurvival() {
        double probDeath = disease.getMortalityRate();
        double chance = Utilities.randomDoubleInRange(0, 101);
        boolean survive = chance > probDeath;
        if (!survive) {
            onDeath(disease.getName());
        }
    }

    private void checkNaturalCauses() {
        if (this.lifeTime >= this.lifeSpan) {
            boolean survive = Utilities.calcSurvival(this);
            if (!survive) {
                onDeath("Natural causes");
            }
        }
    }

    public boolean isMale() {
        return isMale;
    }

    public void setMale(boolean male) {
        this.isMale = male;
    }

    public double getAgeAtDeath() {
        return ageAtDeath;
    }

    public void setAgeAtDeath(double ageAtDeath) {
        this.ageAtDeath = ageAtDeath;
    }

    public Date getSimStart() {
        return simStart;
    }

    public void setSimStart(Date simStart) {
        this.simStart = simStart;
    }

    public Date getSimEnd() {
        return simEnd;
    }

    public void setSimEnd(Date simEnd) {
        this.simEnd = simEnd;
    }

    public String getCauseOfDeath() {
        return causeOfDeath;
    }

    public void setCauseOfDeath(String causeOfDeath) {
        this.causeOfDeath = causeOfDeath;
    }

    public void addDiseaseHistory() {
        this.diseaseHistory.add(this.disease);
    }

    @Override
    public String toString() {
        return idString + " (" + lifeTime + " / " + lifeSpan + ")"; //, v:" + directionVector;
    }
}

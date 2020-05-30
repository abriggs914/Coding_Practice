package sample;

import javafx.animation.*;
import javafx.event.ActionEvent;
import javafx.geometry.Bounds;
import javafx.scene.Group;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.util.Duration;

import java.util.ArrayList;
import java.util.Date;

public class Model {

    // Default Vars
    private static final Date TODAY = DateHandler.getToday();
    private static final double AVG_PERSON_MASS = 10.0;
    private static final int AVG_PERSON_DIAMETER = 10;
    private static final double MIN_PERSON_SPEED = 10;
    private static final double MAX_PERSON_SPEED = 25.0;
    private static final double AVG_PERSON_AGE = 41;
    private static final double AVG_LIFE_EXPECTANCY = 70;
    private static final boolean SHOW_PERSON_IDS = true;
    private static final boolean SHOW_DIRECTION_VECTORS = false;
    private static final boolean PERFORM_PERSON_COLLISIONS = false;

    // UI change-able vars
    private static int numPeopleStart;
    private static int numHealthyStart;
    private static int numInfectedStart;
    private static double daysPerSecond;
    private static Disease currentDisease;

    // Simulation tracked vars
    private static PandemicHistory pandemicHistory;
    private static Timeline timeline;
    private static Date startDate;
    private static Date currentDate;
    private static int numCuredCount;
    private static int numPeopleCount;
    private static int numHealthyCount;
    private static int numInfectedCount;
    private static int numDeathCount;
    private static int numCollisionCount;
    private static ArrayList<Person> population;
    private static ArrayList<Collision> populationCollisions;
    private static ArrayList<Person> infectedPopulation;
    private static ArrayList<Person> passedPopulation;
    private static ArrayList<Person> curedPopulation;
    private static ArrayList<Person> caseHistoryPopulation;
    private static Bounds interactionViewBounds;

    private static ArrayList<Person> infectedTodayPopulation;
    private static ArrayList<Person> curedTodayPopulation;
    private static ArrayList<Person> passedTodayPopulation;

    public static void init() {
        startDate = TODAY;
        currentDate = startDate;
        currentDisease = Disease.CORONAVIRUS;
        numCuredCount = 0;
        numPeopleCount = 0;
        numHealthyStart = numPeopleStart - numInfectedStart;
        numHealthyCount = numHealthyStart;
        numInfectedCount = 0;
        numDeathCount = 0;
        population = new ArrayList<>();
        populationCollisions = new ArrayList<>();
        infectedPopulation = new ArrayList<>();
        passedPopulation = new ArrayList<>();
        curedPopulation = new ArrayList<>();
        caseHistoryPopulation = new ArrayList<>();

        if (daysPerSecond == 0) {
            daysPerSecond = 1;
        }
//        double nSec = 1 / daysPerSecond;
//        if (nSec < 1) {
//            nSec = 1 / nSec;
//        }
//        else {
//            nSec =
//        }
        timeline = createTimeLine();
    }

    public static Timeline oneFrameTimeLine() {
        double t = (1 / daysPerSecond);
        timeline = new Timeline(new KeyFrame(Duration.seconds(t),
                event -> {
                    currentDate = DateHandler.nextDate(currentDate);
                    System.out.println(String.format("this is called every %d seconds on UI thread: ", t) + DateHandler.getDateString(currentDate));
                    View.setTimeView(currentDate);
                    double x1 = 0; //View.getInteractionView().getLayoutX() + 10;
                    double y1 = 0; //View.getInteractionView().getLayoutY() + 10;
                    double x2 = View.getInteractionView().getWidth(); //View.getInteractionView().getWidth() - 10;
                    double y2 = View.getInteractionView().getHeight(); //View.getInteractionView().getHeight() - 10;
                    for (Person p : population) {
                        if (!p.isMoveable()) {
                            continue;
                        }
                        //Creating Translate Transition
                        TranslateTransition translateTransition = new TranslateTransition();

                        //Setting the node for the transition
                        Group circle = p.getCircleStack();
                        translateTransition.setNode(circle);

                        //Setting the value of the transition along the x axis.
                        Vector xComponent = p.getDirectionVector().getXComponent();
                        Vector yComponent = p.getDirectionVector().getYComponent();
                        double speedX = xComponent.getSpeed();
                        double speedY = yComponent.getSpeed();
                        double originX = p.getCircle().getCenterX();
                        double originY = p.getCircle().getCenterY();
                        double distanceX = Math.min(originX - x1, x2 - originX);
                        double distanceY = Math.min(originY - y1, y2 - originY);
                        boolean bounceXAxis = distanceX < speedX;
                        boolean bounceYAxis = distanceY < speedY;
                        double bounceDistanceX = Math.max(0, speedX - distanceX);
                        double bounceDistanceY = Math.max(0, speedY - distanceY);
                        double totalTime = (1 / daysPerSecond) * 1000;
                        double bounceTime = 0;
//                        System.out.println("\n\n\tBEFORE " + p + "\nspeedX: " + speedX + ", speedY: " + speedY + "\noriginX: " + originX + ", originY: " + originY + "\nx1: " + x1 + ", y1: " + y1 + "\nx2: " + x2 + ", y2: " + y2 + "\ndistanceX: " + distanceX + ", distanceY: " + distanceY + "\nbounceXAxis: " + bounceXAxis + ", bounceYAxis: " + bounceYAxis + "\nbounceDistanceX: " + bounceDistanceX + ", bounceDistanceY: " + bounceDistanceY + "\ntotalTime: " + totalTime + ", bounceTime: " + bounceTime);
                        if (bounceXAxis) {
                            double bouncePorportion = bounceDistanceX / (speedX + bounceDistanceX);
//                            System.out.print("\nXbouncePorportion " + bouncePorportion);
                            bounceTime = bouncePorportion * totalTime;
//                            totalTime -= bounceTime;
//                            speedX = distanceX;
                            Vector vX = new Vector(-1 * speedX, p.getDirectionVector().getXComponent().getAngle());
                            Vector vY = p.getDirectionVector().getYComponent();
                            Vector VT = Vector.combineComponents(vX, vY);
                            p.setDirectionVector(VT);
                            speedX = p.getDirectionVector().getXComponent().getSpeed();
                        }

                        if (bounceYAxis) {
                            double bouncePorportion = bounceDistanceY / (speedY + bounceDistanceY);
//                            System.out.println(", YbouncePorportion " + bouncePorportion);
                            bounceTime = bouncePorportion * totalTime;
//                            totalTime -= bounceTime;
//                            speedY = distanceY;
                            Vector vX = p.getDirectionVector().getXComponent();
                            Vector vY = new Vector(-1 * speedY, p.getDirectionVector().getYComponent().getAngle());
                            Vector VT = Vector.combineComponents(vX, vY);
                            p.setDirectionVector(VT);
                            speedY = p.getDirectionVector().getYComponent().getSpeed();
                        }
//                        System.out.println("\n\n\tAFTER " + p + "\nspeedX: " + speedX + ", speedY: " + speedY + "\noriginX: " + originX + ", originY: " + originY + "\ndistanceX: " + distanceX + ", distanceY: " + distanceY + "\nbounceXAxis: " + bounceXAxis + ", bounceYAxis: " + bounceYAxis + "\nbounceDistanceX: " + bounceDistanceX + ", bounceDistanceY: " + bounceDistanceY + "\ntotalTime: " + totalTime + ", bounceTime: " + bounceTime);
                        translateTransition.setByX(speedX);
                        translateTransition.setByY(speedY);
                        translateTransition.setDuration(Duration.millis(totalTime));
                        translateTransition.setAutoReverse(false);
                        translateTransition.play();
                    }
                }
        ));
        return null;
    }

    public static Timeline createTimeLine() {
        double t = (1 / daysPerSecond);
        infectedTodayPopulation = new ArrayList<>();
        curedTodayPopulation = new ArrayList<>();
        passedTodayPopulation = new ArrayList<>();
        timeline = new Timeline(new KeyFrame(Duration.seconds(t),
                (ActionEvent event) -> {

                    if (getAliveAndInfectedPopulation().size() == 0) {
                        stopSim();
                        return;
                    }

                    ParallelTransition parallelTransition = new ParallelTransition();

                    currentDate = DateHandler.nextDate(currentDate);
                    System.out.println(String.format("this is called every %f seconds on UI thread: ", t) + DateHandler.getDateString(currentDate));
                    View.setTimeView(currentDate);
                    ArrayList<Person> checkedPopulation = new ArrayList<>();
                    for (Person p : population) {
//                        System.out.println("\tperson: " + p);
                        if (!p.isMoveable()) {
                            continue;
                        }

                        Circle c = p.getCircle();
                        double cX = c.getCenterX();
                        double cY = c.getCenterY();
                        double x1 = interactionViewBounds.getMinX() + c.getRadius(); //View.getInteractionView().getLayoutX() + 10;
                        double y1 = interactionViewBounds.getMinY() + c.getRadius(); //View.getInteractionView().getLayoutY() + 10;
                        double x2 = interactionViewBounds.getWidth() - c.getRadius(); //View.getInteractionView().getWidth() - 10; //View.getInteractionView().getWidth() - 10;
                        double y2 = interactionViewBounds.getHeight() - c.getRadius(); //View.getInteractionView().getHeight() - 10; //View.getInteractionView().getHeight() - 10;
//                        View.drawInteractionViewHitBounds();

                        Vector xVector = p.getDirectionVector().getXComponent();
                        Vector yVector = p.getDirectionVector().getYComponent();
                        double xSpeed = xVector.getSpeed();
                        double ySpeed = yVector.getSpeed();
                        double endCX = (cX + xSpeed);
                        double endCY = (cY + ySpeed);
                        double nextCX = (cX + (2 * xSpeed)); //+ (x1 - c.getRadius());
                        double nextCY = (cY + (2 * ySpeed)); // + (y1 - c.getRadius());

//                        System.out.println("person " + p + " @ (" + cX + ", " + cY + ") -> (" + endCX + ", " + endCY + ") is moveable in\n\t((" + x1 + ", " + y1 + "), (" + x2 + ", " + y2 + "))");
                        //Creating Translate Transition
                        TranslateTransition translateTransition = new TranslateTransition();

                        if (nextCX <= x1 || x2 <= nextCX) {
//                            System.err.print("X person: " + p + " will hit a side wall next move. \n\tVC:\t{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
//
//                            System.err.print("\n\tVX:\t" + xVector + "\tVY:\t" + yVector + "\n\t\t->\n\tVC:\t");
                            p.getDirectionVector().bounceXDirection();
                            xVector = p.getDirectionVector().getXComponent();
                            yVector = p.getDirectionVector().getYComponent();
//                            System.err.println("{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
                        }

                        if (nextCY <= y1 || y2 <= nextCY) {
//                            System.err.print("Y person: " + p + " will hit an end wall next move. \n\tVC:\t{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
//
//                            System.err.print("\n\tVX:\t" + xVector + "\n\tVY:\t" + yVector + "\n\t\t->\n\tVC:\t");
                            p.getDirectionVector().bounceYDirection();
                            xVector = p.getDirectionVector().getXComponent();
                            yVector = p.getDirectionVector().getYComponent();
//                            System.err.println("{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
                        }

                        if (PERFORM_PERSON_COLLISIONS) {
                            Circle pC = p.getCircle();
                            for (Person person : population) {
                                if (!p.equals(person) && !checkedPopulation.contains(person)) {
                                    Circle personCircle = person.getCircle();
                                    if (pC.intersects(personCircle.getBoundsInLocal())) {
                                        // collision
                                        String idString = genCollisionID();
                                        Collision collision = new Collision(idString, numCollisionCount, p, person);
                                        Vector[] resultVectors = collision.collide();
                                        p.setDirectionVector(resultVectors[0]);
                                        person.setDirectionVector(resultVectors[1]);
//                                        Vector aVector = collision.getPerson_A().getDirectionVector();
//                                        Vector bVector = collision.getPerson_B().getDirectionVector();
//                                        Vector[] aComponents = aVector.calcAxisComponents(); // ax, ay
//                                        Vector[] bComponents = bVector.calcAxisComponents(); // bx, by
//                                        double massA = p.getMass();
//                                        double massB = person.getMass();
//                                        double[] xChangeSpeed = collision.getFinalVelocities(massA, massB, aComponents[0].getSpeed(), bComponents[0].getSpeed()); // ax, bx
//                                        double[] yChangeSpeed = collision.getFinalVelocities(massA, massB, aComponents[1].getSpeed(), bComponents[1].getSpeed()); // ay, by
//                                        System.out.println("COLLISION: a: " + p.getDirectionVector() + ", b: " + person.getDirectionVector());
//                                        System.out.println("Components: a: " + Arrays.toString(aComponents) + ", b: " + Arrays.toString(bComponents));
//                                        System.out.println("aSpeedX(): " + aComponents[0].getSpeed() + ", aSpeedY(): " + aComponents[1].getSpeed() + ", xChangeSpeed: " + Arrays.toString(xChangeSpeed));
//                                        System.out.println("bSpeedX(): " + bComponents[0].getSpeed() + ", bSpeedY(): " + bComponents[1].getSpeed() + ", yChangeSpeed: " + Arrays.toString(yChangeSpeed));
//                                        Vector aChange = Vector.combineSpeeds(xChangeSpeed[0], yChangeSpeed[0]);
//                                        Vector bChange = Vector.combineSpeeds(xChangeSpeed[1], yChangeSpeed[1]);
//                                        System.out.println("aChange: " + aChange + ", bChange: " + bChange);
//
//                                        System.out.print("pVector: " + p.getDirectionVector() + " -> ");
//                                        p.setDirectionVector(aChange);
//                                        System.out.println(p.getDirectionVector());
//
//                                        System.out.print("PVector: " + person.getDirectionVector() + " -> ");
//                                        person.setDirectionVector(bChange);
//                                        System.out.println(person.getDirectionVector());
//
//                                        checkedPopulation.add(person);
//
//
//                                        double xDiff = Math.abs(pC.getCenterX() - personCircle.getCenterX());
//                                        double yDiff = Math.abs(pC.getCenterY() - personCircle.getCenterY());
//                                        boolean sameSize = pC.getRadius() == personCircle.getRadius();
//                                        boolean overlap = xDiff < pC.getRadius() || yDiff < pC.getRadius();
//
//                                        System.err.println(collision + "\n\t@ overlap: " + overlap + ", sameSize: " + sameSize + " (" + xDiff + ", " + yDiff + "\npC " + pC + " and\n" + personCircle);
                                    }
                                }
                            }
                        }
//                        System.out.println("\tySpeed: " + ySpeed + ", " + "xSpeed: " + xSpeed + "\n\tcY: " + cY + ", cX: " + cX + "\n\tendCY: " + endCY + ", endCX: " + endCX);

                        double totalTime = (1 / daysPerSecond) * 1000;
                        Line line = new Line(cX, cY, cX + xSpeed, cY + ySpeed);
//                        System.out.println("\tnew line: " + line);
                        p.addPath(line);
                        if (View.isShowingPaths()) {
                            View.drawPath(p);
                        }
                        p.setCoordinates(cX + xSpeed, cY + ySpeed);

                        //Setting the duration of the transition
                        translateTransition.setDuration(Duration.millis(totalTime));
                        translateTransition.setAutoReverse(false);
                        translateTransition.setCycleCount(Timeline.INDEFINITE);

                        parallelTransition.getChildren().add(translateTransition);

                        p.age();
                        if (!p.isInfected() && !p.isCured()) {
                            checkTransmit(p);
                        }
                        p.updateCircle();
                    }

                    pandemicHistory.setCaseHistory(caseHistoryPopulation);
                    pandemicHistory.setCuredPopulation(curedPopulation);
                    pandemicHistory.setPassedPopulation(passedPopulation);
                    pandemicHistory.setInfectedPopulation(infectedPopulation);

                    View.updateNewsList();
                    View.updateStatsPane();
                    parallelTransition.setCycleCount(Timeline.INDEFINITE);
//                    timeline.play();

                    updateChart();
                    infectedTodayPopulation.clear();
                    curedTodayPopulation.clear();
                    passedTodayPopulation.clear();
                }));
//        timeline.setCycleCount(Timeline.INDEFINITE);
        return timeline;
    }

    public static Person createNewPerson(double x, double y) {

        int personNum = ++numPeopleCount;
        String personID = genPersonID();
        double age = Utilities.getRandomAge(AVG_PERSON_AGE);
        double lifeSpan = Utilities.genRandomLifeSpan(age, AVG_LIFE_EXPECTANCY);
        boolean isMale = Utilities.randomDoubleInRange(0, 1) <= 0.5;
        Person person = new Person(personID, personNum, isMale, age, lifeSpan, AVG_PERSON_MASS, x, y);
        int ageVal = person.getAgeYears();
        double speed = Utilities.randomDoubleInRange(MIN_PERSON_SPEED, MAX_PERSON_SPEED);
        double degrees = Utilities.randomDoubleInRange(0, 360);
        Vector vector = new Vector(speed, degrees);
        person.setDirectionVector(vector);
        person.setMoveable(true);
        if (numInfectedCount < numInfectedStart) {
            boolean infected = Utilities.randomDoubleInRange(0, 100.001) < currentDisease.getInfectionRate(ageVal);
            if (infected) {
                setInfectedPerson(person, currentDisease);
            }
        }
        System.out.println("location (" + x + ", " + y + "), " + vector);
        return person;
    }

    public static void createPopulation() {
        double x1 = View.getInteractionView().getLayoutX() + 10;
        double y1 = View.getInteractionView().getLayoutY() + 10;
        double x2 = View.getInteractionView().getWidth() - 10;
        double y2 = View.getInteractionView().getHeight() - 10;
        interactionViewBounds = View.getInteractionView().getLayoutBounds();
        pandemicHistory = new PandemicHistory(
                startDate,
                (ArrayList<Person>) population.clone(),
                (ArrayList<Person>) infectedPopulation.clone(),
                currentDisease);
        if (x1 < x2 && y1 < y2) {
            for (int i = 0; i < numPeopleStart; i++) {
                double x = Utilities.randomDoubleInRange(10, x2);
                double y = Utilities.randomDoubleInRange(10, y2);
                Person person = Model.createNewPerson(x, y);
                population.add(person);
            }
            while (numInfectedStart > numInfectedCount) {
                int idx = (int) Utilities.randomDoubleInRange(0, population.size());
                if (!population.get(idx).isInfected()) {
                    Person person = population.get(idx);
                    setInfectedPerson(person, currentDisease);
                }
            }
        }
        // final loop to set visible attributes
        for (Person person : population) {
            double x = person.getLayoutX();
            double y = person.getLayoutY();
            person.setCircle(AVG_PERSON_DIAMETER, x, y);
        }
        System.out.println("\tPopulation:\n" + population + "\n\tInfected population:\n" + infectedPopulation);
    }

    private static void setInfectedPerson(Person person, Disease disease) {
        System.err.println(person + " has contracted " + disease.getName());
        person.setInfected(true);
        person.setDisease(disease);
        infectedPopulation.add(person);
        numInfectedCount++;
        numHealthyCount--;
        infectedTodayPopulation.add(person);
    }

    public static void setDeath(Person person) {
        numDeathCount++;
        passedPopulation.add(person);
        caseHistoryPopulation.add(person);
        passedTodayPopulation.add(person);
        System.err.println(person + " has passed away from " + person.getCauseOfDeath());
    }

    public static void setCured(Person person) {
        numCuredCount++;
        numHealthyCount++;
        numInfectedCount--;
        curedPopulation.add(person);
        curedTodayPopulation.add(person);
        person.setInfected(false);
        person.setCured(true);
        person.setMoveable(false);
        person.addDiseaseHistory();
        person.setDisease(null);
        infectedPopulation.remove(person);
        caseHistoryPopulation.add(person);
        person.setCauseOfDeath("CURED");
        person.updateCircle();
    }

    private static String genPersonID() {
        return "PERSON_NUM_" + Utilities.formatify(numPeopleCount);
    }

    private static String genCollisionID() {
        return "COLLISION_" + Utilities.formatify(++numCollisionCount);
    }

    public static void setDaysPerSecond(double value) {
        daysPerSecond = value;
    }

    public static int getNumPeopleStart() {
        return numPeopleStart;
    }

    public static int getNumCuredCount() {
        return numCuredCount;
    }

    public static int getNumDeathCount() {
        return numDeathCount;
    }

    public static int getNumHealthyCount() {
        return numHealthyCount;
    }

    public static int getNumInfectedCount() {
        return numInfectedCount;
    }

    public static int getNumPeopleCount() {
        return numPeopleCount;
    }

    public static ArrayList<Person> getPopulation() {
        return population;
    }

    public static ArrayList<Person> getAliveAndInfectedPopulation() {
        ArrayList<Person> infectedAndAlivePop = new ArrayList<>();
        infectedPopulation.forEach((p) -> {
            if (p.isAlive()) {
                infectedAndAlivePop.add(p);
            }
        });

        return infectedAndAlivePop;
    }

    public static ArrayList<Person> getInfectedPopulation() {
        return infectedPopulation;
    }

    public static ArrayList<Person> getCaseHistoryPopulation() {
        return caseHistoryPopulation;
    }

    public static ArrayList<Person> getPassedPopulation() {
        return passedPopulation;
    }

    public static ArrayList<Person> getCuredPopulation() {
        return curedPopulation;
    }

    public static void setNumPeopleStart(int numPeopleStart) {
        Model.numPeopleStart = numPeopleStart;
    }

    public static void setNumInfectedStart(int numInfectedStart) {
        Model.numInfectedStart = numInfectedStart;
    }

    private static void checkTransmit(Person person) {
        Circle circle = person.getCircle();
        for (Person p : infectedPopulation) {
            if (p.equals(person)) {
                continue;
            }
            Circle infectedCircle = p.getCircle();
            Disease disease = p.getDisease();
//            System.out.println("infected person: " + p + ", disease: " + disease.getName());
            if (circle.intersects(infectedCircle.getBoundsInLocal())) {
                if (p.isAlive() || disease.isTransmittableAfterDeath()) {
                    int ageVal = p.getAgeYears();
                    double infectionRate = disease.getInfectionRate(ageVal);
                    double chance = Utilities.randomDoubleInRange(0, 101);
                    if (chance <= infectionRate) {
                        setInfectedPerson(person, disease);
                        break;
                    }
                }
            }
        }
    }

    public static void playSim() {
        timeline = createTimeLine();
        System.out.println("infectedPopulation: " + infectedPopulation);
        System.out.println("curedPopulation: " + curedPopulation);
        System.out.println("aliveAndInfectedPopulation : " + getAliveAndInfectedPopulation());
        System.out.print("BEGIN playSim {");
//        System.out.print("\n\tstart runnable");
        if (getAliveAndInfectedPopulation().size() > 0) {
            if (timeline.getStatus() == Animation.Status.STOPPED ||
                    timeline.getStatus() == Animation.Status.PAUSED) {
                if (pandemicHistory == null) {
                    pandemicHistory = new PandemicHistory(
                            startDate,
                            (ArrayList<Person>) population.clone(),
                            (ArrayList<Person>) infectedPopulation.clone(),
                            currentDisease);
                }
                updateChart();
//                System.out.print("\n\t\tif is true");
                if (!View.isSteppingSim()) {
                    timeline.setCycleCount(Animation.INDEFINITE);
                    timeline.play();
                }
                else {
                    timeline.play();
                }
            }
        }
        else {
//            System.out.println("No one is infected");
            stopSim();
        }
//        System.out.print("\n\tend runnable");
        System.out.println("\n} -> END playSim");
    }

    public static void stopSim() {
        if (timeline.getStatus() == Animation.Status.RUNNING) {
            timeline.pause();
        }
        else if (timeline.getStatus() == Animation.Status.PAUSED) {
            timeline.stop();
        }
    }

    public static void clearSim() {
        stopSim();
        population.clear();
        populationCollisions.clear();
        infectedPopulation.clear();
        passedPopulation.clear();
        curedPopulation.clear();
        caseHistoryPopulation.clear();
        numInfectedCount = 0;
        numDeathCount = 0;
        numPeopleCount = 0;
        numHealthyCount = 0;
        numHealthyStart = 0;
        numCuredCount = 0;
        numCollisionCount = 0;
        currentDate = DateHandler.getToday();
        pandemicHistory = null;
    }

    public static Animation getTimeLine() {
        return timeline;
    }

    public static Date getCurrentDate() {
        return currentDate;
    }

    public static Date getStartDate() {
        return startDate;
    }

    public static void setCurrentDate(Date currentDateIn) {
        startDate = currentDateIn;
        currentDate = currentDateIn;
        View.setTimeView(currentDate);
    }

    public static boolean isShowDirectionVectors() {
        return SHOW_DIRECTION_VECTORS;
    }

    public static boolean isShowPersonIds() {
        return SHOW_PERSON_IDS;
    }

    public static void updateChart() {
        HistoryPoint hp = new HistoryPoint(
                (Date) currentDate.clone(),
                (ArrayList<Person>) infectedPopulation.clone(),
                (ArrayList<Person>) curedPopulation.clone(),
                (ArrayList<Person>) passedPopulation.clone(),
                (ArrayList<Person>) infectedTodayPopulation.clone(),
                (ArrayList<Person>) curedTodayPopulation.clone(),
                (ArrayList<Person>) passedTodayPopulation.clone());
        pandemicHistory.addHistoryPoint(hp);
        View.updateChart();
    }

    public static PandemicHistory getHistory() {
        return pandemicHistory;
    }
}

package sample;

import javafx.animation.KeyFrame;
import javafx.animation.ParallelTransition;
import javafx.animation.Timeline;
import javafx.animation.TranslateTransition;
import javafx.event.ActionEvent;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.util.Duration;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class BallSimulation {

    public enum LegendOrientation {
        NORTH_WEST,
        NORTH_EAST,
        SOUTH_WEST,
        SOUTH_EAST
    }

    public enum PossibleColours {
        RED(Color.color(1, 0, 0, 1)),
        GREEN(Color.color(0, 1, 0, 1)),
        BLUE(Color.color(0, 0, 1, 1)),
        YELLOW(Color.color(0.98, 0.72, 0.011, 1)),
        ORANGE(Color.color(0.98, 0.48, 0.011, 1)),
        PURPLE(Color.color(0.41, 0.011, 0.98, 1)),
        CYAN(Color.color(0.011, 0.94, 0.98, 1)),
        DARK_GREEN(Color.color(0.07, 0.29, 0.13, 1)),
        DARK_RED(Color.color(0.23, 0, 0, 1)),
        PINK(Color.color(1, 0.45, 0.45, 1));

        public Paint paint;

        PossibleColours(Paint paint) {
            this.paint = paint;
        }

        public Paint getPaint() {
            return paint;
        }
    }

    private final ArrayList<Class> supportedCurves = new ArrayList<>(Arrays.asList(
            Brachistochrone.class,
            Cycloid.class,
            Parabolic.class,
            Linear.class
    ));

    private double x1;                          // lower x-value
    private double y1;                          // higher y-value
    private double x2;                          // higher x-value
    private double y2;                          // lower y-value
    private int segments;                       // number of frames
    private double duration;                    // seconds
    private ArrayList<GraphingCurve> curves;    // Curve sub-classes to draw

    private Paint legendColour;
    private LegendOrientation legendOrientation;
    private double horizontalMargin;
    private double verticalMargin;
    private double widthProportion;
    private double heightProportion;
    private double borderSize;
    private double legendX;
    private double legendY;
    private double legendW;
    private double legendH;
    private int ballRadius;
    private ArrayList<Paint> possibleColours;

    public BallSimulation(double x1, double y1, double x2, double y2, int segments, double duration, Class... curveClasses) throws IllegalAccessException, InstantiationException, InvocationTargetException {
        this.legendColour = Color.color(0.55, 0.55, 0.55, 1);
        this.ballRadius = 5;
        this.legendOrientation = LegendOrientation.NORTH_EAST;
        this.horizontalMargin = 0.1;
        this.verticalMargin = 0.1;
        this.widthProportion = 0.25;
        this.heightProportion = 0.25;
        this.borderSize = 4;
        this.possibleColours = getNewPossibleColours();

        // Ensuring all curves will have negative slopes so that
        // a ball may roll down it's surface.
        Curve c = new Curve(x1, y1, x2, y2, segments, true);
        this.x1 = c.getX1();
        this.y1 = c.getY1();
        this.x2 = c.getX2();
        this.y2 = c.getY2();

        this.segments = segments;
        this.duration = duration;
        this.curves = new ArrayList<>();
        for (Class clazz : curveClasses) {
            if (supportedCurves.contains(clazz)) {
                Constructor constructor = clazz.getDeclaredConstructors()[0];
                Curve curve = (Curve) constructor.newInstance(this.x1, this.y1, this.x2, this.y2, segments, true);
                System.out.println("CONSTRUCTORS: " + curve);
                GraphingCurve graphingCurve = new GraphingCurve(curve, getNewCurveColour());
                this.curves.add(graphingCurve);
            }
        }
    }

    public Paint getNewCurveColour() {
        int size = this.possibleColours.size();
        int idx = (int) Math.floor(Math.random() * size);
        Paint paint = possibleColours.remove(idx);
        this.possibleColours.remove(paint);
        return paint;
    }

    public ArrayList<Paint> getNewPossibleColours() {
//        ArrayList<PossibleColours> pc = new ArrayList<>(Arrays.asList(PossibleColours.values()));
//        return new ArrayList<>(pc.stream().map(PossibleColours::getPaint).collect(Collectors.toList()));
//        ArrayList<PossibleColours> pc = new ArrayList<>(Arrays.asList(PossibleColours.values()));
        return new ArrayList<>(Arrays.asList(PossibleColours.values()).stream().map(PossibleColours::getPaint).collect(Collectors.toList()));
    }

    public void draw(Canvas canvas) {
        // draw legend
        calcLegendOrientation(canvas);
        GraphicsContext gc = canvas.getGraphicsContext2D();
        Main.changeCanvasColour(canvas, legendColour);
        gc.fillRect(legendX, legendY, legendW,legendH);
        Main.changeCanvasColour(canvas, Color.WHITE);
        gc.fillRect(legendX + borderSize, legendY + borderSize, legendW - (2 * borderSize),legendH - (2 * borderSize));


//        // draw each curve
//        for (int i = 0, curvesSize = curves.size(); i < curvesSize; i++) {
//            GraphingCurve graphingCurve = curves.get(i);
//            graphingCurve.draw(canvas);
//            // update legend
//            double x = legendX + (2 * borderSize) + gc.getFont().getSize();// + (i * (legendW / supportedCurves.size()));
//            double y = legendY + (2 * borderSize) + gc.getFont().getSize() + (i * ((legendH - (2 * borderSize)) / supportedCurves.size()));
//            String m = graphingCurve.toString() + " - " + graphingCurve.getEquation();
//                    gc.strokeText(m, x, y);
//        }

        // TODO decide how to display the curves, either canvas or using nodes.
        //  timeline seems to only work with nodes.
        Timeline timeline = createTimeLine(canvas);
        timeline.play();
    }

    public void calcLegendOrientation(Canvas canvas) {
        double width = canvas.getWidth();
        double height = canvas.getHeight();
        double legendX = width * horizontalMargin;
        double legendY = height * verticalMargin;

        double w = width * widthProportion;
        double h = height * heightProportion;

        switch (legendOrientation) {
            case NORTH_EAST:    legendX = (width * (1 - horizontalMargin)) - w;
                                break;
            case SOUTH_WEST:    legendY = (height * (1 - verticalMargin)) - h;
                                break;
            case SOUTH_EAST:    legendX = (width * (1 - horizontalMargin)) - w;
                                legendY = (height * (1 - verticalMargin)) - h;
                                break;
            default:            break; // already set to north west corner
        }

        /// NW, NE, SE, SW
        // NW, SW - same x
        // NE, SE - same x
        // NW, NE - same y
        // SW, SE - same y
        this.legendX = legendX;
        this.legendY = legendY;
        this.legendW = w;
        this.legendH = h;

    }

    public Timeline createTimeLine(Canvas canvas) {
        List<Double> times = curves.stream().map(GraphingCurve::getDuration).collect(Collectors.toList());
        System.out.println("times: " + times);
        double maxT = times.stream().reduce(0.0, Math::max);
        Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(maxT),
                (ActionEvent event) -> {
                    ParallelTransition parallelTransition = new ParallelTransition();
                    for (GraphingCurve graphingCurve : curves) {
                        double t = graphingCurve.getDuration();
                        double tIncrement = t / segments;
                        for (double x = 0; x < t; x += tIncrement) {
                            BigDecimal[] point = graphingCurve.getPointAtT(x);
                            double xPos = point[0].doubleValue();
                            double yPos = point[1].doubleValue();
//                            Circle circle = new Circle(xPos, yPos, 5, graphingCurve.getColour());
                            canvas.getGraphicsContext2D().fillOval(xPos, yPos, 5, graphingCurve.getColour().hashCode());
                        }
                        TranslateTransition translateTransition = new TranslateTransition();
                        translateTransition.setDuration(Duration.millis(t * 1000));
                        translateTransition.setAutoReverse(false);
                        translateTransition.setCycleCount(Timeline.INDEFINITE);

                        parallelTransition.getChildren().add(translateTransition);

                    }
                    parallelTransition.setCycleCount(Timeline.INDEFINITE);
                }
        ));
        timeline.setCycleCount(Timeline.INDEFINITE);
        System.out.println("maxT: " + maxT);
        return timeline;
    }

//    public static Timeline createTimeLine() {
//        double t = (1 / daysPerSecond);
//        infectedTodayPopulation = new ArrayList<>();
//        curedTodayPopulation = new ArrayList<>();
//        passedTodayPopulation = new ArrayList<>();
//        timeline = new Timeline(new KeyFrame(Duration.seconds(t),
//                (ActionEvent event) -> {
//
//                    if (getAliveAndInfectedPopulation().size() == 0) {
//                        stopSim();
//                        return;
//                    }
//
//                    ParallelTransition parallelTransition = new ParallelTransition();
//
//                    currentDate = DateHandler.nextDate(currentDate);
//                    System.out.println(String.format("this is called every %f seconds on UI thread: ", t) + DateHandler.getDateString(currentDate));
//                    View.setTimeView(currentDate);
//                    ArrayList<Person> checkedPopulation = new ArrayList<>();
//                    for (Person p : population) {
////                        System.out.println("\tperson: " + p);
//                        if (!p.isMoveable()) {
//                            continue;
//                        }
//
//                        Circle c = p.getCircle();
//                        double cX = c.getCenterX();
//                        double cY = c.getCenterY();
//                        double x1 = interactionViewBounds.getMinX() + c.getRadius(); //View.getInteractionView().getLayoutX() + 10;
//                        double y1 = interactionViewBounds.getMinY() + c.getRadius(); //View.getInteractionView().getLayoutY() + 10;
//                        double x2 = interactionViewBounds.getWidth() - c.getRadius(); //View.getInteractionView().getWidth() - 10; //View.getInteractionView().getWidth() - 10;
//                        double y2 = interactionViewBounds.getHeight() - c.getRadius(); //View.getInteractionView().getHeight() - 10; //View.getInteractionView().getHeight() - 10;
////                        View.drawInteractionViewHitBounds();
//
//                        Vector xVector = p.getDirectionVector().getXComponent();
//                        Vector yVector = p.getDirectionVector().getYComponent();
//                        double xSpeed = xVector.getSpeed();
//                        double ySpeed = yVector.getSpeed();
//                        double endCX = (cX + xSpeed);
//                        double endCY = (cY + ySpeed);
//                        double nextCX = (cX + (2 * xSpeed)); //+ (x1 - c.getRadius());
//                        double nextCY = (cY + (2 * ySpeed)); // + (y1 - c.getRadius());
//
////                        System.out.println("person " + p + " @ (" + cX + ", " + cY + ") -> (" + endCX + ", " + endCY + ") is moveable in\n\t((" + x1 + ", " + y1 + "), (" + x2 + ", " + y2 + "))");
//                        //Creating Translate Transition
//                        TranslateTransition translateTransition = new TranslateTransition();
//
//                        if (nextCX <= x1 || x2 <= nextCX) {
////                            System.err.print("X person: " + p + " will hit a side wall next move. \n\tVC:\t{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
////
////                            System.err.print("\n\tVX:\t" + xVector + "\tVY:\t" + yVector + "\n\t\t->\n\tVC:\t");
//                            p.getDirectionVector().bounceXDirection();
//                            xVector = p.getDirectionVector().getXComponent();
//                            yVector = p.getDirectionVector().getYComponent();
////                            System.err.println("{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
//                        }
//
//                        if (nextCY <= y1 || y2 <= nextCY) {
////                            System.err.print("Y person: " + p + " will hit an end wall next move. \n\tVC:\t{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
////
////                            System.err.print("\n\tVX:\t" + xVector + "\n\tVY:\t" + yVector + "\n\t\t->\n\tVC:\t");
//                            p.getDirectionVector().bounceYDirection();
//                            xVector = p.getDirectionVector().getXComponent();
//                            yVector = p.getDirectionVector().getYComponent();
////                            System.err.println("{ " + p.getDirectionVector() + " }\n\tVX:\t" + xVector + "\tVY:\t" + yVector);
//                        }
//
//                        if (PERFORM_PERSON_COLLISIONS) {
//                            Circle pC = p.getCircle();
//                            for (Person person : population) {
//                                if (!p.equals(person) && !checkedPopulation.contains(person)) {
//                                    Circle personCircle = person.getCircle();
//                                    if (pC.intersects(personCircle.getBoundsInLocal())) {
//                                        // collision
//                                        String idString = genCollisionID();
//                                        Collision collision = new Collision(idString, numCollisionCount, p, person);
//                                        Vector[] resultVectors = collision.collide();
//                                        p.setDirectionVector(resultVectors[0]);
//                                        person.setDirectionVector(resultVectors[1]);
////                                        Vector aVector = collision.getPerson_A().getDirectionVector();
////                                        Vector bVector = collision.getPerson_B().getDirectionVector();
////                                        Vector[] aComponents = aVector.calcAxisComponents(); // ax, ay
////                                        Vector[] bComponents = bVector.calcAxisComponents(); // bx, by
////                                        double massA = p.getMass();
////                                        double massB = person.getMass();
////                                        double[] xChangeSpeed = collision.getFinalVelocities(massA, massB, aComponents[0].getSpeed(), bComponents[0].getSpeed()); // ax, bx
////                                        double[] yChangeSpeed = collision.getFinalVelocities(massA, massB, aComponents[1].getSpeed(), bComponents[1].getSpeed()); // ay, by
////                                        System.out.println("COLLISION: a: " + p.getDirectionVector() + ", b: " + person.getDirectionVector());
////                                        System.out.println("Components: a: " + Arrays.toString(aComponents) + ", b: " + Arrays.toString(bComponents));
////                                        System.out.println("aSpeedX(): " + aComponents[0].getSpeed() + ", aSpeedY(): " + aComponents[1].getSpeed() + ", xChangeSpeed: " + Arrays.toString(xChangeSpeed));
////                                        System.out.println("bSpeedX(): " + bComponents[0].getSpeed() + ", bSpeedY(): " + bComponents[1].getSpeed() + ", yChangeSpeed: " + Arrays.toString(yChangeSpeed));
////                                        Vector aChange = Vector.combineSpeeds(xChangeSpeed[0], yChangeSpeed[0]);
////                                        Vector bChange = Vector.combineSpeeds(xChangeSpeed[1], yChangeSpeed[1]);
////                                        System.out.println("aChange: " + aChange + ", bChange: " + bChange);
////
////                                        System.out.print("pVector: " + p.getDirectionVector() + " -> ");
////                                        p.setDirectionVector(aChange);
////                                        System.out.println(p.getDirectionVector());
////
////                                        System.out.print("PVector: " + person.getDirectionVector() + " -> ");
////                                        person.setDirectionVector(bChange);
////                                        System.out.println(person.getDirectionVector());
////
////                                        checkedPopulation.add(person);
////
////
////                                        double xDiff = Math.abs(pC.getCenterX() - personCircle.getCenterX());
////                                        double yDiff = Math.abs(pC.getCenterY() - personCircle.getCenterY());
////                                        boolean sameSize = pC.getRadius() == personCircle.getRadius();
////                                        boolean overlap = xDiff < pC.getRadius() || yDiff < pC.getRadius();
////
////                                        System.err.println(collision + "\n\t@ overlap: " + overlap + ", sameSize: " + sameSize + " (" + xDiff + ", " + yDiff + "\npC " + pC + " and\n" + personCircle);
//                                    }
//                                }
//                            }
//                        }
////                        System.out.println("\tySpeed: " + ySpeed + ", " + "xSpeed: " + xSpeed + "\n\tcY: " + cY + ", cX: " + cX + "\n\tendCY: " + endCY + ", endCX: " + endCX);
//
//                        double totalTime = (1 / daysPerSecond) * 1000;
//                        Line line = new Line(cX, cY, cX + xSpeed, cY + ySpeed);
////                        System.out.println("\tnew line: " + line);
//                        p.addPath(line);
//                        if (View.isShowingPaths()) {
//                            View.drawPath(p);
//                        }
//                        p.setCoordinates(cX + xSpeed, cY + ySpeed);
//
//                        //Setting the duration of the transition
//                        translateTransition.setDuration(Duration.millis(totalTime));
//                        translateTransition.setAutoReverse(false);
//                        translateTransition.setCycleCount(Timeline.INDEFINITE);
//
//                        parallelTransition.getChildren().add(translateTransition);
//
//                        p.age();
//                        if (!p.isInfected() && !p.isCured()) {
//                            checkTransmit(p);
//                        }
//                        p.updateCircle();
//                    }
//
//                    pandemicHistory.setCaseHistory(caseHistoryPopulation);
//                    pandemicHistory.setCuredPopulation(curedPopulation);
//                    pandemicHistory.setPassedPopulation(passedPopulation);
//                    pandemicHistory.setInfectedPopulation(infectedPopulation);
//
//                    View.updateNewsList();
//                    View.updateStatsPane();
//                    parallelTransition.setCycleCount(Timeline.INDEFINITE);
////                    timeline.play();
//
//                    updateChart();
//                    infectedTodayPopulation.clear();
//                    curedTodayPopulation.clear();
//                    passedTodayPopulation.clear();
//                }));
////        timeline.setCycleCount(Timeline.INDEFINITE);
//
//        if (getAliveAndInfectedPopulation().size() > 0) {
//            extraDay = false;
//        }
//        return timeline;
//    }
}

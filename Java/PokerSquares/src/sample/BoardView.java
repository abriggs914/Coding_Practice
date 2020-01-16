package sample;

import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Line;

public class BoardView extends BorderPane {

    private int columns;
    private int rows;
    private double width; // window width
    private double height; // window height
    private double leftWidth;
    private double leftHeight;
    private double rightWidth;
    private double rightHeight;
    private double topWidth;
    private double topHeight;
    private double bottomWidth;
    private double bottomHeight;
    private double centerWidth;
    private double centerHeight;
    private double cellWidth;
    private double cellHeight;

    private AnchorPane grid;

    public BoardView(int rows, int cols, double width, double height) {
        this.rows = rows;
        this.columns = cols;
        this.width = width;
        this.height = height;
        this.grid = new AnchorPane();
        calcSizes();
        drawGrid();
        this.setCenter(grid);
    }

    public void calcSizes() {
        this.leftWidth = width / 5; // 1/5
        this.leftHeight = (8 * height) / 10; // 8/10
        this.rightWidth = width / 5; // 1/6
        this.rightHeight = (8 * height) / 10; // 8/10
        this.topWidth = width;
        this.topHeight = height / 10; // 1/10
        this.bottomWidth = width;
        this.bottomHeight = height / 10; // 1/10
        this.centerWidth = (3 * width) / 5; // 3/5
        this.centerHeight = (8 * height) / 10; // 8/10;
        this.cellHeight = centerHeight / rows;
        this.cellWidth = centerWidth / columns;
    }

    public void drawGrid() {
        this.grid.setMinWidth(centerWidth);
        this.grid.setMaxWidth(centerWidth);
        this.grid.setPrefWidth(centerWidth);

        this.grid.setMinHeight(centerHeight);
        this.grid.setMaxHeight(centerHeight);
        this.grid.setPrefHeight(centerHeight);

        double rowSpacer = cellHeight;
        double colSpacer = cellWidth;
        double currX = 0;
        double currY = 0;
        System.out.println("rowSpacer: " + rowSpacer + ", colSpacer: " + colSpacer);
        for (int i = 0; i < rows+1; i++) {
            Line l = new Line(0, currY, centerWidth, currY);
            l.setStrokeWidth(2);
            l.setStroke(Color.BLACK);
            currY += rowSpacer;
            grid.getChildren().add(l);
        }
        for (int i = 0; i < columns+1; i++) {
            Line l = new Line(currX, 0, currX, centerHeight);
            l.setStrokeWidth(2);
            l.setStroke(Color.BLACK);
            currX += colSpacer;
            grid.getChildren().add(l);
        }
//        this.setStyle("-fx-border-color: black");
        Image background = new Image("resources/board_background.png");
        BackgroundImage backgroundImage = new BackgroundImage(background, BackgroundRepeat.REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT,
                BackgroundSize.DEFAULT);
        grid.setBackground(new Background(backgroundImage));
    }

}

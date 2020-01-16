package sample;

import javafx.scene.layout.BorderPane;

public class View extends BorderPane {

    public View() {
        this.setStyle("-fx-border-color: purple");
        System.out.println("size W: " + this.getWidth() + " H: " + this.getHeight());
    }
}

package sample;

import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Spinner;
import javafx.scene.layout.HBox;
import javafx.scene.text.Font;

public class BarsToolBar extends HBox {

    private Label numBarsLabel = new Label("# of bars:");
    private Spinner numBarsSpinner = new Spinner<Integer>(0, 10, 0);
    private Button submitButton = new Button("SUBMIT");
    private Font helvetica = new Font("Helvetica", 15);

    public BarsToolBar() {

        numBarsSpinner.setEditable(true);
        numBarsLabel.setFont(helvetica);

        numBarsSpinner.getEditor().textProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal != null && ! newVal.matches("-?[0-9]*")) {
                numBarsSpinner.getEditor().setText(oldVal);
            }
        });

        submitButton.setOnAction(event -> {
            System.out.println("submitting...");
        });

        this.setSpacing(15);
        this.setPadding(new Insets(10, 10, 10, 10));
        this.getChildren().addAll(numBarsLabel, numBarsSpinner, submitButton);
    }

}

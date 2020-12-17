package sample.Version_4;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.shape.Line;

import java.util.ArrayList;

public class TriangleCreatorBar {

    // place an adjustable triangle on the WhiteBoard
    //  -   Each corner will have a zone that can be clicked and dragged which will change.
    //      the dimensions of the triangle.
    //  -   allow customization of line colour, width.
    // input boxes for custom triangles.
    //  -   Have one input for a, b, c, A, B, and C. must follow and handle creation exceptions.
    //  -   also provide customization for each triangle
    // listView containing all triangles created by this widget.
    //  -   When a triangle is clicked, change bar contents to customization window.

    private boolean isHorizontal;
    private HBox hBar;
    private VBox vBar;

    private TextField nameTextField;
    private ListView<Triangle> triangleListView;
    private ArrayList<Triangle> trianglesCreated;

    public TriangleCreatorBar() {
        nameTextField = new TextField();
        triangleListView = new ListView<>();
        trianglesCreated = new ArrayList<>();
    }

    public void updateCreatedListView() {
        ObservableList<Triangle> triangles = FXCollections.observableArrayList(trianglesCreated);
        triangleListView.getItems().clear();
        triangleListView.getItems().addAll(triangles);
    }

    public void addCreatedTriangle(AdjustableTriangle... ts) {
        for (Triangle t : ts) {
            this.trianglesCreated.add(t);
        }
    }

    public void createAdjustableTriangle() {
        String name = getNameInput();
        Line a = new Line();
        Line b = new Line();
        Line c = new Line();
        AdjustableTriangle t = WhiteBoardModel.createAdjustableTriangle(name, a, b, c);
        addCreatedTriangle(t);
        updateCreatedListView();
    }

    public String getNameInput() {
        String name = nameTextField.getText();
//        if (name.length() == 0) {
//            name = WhiteBoardModel.genTriangleName();
//        }
        return name;
    }
}

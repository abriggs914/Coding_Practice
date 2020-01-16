package sample;

import javafx.scene.Node;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

public class CardViews extends BorderPane {

    private HBox heartsHBox;
    private HBox diamondsHBox;
    private HBox spadesHBox;
    private HBox clubsHBox;
    private HBox cardBacks;
    private VBox grid;

    public CardViews() {
        init();
        grid.getChildren().addAll(heartsHBox, spadesHBox, diamondsHBox, clubsHBox, cardBacks);
        this.setCenter(grid);
    }

    public void init() {
        grid = new VBox();
        cardBacks = new HBox();
        heartsHBox = new HBox();
        diamondsHBox = new HBox();
        spadesHBox = new HBox();
        clubsHBox = new HBox();

        setHearts();
        setClubs();
        setDiamonds();
        setSpades();
        setBacks();

        setBounds(heartsHBox);
        setBounds(spadesHBox);
        setBounds(diamondsHBox);
        setBounds(clubsHBox);
        setBounds(cardBacks);
    }

    private void setBounds(HBox hBox) {
        for (Node n : hBox.getChildren()) {
            ImageView i = (ImageView) n;
            i.setFitWidth(60);
            i.setFitHeight(90);
        }
    }

    public void setBacks() {
        ImageView blueBackYellowDiamonds = new ImageView(new Image("resources/back_blue_&_yellow_diamonds.png"));
        cardBacks.getChildren().addAll(blueBackYellowDiamonds);
    }

    public void setHearts() {
        ImageView ace = new ImageView(new Image("resources/hearts_A.png"));
        ImageView two = new ImageView(new Image("resources/hearts_2.png"));
        ImageView three = new ImageView(new Image("resources/hearts_3.png"));
        ImageView four = new ImageView(new Image("resources/hearts_4.png"));
        ImageView five = new ImageView(new Image("resources/hearts_5.png"));
        ImageView six = new ImageView(new Image("resources/hearts_6.png"));
        ImageView seven = new ImageView(new Image("resources/hearts_7.png"));
        ImageView eight = new ImageView(new Image("resources/hearts_8.png"));
        ImageView nine = new ImageView(new Image("resources/hearts_9.png"));
        ImageView ten = new ImageView(new Image("resources/hearts_10.png"));
        ImageView jack = new ImageView(new Image("resources/hearts_J.png"));
        ImageView queen = new ImageView(new Image("resources/hearts_Q.png"));
        ImageView king = new ImageView(new Image("resources/hearts_K.png"));

        heartsHBox.getChildren().addAll(ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king);
//        heartsHBox.setStyle("-fx-border-color: black");
    }

    public void setSpades() {
        ImageView ace = new ImageView(new Image("resources/spades_A.png"));
        ImageView two = new ImageView(new Image("resources/spades_2.png"));
        ImageView three = new ImageView(new Image("resources/spades_3.png"));
        ImageView four = new ImageView(new Image("resources/spades_4.png"));
        ImageView five = new ImageView(new Image("resources/spades_5.png"));
        ImageView six = new ImageView(new Image("resources/spades_6.png"));
        ImageView seven = new ImageView(new Image("resources/spades_7.png"));
        ImageView eight = new ImageView(new Image("resources/spades_8.png"));
        ImageView nine = new ImageView(new Image("resources/spades_9.png"));
        ImageView ten = new ImageView(new Image("resources/spades_10.png"));
        ImageView jack = new ImageView(new Image("resources/spades_J.png"));
        ImageView queen = new ImageView(new Image("resources/spades_Q.png"));
        ImageView king = new ImageView(new Image("resources/spades_K.png"));

        spadesHBox.getChildren().addAll(ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king);
    }

    public void setDiamonds() {
        ImageView ace = new ImageView(new Image("resources/diamonds_A.png"));
        ImageView two = new ImageView(new Image("resources/diamonds_2.png"));
        ImageView three = new ImageView(new Image("resources/diamonds_3.png"));
        ImageView four = new ImageView(new Image("resources/diamonds_4.png"));
        ImageView five = new ImageView(new Image("resources/diamonds_5.png"));
        ImageView six = new ImageView(new Image("resources/diamonds_6.png"));
        ImageView seven = new ImageView(new Image("resources/diamonds_7.png"));
        ImageView eight = new ImageView(new Image("resources/diamonds_8.png"));
        ImageView nine = new ImageView(new Image("resources/diamonds_9.png"));
        ImageView ten = new ImageView(new Image("resources/diamonds_10.png"));
        ImageView jack = new ImageView(new Image("resources/diamonds_J.png"));
        ImageView queen = new ImageView(new Image("resources/diamonds_Q.png"));
        ImageView king = new ImageView(new Image("resources/diamonds_K.png"));

        diamondsHBox.getChildren().addAll(ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king);
    }

    public void setClubs() {
        ImageView ace = new ImageView(new Image("resources/clubs_A.png"));
        ImageView two = new ImageView(new Image("resources/clubs_2.png"));
        ImageView three = new ImageView(new Image("resources/clubs_3.png"));
        ImageView four = new ImageView(new Image("resources/clubs_4.png"));
        ImageView five = new ImageView(new Image("resources/clubs_5.png"));
        ImageView six = new ImageView(new Image("resources/clubs_6.png"));
        ImageView seven = new ImageView(new Image("resources/clubs_7.png"));
        ImageView eight = new ImageView(new Image("resources/clubs_8.png"));
        ImageView nine = new ImageView(new Image("resources/clubs_9.png"));
        ImageView ten = new ImageView(new Image("resources/clubs_10.png"));
        ImageView jack = new ImageView(new Image("resources/clubs_J.png"));
        ImageView queen = new ImageView(new Image("resources/clubs_Q.png"));
        ImageView king = new ImageView(new Image("resources/clubs_K.png"));

        clubsHBox.getChildren().addAll(ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king);
    }
}

package sample;

import javafx.application.Platform;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Parent;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

/**
 * Global controller for all tabs.
 */

public class Controller {

//    @FXML public Button gameCreationOkButton;
//    @FXML public Button gameCreationClearButton;

    private static StringBuilder reportString;

    private static ObservableList<Gym> gameCreationGymsList;
    private static ObservableList<Team> gameCreationAwayTeamsList;
    private static ObservableList<Team> gameCreationHomeTeamsList;
    private static ObservableList<Referee> gameCreationRefereeAList;
    private static ObservableList<Referee> gameCreationRefereeBList;

    private static DatePicker gameCreationDatePicker;
    private static Slider gameCreationTimeSlider;
    private static Spinner<Double> gameCreationTimeReportSpinner;
    private static ComboBox<Gym> gameCreationGymComboBox;
    private static ComboBox<Team> gameCreationHomeTeamComboBox;
    private static ComboBox<Team> gameCreationAwayTeamComboBox;
    private static ComboBox<Referee> gameCreationRefereeAComboBox;
    private static ComboBox<Referee> gameCreationRefereeBComboBox;

    private static TextArea gameCreationReportTextArea;

//    Controller() {
//        GridPane gp = FXMLLoader;
//        this.gameCreationTeamComboBox = FX
//        this.gameCreationOkButton = game_creation_ok_button;
//        gameCreationOkButton.setOnAction(this::gameCreation_okButtonClicked);
//        gameCreationClearButton.setOnAction(this::gameCreation_clearButtonClicked);

//        ObservableList<Team> gameCreationAwayTeamsList = (ObservableList<Team>) Team.getValues();
//        ObservableList<Team> gameCreationHomeTeamsList = (ObservableList<Team>) Team.getValues();
//
//        gameCreationHomeTeamComboBox.setItems(gameCreationHomeTeamsList);
//        gameCreationAwayTeamComboBox.setItems(gameCreationAwayTeamsList);
//    }

    public void init(Parent parent) {

        reportString = new StringBuilder();

        // Begin gameCreation set-up
        gameCreationGymsList = FXCollections.observableArrayList(Gym.getValues()).sorted(Gym.compareGymNames());
        gameCreationAwayTeamsList = FXCollections.observableArrayList(Team.getValues()).sorted(Team.compareTeamNames());
        gameCreationHomeTeamsList = FXCollections.observableArrayList(Team.getValues()).sorted(Team.compareTeamNames());
        gameCreationRefereeAList = FXCollections.observableArrayList(Referee.getValues()).sorted(Referee.compareRefereeNames());
        gameCreationRefereeBList = FXCollections.observableArrayList(Referee.getValues()).sorted(Referee.compareRefereeNames());

        gameCreationDatePicker = (DatePicker) parent.lookup("#game_creation_datePicker");
        gameCreationTimeSlider = (Slider) parent.lookup("#game_creation_time_slider");
        gameCreationTimeReportSpinner = (Spinner) parent.lookup("#game_creation_time_report_spinner");
        gameCreationGymComboBox = (ComboBox<Gym>) parent.lookup("#game_creation_gym_comboBox");
        gameCreationHomeTeamComboBox = (ComboBox<Team>) parent.lookup("#game_creation_home_team_comboBox");
        gameCreationAwayTeamComboBox = (ComboBox<Team>) parent.lookup("#game_creation_away_team_comboBox");
        gameCreationRefereeAComboBox = (ComboBox<Referee>) parent.lookup("#game_creation_referee_A_comboBox");
        gameCreationRefereeBComboBox = (ComboBox<Referee>) parent.lookup("#game_creation_referee_B_comboBox");
        gameCreationReportTextArea = (TextArea) parent.lookup("#game_creation_report_textArea");

        gameCreationGymComboBox.setItems(gameCreationGymsList);
        gameCreationHomeTeamComboBox.setItems(gameCreationHomeTeamsList);
        gameCreationAwayTeamComboBox.setItems(gameCreationAwayTeamsList);
        gameCreationRefereeAComboBox.setItems(gameCreationRefereeAList);
        gameCreationRefereeBComboBox.setItems(gameCreationRefereeBList);

        gameCreationTimeSlider.setOnMouseDragged(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                double time = gameCreationTimeSlider.getValue();
                gameCreationTimeReportSpinner.getEditor().setText(Utilities.parseTime(time, false));
            }
        });

        gameCreationTimeSlider.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                double time = gameCreationTimeSlider.getValue();
                gameCreationTimeReportSpinner.getEditor().setText(Utilities.parseTime(time, false));
            }
        });
//        gameCreationTimeReportSpinner.valueProperty().addListener((observableValue, oldValue, newValue) -> gameCreation_spinnerButton(observableValue, oldValue, newValue));
        gameCreationTimeReportSpinner.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean increment = event.getPickResult().toString().contains("increment-arrow-button");
//                System.out.println("incrementing: " + increment);
                String timeText = gameCreationTimeReportSpinner.getEditor().getText();
                double timeValue = 0.0;
                String newTime = null;
                if (increment) {
                    newTime = Utilities.addOneMinute(timeText);
                }
                else {
                    newTime = Utilities.subtractOneMinute(timeText);
                }
                timeValue = Utilities.getTimeSliderValue(newTime);
                gameCreationTimeReportSpinner.getEditor().setText(newTime);
                gameCreationTimeSlider.setValue(timeValue);
            }
        });

        gameCreationHomeTeamComboBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                Team teamSelected = gameCreationHomeTeamComboBox.getValue();
                Team alreadySelected = Main.gameManager.getGameCreation_homeTeamSelected();
                Platform.runLater(() -> {
                    if (alreadySelected == null) {
                        Main.gameManager.gameCreation_setHomeTeamSelected(teamSelected);
                    }
                    else if (alreadySelected != teamSelected) {
                        gameCreationAwayTeamsList = addTeam(alreadySelected, gameCreationAwayTeamsList);
                        updateTeamComboBox(gameCreationAwayTeamsList, gameCreationAwayTeamComboBox);
                        Main.gameManager.gameCreation_setHomeTeamSelected(teamSelected);
                    }
                    gameCreationAwayTeamsList = removeTeam(teamSelected, gameCreationAwayTeamsList);
                    updateTeamComboBox(gameCreationAwayTeamsList, gameCreationAwayTeamComboBox);
                });
            }
        });

        gameCreationRefereeAComboBox.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                Referee refereeSelected = gameCreationRefereeAComboBox.getValue();
                Referee alreadySelected = Main.gameManager.gameCreation_getRefereeASelected();
                Platform.runLater(() -> {
                    if (alreadySelected == null) {
                        Main.gameManager.gameCreation_setRefereeASelected(refereeSelected);
                    }
                    else if (alreadySelected != refereeSelected) {
                        gameCreationRefereeBList = addReferee(alreadySelected, gameCreationRefereeBList);
                        updateRefereeComboBox(gameCreationRefereeBList, gameCreationRefereeBComboBox);
                        Main.gameManager.gameCreation_setRefereeASelected(refereeSelected);
                    }
                    gameCreationRefereeBList = removeReferee(refereeSelected, gameCreationRefereeBList);
                    updateRefereeComboBox(gameCreationRefereeBList, gameCreationRefereeBComboBox);
                });
            }
        });

        gameCreationTimeReportSpinner.getEditor().setText(Utilities.parseTime(gameCreationTimeSlider.getValue(), false));
        // End gameCreation set-up
    }

    private ObservableList<Team> addTeam(Team newTeam, ObservableList<Team> list) {
        ArrayList<Team> teams = new ArrayList<>(list);
        teams.add(newTeam);
        return FXCollections.observableArrayList(teams).sorted(Team.compareTeamNames());
    }

    private ObservableList<Team> removeTeam(Team teamToGo, ObservableList<Team> list) {
        ArrayList<Team> teams = new ArrayList<>();
        for (Team t : list) {
            if (t != teamToGo) {
                teams.add(t);
            }
        }
        return FXCollections.observableArrayList(teams);
    }

    private ObservableList<Referee> addReferee(Referee newReferee, ObservableList<Referee> list) {
        ArrayList<Referee> referees = new ArrayList<>(list);
        referees.add(newReferee);
        return FXCollections.observableArrayList(referees).sorted(Referee.compareRefereeNames());
    }

    private ObservableList<Referee> removeReferee(Referee refereeToGo, ObservableList<Referee> list) {
        ArrayList<Referee> referees = new ArrayList<>();
        for (Referee r : list) {
            if (r != refereeToGo) {
                referees.add(r);
            }
        }
        return FXCollections.observableArrayList(referees);
    }

    private void updateTeamComboBox(ObservableList<Team> teams, ComboBox<Team> comboBox) {
        comboBox.setItems(teams);
    }

    private void updateRefereeComboBox(ObservableList<Referee> referees, ComboBox<Referee> comboBox) {
        comboBox.setItems(referees);
    }

    private static void clearReportString() {
        reportString.delete(0, reportString.length());
    }

    private static void addToReportString(String s) {
        reportString.append(s);
    }

    public static String getReportString() {
        return reportString.toString();
    }


    public static Date gameCreation_getDate() {
        String dateText = gameCreationDatePicker.getEditor().getText().trim();
        String timeText = gameCreationTimeReportSpinner.getEditor().getText().trim();
        String dateTimeText = dateText + " " + timeText;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy KK:mm aa");//"EEE MMM dd hh:mm:ss zzz yyyy");
        Date date = null;
        try {
            date = sdf.parse(dateTimeText);
        } catch (ParseException e) {
            addToReportString("\ndate {" + dateTimeText + "} is unparseable.");
            e.printStackTrace();
        }
        return date;
    }

    public static Team gameCreation_getHomeTeam() {
        Team t = gameCreationHomeTeamComboBox.getValue();
        if (t == null) {
            addToReportString("\nSelect a home team.");
        }
        return t;
    }

    public static Team gameCreation_getAwayTeam() {
        Team t = gameCreationAwayTeamComboBox.getValue();
        if (t == null) {
            addToReportString("\nSelect an away team.");
        }
        return t;
    }

    public static Gym gameCreation_getGym() {
        Gym g = gameCreationGymComboBox.getValue();
        if (g == null) {
            addToReportString("\nSelect a gym.");
        }
        return g;
    }

    public static Referee gameCreation_getRefereeA() {
        Referee r = gameCreationRefereeAComboBox.getValue();
        if (r == null) {
            addToReportString("\nSelect referee A.");
        }
        return r;
    }

    public static Referee gameCreation_getRefereeB() {
        Referee r = gameCreationRefereeBComboBox.getValue();
        if (r == null) {
            addToReportString("\nSelect referee B.");
        }
        return r;
    }

    public void gameCreation_okButtonClicked(ActionEvent actionEvent) {
        GameCreationForm gcf = new GameCreationForm();
        gcf.collectAttributes();
        boolean validEntries = gcf.checkValid();
        Game game = null;
        if (validEntries) {
            game = gcf.createGame();
            addToReportString(game.toString());
        }
        else {
            addToReportString("\nCheck entries.");
        }
        gameCreation_showReportText(true, true);
    }

    public void gameCreation_clearButtonClicked(ActionEvent actionEvent) {
    }

    public void gameCreation_showReportText(boolean show, boolean clearString) {
        if (show) {
            gameCreationReportTextArea.setText(getReportString());
        }
        else {
            gameCreationReportTextArea.setText("");
        }
        if (clearString) {
            clearReportString();
        }
    }

    private void gameCreation_spinnerButton(ObservableValue<? extends Double> observableValue, Double oldValue, Double newValue) {
        String timeText = gameCreationTimeReportSpinner.getEditor().getText();
        String newTime = Utilities.addOneMinute(timeText);
        gameCreationTimeReportSpinner.getEditor().setText(newTime);
        double timeValue = Utilities.getTimeSliderValue(newTime);
        gameCreationTimeSlider.setValue(timeValue);
    }
}

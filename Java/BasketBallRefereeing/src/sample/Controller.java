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
import java.time.LocalDate;
import java.time.chrono.Chronology;
import java.util.ArrayList;
import java.util.Date;

/**
 * Global controller for all tabs.
 */

public class Controller {

//    @FXML public Button gameCreationOkButton;
//    @FXML public Button gameCreationClearButton;

    private static StringBuilder reportString;
    private String selectedString = "SELECTED";
    private String unSelectedString = "Not selected";

    // Game creation variables
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

    // Game History variables
    private static ToggleButton gameHistoryDateToggleButton;
    private static ToggleButton gameHistoryTimeToggleButton;
    private static ToggleButton gameHistoryGymToggleButton;
    private static ToggleButton gameHistoryHomeTeamToggleButton;
    private static ToggleButton gameHistoryAwayTeamToggleButton;
    private static ToggleButton gameHistoryRefereeAToggleButton;
    private static ToggleButton gameHistoryRefereeBToggleButton;

    private static ObservableList<TimeList> gameHistoryTimeList;
    private static ObservableList<Gym> gameHistoryGymsList;
    private static ObservableList<Team> gameHistoryAwayTeamsList;
    private static ObservableList<Team> gameHistoryHomeTeamsList;
    private static ObservableList<Referee> gameHistoryRefereeAList;
    private static ObservableList<Referee> gameHistoryRefereeBList;

    private static DatePicker gameHistoryDatePicker;
    private static Spinner<Double> gameHistoryOffsetSpinner;
    private static ComboBox<TimeList> gameHistoryTimeComboBox;
    private static ComboBox<Gym> gameHistoryGymComboBox;
    private static ComboBox<Team> gameHistoryHomeTeamComboBox;
    private static ComboBox<Team> gameHistoryAwayTeamComboBox;
    private static ComboBox<Referee> gameHistoryRefereeAComboBox;
    private static ComboBox<Referee> gameHistoryRefereeBComboBox;
    private static TextArea gameHistoryReportTextArea;

    public void init(Parent parent) {

        reportString = new StringBuilder();
        beginGameCreationSetUp(parent);
        beginGameHistorySetUp(parent);
    }

    private void beginGameCreationSetUp(Parent parent) {

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

    private void beginGameHistorySetUp(Parent parent) {

        // Begin gameHistory set-up
        gameHistoryTimeList = FXCollections.observableArrayList(TimeList.getValues()).sorted(TimeList.compareHours());
        gameHistoryGymsList = FXCollections.observableArrayList(Gym.getValues()).sorted(Gym.compareGymNames());
        gameHistoryAwayTeamsList = FXCollections.observableArrayList(Team.getValues()).sorted(Team.compareTeamNames());
        gameHistoryHomeTeamsList = FXCollections.observableArrayList(Team.getValues()).sorted(Team.compareTeamNames());
        gameHistoryRefereeAList = FXCollections.observableArrayList(Referee.getValues()).sorted(Referee.compareRefereeNames());
        gameHistoryRefereeBList = FXCollections.observableArrayList(Referee.getValues()).sorted(Referee.compareRefereeNames());

        gameHistoryDateToggleButton = (ToggleButton) parent.lookup("#game_history_date_toggleButton");
        gameHistoryTimeToggleButton = (ToggleButton) parent.lookup("#game_history_time_toggleButton");
        gameHistoryGymToggleButton = (ToggleButton) parent.lookup("#game_history_gym_toggleButton");
        gameHistoryHomeTeamToggleButton = (ToggleButton) parent.lookup("#game_history_home_team_toggleButton");
        gameHistoryAwayTeamToggleButton = (ToggleButton) parent.lookup("#game_history_away_team_toggleButton");
        gameHistoryRefereeAToggleButton = (ToggleButton) parent.lookup("#game_history_referee_A_toggleButton");
        gameHistoryRefereeBToggleButton = (ToggleButton) parent.lookup("#game_history_referee_B_toggleButton");

        gameHistoryDatePicker = (DatePicker) parent.lookup("#game_history_datePicker");
        gameHistoryOffsetSpinner = (Spinner<Double>) parent.lookup("#game_history_offset_spinner");
        gameHistoryTimeComboBox = (ComboBox<TimeList>) parent.lookup("#game_history_time_comboBox");
        gameHistoryGymComboBox = (ComboBox<Gym>) parent.lookup("#game_history_gym_comboBox");
        gameHistoryHomeTeamComboBox = (ComboBox<Team>) parent.lookup("#game_history_home_team_comboBox");
        gameHistoryAwayTeamComboBox = (ComboBox<Team>) parent.lookup("#game_history_away_team_comboBox");
        gameHistoryRefereeAComboBox = (ComboBox<Referee>) parent.lookup("#game_history_referee_A_comboBox");
        gameHistoryRefereeBComboBox = (ComboBox<Referee>) parent.lookup("#game_history_referee_B_comboBox");
        gameHistoryReportTextArea = (TextArea) parent.lookup("#game_history_report_textArea");

        gameHistoryTimeComboBox.setItems(gameHistoryTimeList);
        gameHistoryGymComboBox.setItems(gameHistoryGymsList);
        gameHistoryHomeTeamComboBox.setItems(gameHistoryHomeTeamsList);
        gameHistoryAwayTeamComboBox.setItems(gameHistoryAwayTeamsList);
        gameHistoryRefereeAComboBox.setItems(gameHistoryRefereeAList);
        gameHistoryRefereeBComboBox.setItems(gameHistoryRefereeBList);

        gameHistoryDateToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryDateToggleButton.isSelected();
                if (isDown) {
                    gameHistoryDateToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryDateToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryTimeToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryTimeToggleButton.isSelected();
                if (isDown) {
                    gameHistoryTimeToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryTimeToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryGymToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryGymToggleButton.isSelected();
                if (isDown) {
                    gameHistoryGymToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryGymToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryHomeTeamToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryHomeTeamToggleButton.isSelected();
                if (isDown) {
                    gameHistoryHomeTeamToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryHomeTeamToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryAwayTeamToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryAwayTeamToggleButton.isSelected();
                if (isDown) {
                    gameHistoryAwayTeamToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryAwayTeamToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryRefereeAToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryRefereeAToggleButton.isSelected();
                if (isDown) {
                    gameHistoryRefereeAToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryRefereeAToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryRefereeBToggleButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent event) {
                boolean isDown = gameHistoryRefereeBToggleButton.isSelected();
                if (isDown) {
                    gameHistoryRefereeBToggleButton.setText(selectedString);
                }
                else {
                    gameHistoryRefereeBToggleButton.setText(unSelectedString);
                }
            }
        });

        gameHistoryOffsetSpinner.setValueFactory(new SpinnerValueFactory<Double>() {
            @Override
            public void decrement(int steps) {
                double st = steps / 100.0;
                double v = Double.parseDouble(gameHistoryOffsetSpinner.getEditor().getText());
                double x = Math.max(0.0, (v - st));
                String s = Utilities.twoDecimals(x);
                gameHistoryOffsetSpinner.getEditor().setText(s);
            }

            @Override
            public void increment(int steps) {
                double st = steps / 100.0;
                double v = Double.parseDouble(gameHistoryOffsetSpinner.getEditor().getText());
                double x = Math.min(1.0, (v + st));
                String s = Utilities.twoDecimals(x);
                gameHistoryOffsetSpinner.getEditor().setText(s);

            }
        });
        gameHistoryDatePicker.setValue(LocalDate.now());
        gameHistoryOffsetSpinner.getEditor().setText("0.00");
        // End gameHistory set-up
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

    public void selectToggleButton(ToggleButton t) {
        t.setSelected(true);
        t.setText(selectedString);
    }

    public void unSelectToggleButton(ToggleButton t) {
        t.setSelected(false);
        t.setText(unSelectedString);
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


    public static Date gameHistory_getDate() {
        String dateText = gameHistoryDatePicker.getEditor().getText().trim();
        TimeList timeListText = gameHistoryTimeComboBox.getValue();
        String timeText;
        if (timeListText == null) {
            timeText = TimeList._05_00_PM.getName();
        }
        else {
            timeText = timeListText.getTimeString();
        }
        String dateTimeText = dateText + " " + timeText;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm");//"EEE MMM dd hh:mm:ss zzz yyyy");
        System.out.println("sdf.toPattern: " + sdf.toPattern() + ", sdf.toString: " + sdf.toString());
        Date date = null;
        try {
            date = sdf.parse(dateTimeText);
        } catch (ParseException e) {
            addToReportString("\ndate {" + dateTimeText + "} is unparseable.");
            gameHistory_showReportText(true, true);
            e.printStackTrace();
        }
        System.out.println("GameHistory_getDate, dateTimeText: " + dateTimeText + ", date: " + date);
        return date;
    }

    public static double gameHistory_getOffset() {
        return Double.parseDouble(gameHistoryOffsetSpinner.getEditor().getText());
    }

    public static Team gameHistory_getHomeTeam() {
        Team t = gameHistoryHomeTeamComboBox.getValue();
        boolean b = gameHistoryHomeTeamToggleButton.isSelected();
        if (b && t == null) {
            addToReportString("\nSelect a home team.");
        }
        return t;
    }

    public static Team gameHistory_getAwayTeam() {
        Team t = gameHistoryAwayTeamComboBox.getValue();
        boolean b = gameHistoryAwayTeamToggleButton.isSelected();
        if (b && t == null) {
            addToReportString("\nSelect an away team.");
        }
        return t;
    }

    public static Gym gameHistory_getGym() {
        Gym g = gameHistoryGymComboBox.getValue();
        boolean b = gameHistoryGymToggleButton.isSelected();
        if (b && g == null) {
            addToReportString("\nSelect a gym.");
        }
        return g;
    }

    public static Referee gameHistory_getRefereeA() {
        Referee r = gameHistoryRefereeAComboBox.getValue();
        boolean b = gameHistoryRefereeAToggleButton.isSelected();
        if (b && r == null) {
            addToReportString("\nSelect referee A.");
        }
        return r;
    }

    public static Referee gameHistory_getRefereeB() {
        Referee r = gameHistoryRefereeBComboBox.getValue();
        boolean b = gameHistoryRefereeBToggleButton.isSelected();
        if (b && r == null) {
            addToReportString("\nSelect referee B.");
        }
        return r;
    }

    public static Date gameCreation_getDate() {
        String dateText = gameCreationDatePicker.getEditor().getText().trim();
        String timeText = gameCreationTimeReportSpinner.getEditor().getText().trim();
//        if (dateText.equals("")) {
//        }
        String dateTimeText = (dateText + " " + timeText).trim();
        System.out.println("dateText: " + dateText + ", timeText: " + timeText + ", dateTimeText: " + dateTimeText);
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

    public static boolean gameHistory_getDateFilterStatus() {
        return gameHistoryDateToggleButton.isSelected();
    }

    public static boolean gameHistory_getTimeFilterStatus() {
        return gameHistoryTimeToggleButton.isSelected();
    }

    public static boolean gameHistory_getGymFilterStatus() {
        return gameHistoryGymToggleButton.isSelected();
    }

    public static boolean gameHistory_getHomeTeamFilterStatus() {
        return gameHistoryHomeTeamToggleButton.isSelected();
    }

    public static boolean gameHistory_getAwayTeamFilterStatus() {
        return gameHistoryAwayTeamToggleButton.isSelected();
    }

    public static boolean gameHistory_getRefereeAFilterStatus() {
        return gameHistoryRefereeAToggleButton.isSelected();
    }

    public static boolean gameHistory_getRefereeBFilterStatus() {
        return gameHistoryRefereeBToggleButton.isSelected();
    }

    // Showing report string for each tab
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

    public static void gameHistory_showReportText(boolean show, boolean clearString) {
        if (show) {
            gameHistoryReportTextArea.setText(getReportString());
        }
        else {
            gameHistoryReportTextArea.setText("");
        }
        if (clearString) {
            clearReportString();
        }
    }

    // Main button handlers for all tabs
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
        gameCreationDatePicker.getEditor().setText("");
        gameCreationTimeSlider.setValue(17.0); // default 5 PM
        String timeText = Utilities.parseTime(gameCreationTimeSlider.getValue(), true);
        gameCreationTimeReportSpinner.getEditor().setText(timeText);
        gameCreationGymComboBox.getSelectionModel().clearSelection();
        gameCreationHomeTeamComboBox.getSelectionModel().clearSelection();
        gameCreationAwayTeamComboBox.getSelectionModel().clearSelection();
        gameCreationRefereeAComboBox.getSelectionModel().clearSelection();
        gameCreationRefereeBComboBox.getSelectionModel().clearSelection();
        gameCreation_showReportText(false, true);
    }

    public void gameHistory_graphButtonClicked(ActionEvent actionEvent) {
        System.out.println("gameHistory graph button clicked");
        GameHistoryForm ghf = new GameHistoryForm();
        ghf.collectAttributes();
        boolean validEntries = ghf.checkValid() || ghf.checkSelectionValidity();
//        Game game = null;
        if (validEntries) {
//            game = gcf.createGame();
//            addToReportString(game.toString());
            System.out.println("ALL VALID");
            System.out.println(
                    "filtered games: " + ghf.getFilteredGames() +
                     "\n\tSIZE: " + ghf.getFilteredGames().size());
            addToReportString(ghf.getFilteredGames().toString());
        }
        else {
            addToReportString("\nCheck entries.");
        }
        gameHistory_showReportText(true, true);
    }

    public void gameHistory_clearTogglesButtonClicked(ActionEvent actionEvent) {
        System.out.println("gameHistory clear toggles button clicked");
        unSelectToggleButton(gameHistoryDateToggleButton);
        unSelectToggleButton(gameHistoryTimeToggleButton);
        unSelectToggleButton(gameHistoryGymToggleButton);
        unSelectToggleButton(gameHistoryHomeTeamToggleButton);
        unSelectToggleButton(gameHistoryAwayTeamToggleButton);
        unSelectToggleButton(gameHistoryRefereeAToggleButton);
        unSelectToggleButton(gameHistoryRefereeBToggleButton);
    }

    public void gameHistory_clearAllButtonClicked(ActionEvent actionEvent) {
        System.out.println("gameHistory clear all button clicked");
        gameHistory_clearTogglesButtonClicked(actionEvent);
        gameHistoryDatePicker.setValue(LocalDate.now());
        gameHistoryOffsetSpinner.getEditor().setText("0.00");
        gameHistoryTimeComboBox.getSelectionModel().clearSelection();
        gameHistoryGymComboBox.getSelectionModel().clearSelection();
        gameHistoryHomeTeamComboBox.getSelectionModel().clearSelection();
        gameHistoryAwayTeamComboBox.getSelectionModel().clearSelection();
        gameHistoryRefereeAComboBox.getSelectionModel().clearSelection();
        gameHistoryRefereeBComboBox.getSelectionModel().clearSelection();
    }
}

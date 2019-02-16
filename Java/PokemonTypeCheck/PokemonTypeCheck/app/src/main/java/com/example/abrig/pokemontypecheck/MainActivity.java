package com.example.abrig.pokemontypecheck;

import android.os.Handler;
import android.renderscript.RenderScript;
import android.support.design.widget.TextInputLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.HashSet;

public class MainActivity extends AppCompatActivity {

    protected String user_input = "";
    protected String checkStringName = "";
    protected String[] allTypes = {"Normal","Fight","Flying","Poison","Ground","Rock","Bug",
            "Ghost","Steel","Fire","Water","Grass","Electric",
            "Psychic","Ice","Dragon","Dark","Fairy"};
    // each row corresponds to a type. The first column
    // identifies the type for that row, each type after
    // column 1, is a type that would be a good match up
    // for the row-type.
    // I.E. Fighting type attackS will be super effective
    // against Ice or Dark types
    protected String[][] strongATTK =
            {{"Normal"},
                    {"Fight","Normal","Rock","Steel","Ice","Dark"},
                    {"Flying","Fight","Bug","Grass"},
                    {"Poison","Grass"},
                    {"Ground","Poison","Rock","Steel","Fire","Electric"},
                    {"Rock","Flying","Bug","Fire","Ice"},
                    {"Bug","Grass","Psychic","Dark"},
                    {"Ghost","Ghost","Psychic"},
                    {"Steel","Rock","Ice"},
                    {"Fire","Bug","Steel","Grass","Ice"},
                    {"Water","Ground","Rock","Fire"},
                    {"Grass","Ground","Rock","Water"},
                    {"Electric","Flying","Water"},
                    {"Psychic","Fight","Poison"},
                    {"Ice","Flying","Ground","Grass","Dragon"},
                    {"Dragon","Dragon"},
                    {"Dark","Ghost","Psychic"},
                    {"Fairy","Fight","Dragon","Dark"}};

    // each row corresponds to a type. The first column
// identifies the type for that row, each type after
// column 1, is a type that would be a good match up
// for the row-type.
// I.E. Fighting type DEFENCE will be super effective
// against Bug or Dark types
    protected String[][] strongDEF =
            {{"Normal"},
                    {"Fight","Rock","Bug","Dark"},
                    {"Flying","Fight","Bug","Grass"},
                    {"Poison","Fight","Poison","Bug","Grass"},
                    {"Ground","Poison","Rock"},
                    {"Rock","Normal","Flying","Poison","Fire"},
                    {"Bug","Fight","Ground","Grass"},
                    {"Ghost","Poison","Bug"},
                    {"Steel","Normal","Flying","Rock","Bug","Ghost","Steel",
                            "Grass","Psychic","Ice","Dragon","Dark"},
                    {"Fire","Bug","Steel","Fire","Grass","Ice"},
                    {"Water","Steel","Fire","Water","Ice"},
                    {"Grass","Ground","Water","Grass","Electric"},
                    {"Electric","Flying","Steel","Electric"},
                    {"Psychic","Fight","Psychic"},
                    {"Ice","Ice"},
                    {"Dragon","Fire","Water","Grass","Electric"},
                    {"Dark","Ghost","Dark"},
                    {"Fairy","Poison","Steel"}};

    protected String[][] allPokemon;
    protected Spelling corrector;
    protected Handler mainHandler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        allPokemon = parseCSV();
        allPokemon = capitalizeTypeNames(allPokemon);
        try {
            corrector = new Spelling(allPokemon);
        } catch (IOException e) {
            //e.printStackTrace();
        }
        final TextView resultsMessageDisplay = (TextView) findViewById(R.id.results_window);
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                mainHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        resultsMessageDisplay.setText("Beginning: " + allPokemon[0][0] + "\n" + allPokemon[908][0]);
                    }
                });
            }
        };
    }

    public String[] bestTypes(String[][] types, String[] currPokemonTypes){
        String[] result = new String[0];
        // loop current pokemon types
        for(int i = 0; i < currPokemonTypes.length; i++){
            // loop 2D array looking at the first column
            for (String[] type : types) {
                // if the types match record all other types in that row
                if (type[0].equals(currPokemonTypes[i])) {
                    int size = type.length - 1;
                    int resSize = result.length;
                    int l, k = 0;
                    String[] temp = new String[resSize + size];
                    // first type
                    if (i == 0) {
                        for (l = 1; l < size + 1; l++, k++) {
                            temp[k] = type[l];
                        }
                    }
                    // more than one type
                    else {
                        for (k = 0; k < resSize; k++) {
                            temp[k] = result[k];
                        }
                        for (l = 1; l < size + 1; l++, k++) {
                            temp[k] = type[l];
                        }
                    }
                    result = temp;
                }
            }
        }
        // remove all duplicate types accumulated
        result = removeDuplicates(result);
        return result;
    }


    /*
     * removeDuplicates takes in an array of strings, and returns a
     * new array of every unique string in the original array.
     */
    public String[] removeDuplicates(String[] arr){
        return new HashSet<String>(Arrays.asList(arr)).toArray(new String[0]);
    }

    public String[] decipher(String line, String[] types){
        String[] result = new String[1];
        boolean earlyExit = true;
        int len = line.length(), curr = 0;
        earlyExit = len > 15;
        earlyExit = earlyExit || (!line.contains(",") && len > 8);
        if(earlyExit){ // earlyExit conditions met
            return result;
        }
        String typeToAdd = "";
        int i;
        for(i = 0; i < len; i++){
            if(line.charAt(i) != ',' && line.charAt(i) != ' '){
                typeToAdd += line.charAt(i);
            }
            if(line.charAt(i) == ',' || i == len-1){
                if(curr > 0){
                    String[] arr = new String[result.length+1];
                    System.arraycopy(result, 0, arr, 0, result.length);
                    result = arr;
                }
                for (String type : types) {
                    if (type.equals(typeToAdd)) {
                        result[curr] = typeToAdd;
                        curr++;
                        break;
                    }
                }
                typeToAdd = "";
            }
        }
        return result;
    }

    public void typeRadioButtonClicked(View view){
        boolean checked = ((RadioButton) view).isChecked();
        String str = user_input;
        String temp = str;
        int count = temp.length() - temp.replace(",", "").length();
        if(!checkStringName.equals("")){
            checkStringName = "";
            user_input = "";
        }
        // Check which radio button was clicked
        if(count >= 2){
            str = "";
            user_input = str;
        }
        switch(view.getId()) {
            case R.id.radioButton_NormalType:
                if(checked)
                    str += "Normal,";
                break;
            case R.id.radioButton_FightType:
                if(checked)
                    str += "Fight,";
                break;
            case R.id.radioButton_FlyingType:
                if(checked)
                    str += "Flying,";
                break;
            case R.id.radioButton_PoisonType:
                if(checked)
                    str += "Poison,";
                break;
            case R.id.radioButton_GroundType:
                if(checked)
                    str += "Ground,";
                break;
            case R.id.radioButton_RockType:
                if(checked)
                    str += "Rock,";
                break;
            case R.id.radioButton_BugType:
                if(checked)
                    str += "Bug,";
                break;
            case R.id.radioButton_GhostType:
                if(checked)
                    str += "Ghost,";
                break;
            case R.id.radioButton_SteelType:
                if(checked)
                    str += "Steel,";
                break;
            case R.id.radioButton_FireType:
                if(checked)
                    str += "Fire,";
                break;
            case R.id.radioButton_WaterType:
                if(checked)
                    str += "Water,";
                break;
            case R.id.radioButton_GrassType:
                if(checked)
                    str += "Grass,";
                break;
            case R.id.radioButton_ElectricType:
                if(checked)
                    str += "Electric,";
                break;
            case R.id.radioButton_PsychicType:
                if(checked)
                    str += "Psychic,";
                break;
            case R.id.radioButton_IceType:
                if(checked)
                    str += "Ice,";
                break;
            case R.id.radioButton_DragonType:
                if(checked)
                    str += "Dragon,";
                break;
            case R.id.radioButton_DarkType:
                if(checked)
                    str += "Dark,";
                break;
            case R.id.radioButton_FairyType:
                if(checked)
                    str += "Fairy,";
                break;
        }
        temp = str;
        count = temp.length() - temp.replace(",", "").length();
        if(count <= 2){
            user_input = str;
        }
        Toast.makeText(getApplicationContext(), str, Toast.LENGTH_SHORT).show();
    }

    public void submitButtonClicked(View view) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                mainHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        TextView resultsMessageDisplay = (TextView) findViewById(R.id.results_window);
                        TextInputLayout pokemonNameEditText = findViewById(R.id.pokemon_name_editText);
                        String nameInput = pokemonNameEditText.getEditText().getText().toString().trim();
                        String[] nameInputArray = decipherName(nameInput);
                        StringBuilder result = new StringBuilder();
                        result.append(nameInputArray[0]).append(" < name\n");
                        String namedPokemonTypes;
                        Boolean properNameGiven = false;
                        if(user_input.equals((checkStringName))) {
                           user_input = "";
                        }
                        if (!nameInput.equals("")) {
                            namedPokemonTypes = typesFromNameFromInput(nameInputArray[0]); // take in a string, give a string, (use commas will decipher the result)
                            if (!namedPokemonTypes.equals("")) {
                                properNameGiven = true;
                                user_input = namedPokemonTypes;
                                if(user_input.equals((checkStringName))) {
                                    user_input = "";
                                    result.append("Nothing Entered!");
                                    resultsMessageDisplay.setText(result);
                                    pokemonNameEditText.getEditText().setText("");
                                    return;
                                }
                                checkStringName = user_input;
                                String[] typeInput = decipher(namedPokemonTypes, allTypes);
                                typeInput = capitalizeStringArray(typeInput);
                                result.append("Input: \n").append(user_input).append("\n");
                                result.append("Best types to fight against:\n");
                                typeInput = bestTypes(strongATTK, typeInput);
                                for (String type : typeInput) {
                                    //if(!type.equals("None")) {
                                    result.append(type).append(", ");
                                    // }
                                }
                            } else {
                                result.append("Try again");
                                properNameGiven = true;
                            }
                        }
                        if (!properNameGiven) {
                            if (user_input.length() == 0) {
                                result.append("Nothing Entered!");
                            } else {
                                result.append("Input: \n").append(user_input).append("\n");
                                String[] input = decipher(user_input, allTypes);
                                input = bestTypes(strongATTK, input);
                                result.append("Best types to fight against:\n");
                                for (String type : input) {
                                    result.append(type).append(", ");
                                }
                            }
                        }
                        resultsMessageDisplay.setText(result);
                    }
                });
            }
        };
        Thread myThread = new Thread(runnable);
        myThread.start();
    }

    private String[] decipherName(String name) {

        String[] result = new String[1];
        boolean earlyExit;
        int len = name.length();
        earlyExit = len > 15;
        if(earlyExit){ // earlyExit conditions met
            return result;
        }
        int i;
        StringBuilder nameBuilder = new StringBuilder();
        for(i = 0; i < len; i++) {
            if (i == 0) {
                nameBuilder.append(Character.toUpperCase(name.charAt(i)));
            } else {
                nameBuilder.append(name.charAt(i));
            }
        }
        name = nameBuilder.toString();
        result[0] = corrector.correct(name);
        result = capitalizeStringArray(result);
        return result;
    }

    private String typesFromNameFromInput(String nameInput) {
        StringBuilder result = new StringBuilder();
        //ameInput = corrector.correct(nameInput);
        for(int i = 0; i < allPokemon.length; i++){
            if(allPokemon[i][0].equals(nameInput)){
                String secondType = ((allPokemon[i][2].equals("None")? "" : allPokemon[i][2]));
                result.append(allPokemon[i][1]).append(",").append(secondType);
                break;
            }
        }
        String line = result.toString();
        if(line.length() == 0){
            return "";
        }
        else {
            TextView resultsMessageDisplay = (TextView) findViewById(R.id.results_window);
            resultsMessageDisplay.setText("Processing");
            //return corrector.correct(line); // ?????????????
            return line;
        }
    }

    public String[][] parseCSV() {
        String line;
        String[][] pokemonArr = new String[908][1];
        InputStream inputStream = getResources().openRawResource(R.raw.pokedex);
        BufferedReader br = null;
        int curr = 0;
        try {
            br = new BufferedReader(new InputStreamReader(inputStream));
            while ((line = br.readLine()) != null) {
                // use comma as separator
                String[] pokemon = line.split(",");
                pokemonArr[curr] = pokemon;
                curr++;
            }

        } catch (FileNotFoundException e) {
            //e.printStackTrace();
        } catch (IOException e) {
            //e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    //e.printStackTrace();
                }
            }
        }
        return pokemonArr;
    }

    private String[][] capitalizeTypeNames(String[][] arr) {
        int i, j, k;
        for(i = 0; i < arr.length; i++){
            for(j = 0; j < arr[i].length; j++){
                char firstLetter = Character.toUpperCase(arr[i][j].charAt(0));
                StringBuilder line = new StringBuilder(Character.toString(firstLetter));
                for(k = 1; k < arr[i][j].length(); k++){
                    line.append(Character.toString(arr[i][j].charAt(k)));
                }
                arr[i][j] = line.toString();
            }
        }
        return arr;
    }



    private String[] capitalizeStringArray(String[] arr) {
        int j = 0, k;
        for(String item : arr){
            if(item == null){
                item = "";
            }
            int size = item.length();
            if(size > 0) {
                char firstLetter = Character.toUpperCase(item.charAt(0));
                StringBuilder line = new StringBuilder(Character.toString(firstLetter));
                for (k = 1; k < size; k++) {
                    line.append(Character.toString(item.charAt(k)));
                }
                item = line.toString();
            }
            else{
                item =  "";
            }
            arr[j] = item;
            j++;
        }
        return arr;
    }

}

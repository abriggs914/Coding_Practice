package com.example.abrig.forbiddenmemoriesaid;

import android.content.Context;
import android.widget.Toast;

import static android.widget.Toast.LENGTH_LONG;

public class UserInput {

    public void method1(){
        String line = "Hey there";
        Context context = this;
        Toast.makeText(UserInput.this, line, Toast.LENGTH_LONG).show();
    }
}

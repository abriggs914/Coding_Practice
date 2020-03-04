package com.example.abrig.minesweeper;

import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatDialogFragment;
import android.view.LayoutInflater;
import android.view.View;

public class QuitGamePopUp extends AppCompatDialogFragment {

    private boolean keepPlaying, resetGame;
    private ExampleDialogListener listener;

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater layoutInflater = getActivity().getLayoutInflater();
        View view = layoutInflater.inflate(R.layout.quit_game_pop_up, null);
        builder.setView(view)
                .setTitle("Quit?")
                .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        keepPlaying = true;
                        resetGame = false;
                        listener.applyTexts(keepPlaying, resetGame);
                    }
                })
                .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        keepPlaying = false;
                        resetGame = false;
                        listener.applyTexts(keepPlaying, resetGame);
                    }
                })
                .setNeutralButton("reset", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        keepPlaying = false;
                        resetGame = true;
                        listener.applyTexts(keepPlaying, resetGame);
                    }
                });
        return builder.create();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        try {
            listener = (ExampleDialogListener) context;
        }
        catch (ClassCastException e) {
            throw new ClassCastException(context + " must implement ClassCastException");
        }
    }

    public interface ExampleDialogListener {
        void applyTexts(boolean keepPlaying, boolean resetGame);
    }
}

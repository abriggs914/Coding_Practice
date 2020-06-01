package com.example.abrig.spendinglog;

import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatDialogFragment;
import android.view.LayoutInflater;
import android.view.View;

public class AddFiltersDialog extends AppCompatDialogFragment {

    // types of filters:

    //          Priority
    // entity           (sender / receiver)
    // transaction type

    //          Secondary
    // date             (start / on / end)
    // amount           (range / window)

    //          Late additions
    // re-occurring
    // same cycle       (is re-occurring on a set interval (may need a date...))

    private boolean keepPlaying, shuffleGrid, resetGame;
    private ExampleDialogListener listener;

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater layoutInflater = getActivity().getLayoutInflater();
        View view = layoutInflater.inflate(R.layout.add_filters_pop_up, null);
        builder.setView(view)
                .setTitle("Quit?");
        builder.setItems(new CharSequence[]
                        {"ok", "shuffle", "reset", "cancel"},
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        // The 'which' argument contains the index position
                        // of the selected item
                        switch (which) {
                            case 0:
                                // ok button
                                keepPlaying = false;
                                shuffleGrid = false;
                                resetGame = false;
                                listener.applyTexts(keepPlaying, shuffleGrid, resetGame);
                                break;
                            case 1:
                                // shuffle button
                                keepPlaying = false;
                                shuffleGrid = true;
                                resetGame = false;
                                listener.applyTexts(keepPlaying, shuffleGrid, resetGame);
                                break;
                            case 2:
                                // reset button
                                keepPlaying = false;
                                shuffleGrid = false;
                                resetGame = true;
                                listener.applyTexts(keepPlaying, shuffleGrid, resetGame);
                                break;
                            case 3:
                                // cancel button
                                keepPlaying = true;
                                shuffleGrid = false;
                                resetGame = false;
                                listener.applyTexts(keepPlaying, shuffleGrid, resetGame);
                                break;
                        }
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

    // collect and return filter information
    public interface ExampleDialogListener {
        void applyTexts(boolean keepPlaying, boolean shuffleGrid, boolean resetGame);
    }
}

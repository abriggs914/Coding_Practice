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

    private String filterString = "00000000";
    private ExampleDialogListener listener;

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        final AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater layoutInflater = getActivity().getLayoutInflater();
        View view = layoutInflater.inflate(R.layout.add_filters_pop_up, null);
        final char[] arr = filterString.toCharArray();
        final char checked = '1';
        builder.setView(view)
                .setTitle("Add a filter:");
        builder.setItems(Utilities.possibleFilters,
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        // The 'which' argument contains the index position
                        // of the selected item
                        switch (which) {
                            case 0:
                                // By Entity
                                arr[0] = checked;
                                break;
                            case 1:
                                // By Sender
                                arr[1] = checked;
                                break;
                            case 2:
                                // By Recipient
                                arr[2] = checked;
                                break;
                            case 3:
                                // By Transaction Type
                                arr[3] = checked;
                                break;
                            case 4:
                                // By Start Date
                                arr[4] = checked;
                                break;
                            case 5:
                                // By Current Date
                                arr[5] = checked;
                                break;
                            case 6:
                                // By End Date
                                arr[6] = checked;
                                break;
                            case 7:
                                // By Amount Range
                                arr[7] = checked;
                                break;
                        }
                        filterString = new String(arr);
                        listener.applyTexts(filterString);

                    }
                });
//        getTargetFragment().onActivityResult(getTargetRequestCode(), 1, null);
        return builder.create();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        // Verify that the host activity implements the callback interface
        try {
            // Instantiate the EditNameDialogListener so we can send events to the host
            listener = (ExampleDialogListener) getTargetFragment();
        } catch (ClassCastException e) {
            // The activity doesn't implement the interface, throw exception
            throw new ClassCastException(getActivity().toString()
                    + " must implement EditNameDialogListener");
        }
    }

    // collect and return filter information
    public interface ExampleDialogListener {
        void applyTexts(String filterString);
    }
}

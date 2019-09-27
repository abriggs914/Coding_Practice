package com.example.abrig.tictactoeapp;

public class TicTacToeException extends Exception {
    public TicTacToeException(int code){
        switch(code) {
            case    1:  errorInAIMoveException();
                        break;
            default  :  unkownErrorException();
                        break;
        }
    }

    private void unkownErrorException() {
        System.out.println("UNKNOWN ERROR occurred");
    }

    private void errorInAIMoveException() {
        System.out.println("AI is struggling with their answer");
    }
}

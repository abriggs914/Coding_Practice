package com.example.abrig.forbiddenmemoriesaid;

public class CardException extends Exception{

    public CardException(String message){
        System.out.println(message);
        if(message.equals("HORB")){
            HORBException();
        }
        else if(message.equals("SSUC")){
            starSignCaseUnCaught();
        }
        else if(message.equals("IVSS")){
            invalidStarSignAssignment();
        }
        else if(message.equals("UNKC")){
            unknownCardEncountered();
        }
        System.out.println("Exception constructor");
    }

    public void invalidStarSignAssignment(){
        System.out.println("Invalid Star sign given for board assignment");
    }

    public void unknownCardEncountered(){
        System.out.println("Given an unknown card");
    }


    public void starSignCaseUnCaught(){
        System.out.println("Reached end of starSign evalulator with uncaught case.");
    }

    public void HORBException(){
        System.out.println("Invalid card status identifier entered");
    }

}


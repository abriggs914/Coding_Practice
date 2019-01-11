import java.util.Timer;
import java.util.TimerTask;

/**
 * Simple demo that uses java.util.Timer to schedule a task 
 * to execute once 5 seconds have passed.
 */

public class Reminder{
    Timer timer;
	
    public Reminder(int seconds) {
        timer = new Timer();
        timer.schedule(new RemindTask(), seconds*1500);
	}

    class RemindTask extends TimerTask {
        public void run() {
            //System.out.println("Time's up!");
            timer.cancel(); //Terminate the timer thread
        }
    }

    public static void main(String args[]) {
        new Reminder(1);
        //System.out.println("Task scheduled.");
    }
	
	public void wait(int n){
		int timeToWait = n; //second
        //System.out.print("Scanning");
        try{
            for (int i=0; i<timeToWait ; i++) {
                Thread.sleep(1000);
                System.out.print(".");
            }
			
            System.out.print("\n");
        }
		catch (InterruptedException ie){
            Thread.currentThread().interrupt();
        }
	}
}
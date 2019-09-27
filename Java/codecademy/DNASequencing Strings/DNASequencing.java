// LEARN JAVA
// DNA Sequencing
// The genome of an organism stores all the genetic information necessary to build and maintain that organism. It is an
// organism’s complete set of DNA.

// DNA is composed of a series of nucleotides abbreviated as:

// A: Adenine
// C: Cytosine
// G: Guanine
// T: Thymine
// DNA
// So a strand of DNA could look something like ACGAATTCCG.

// Write a DNA.java program that determines whether there is a protein in a strand of DNA.

// A protein has the following qualities:

// It begins with a \"start codon\": ATG.
// It ends with a \"stop codon\": TGA.
// In between, each additional codon is a sequence of three nucleotides.
// So for example:

// ATGCGATACTGA is a protein because it has the start codon ATG, the stop codon TGA, and the length is divisible
// by by 3.
// ATGCGATAGA is not a protein because the sequence length is not divisible by 3, so the third condition is not
// satisfied.
// Tasks
// 12/13Complete
// Mark the tasks as complete by checking them off
// String methods:
// 1.
// string methods	value
// length()	returns the length
// concat()	concatenates two strings
// equals()	checks for equality between two strings
// indexOf()	returns the index of a substring
// charAt()	returns a character
// substring()	returns a substring
// toUpperCase()	returns the upper case version
// toLowerCase()	returns the lower case version

// Note: Scroll through the table to see each method.

// You don’t need to use all the string methods in this project.

// Setting up:
// 2.
// Let’s create a skeleton for the program. Add the following into DNA.java:

// public class DNA {

//   public static void main(String[] args) {

//     //  -. .-.   .-. .-.   .
//     //    \   \ /   \   \ / 
//     //   / \   \   / \   \  
//     //  ~   `-~ `-`   `-~ `-

//   }

// }
// The main() is the main method that houses your program.

// 3.
// Write a comment near the top of the program that describe what the program does.

// // DNA Sequencing
// 4.
// Here are the three DNA strands that you are going to use to test your program:

// "ATGCGATACGCTTGA"
// "ATGCGATACGTGA"
// "ATTAATATGTACTGA"
// Store them in different strings: dna1, dna2, and dna3.

// String dna1 = "ATGCGATACGCTTGA";
// String dna2 = "ATGCGATACGTGA";
// String dna3 = "ATTAATATGTACTGA";
// Find the length:
// 5.
// Create a generic String variable called dna that can be set to any DNA sequence (dna1, dna2, dna3).

// If you want to test with dna1:

// String dna = dna1;
// 6.
// To warm up, find the length of the dna string.

// // Find the length:
// int length = dna.length();
// System.out.println("Length: " + length);
// Find the start codon and stop codon:
// 7.
// Remember that a protein has the following qualities:

// It begins with a start codon ATG.
// It ends with a stop codon TGA.
// In between, the number of nucleotides is divisible by 3.
// First, let’s start with the first condition. Does the DNA strand have the start codon ATG within it?

// Find the index where ATG begins using indexOf().

// // Find start codon: 
// int start = dna.indexOf("ATG");
// System.out.println("Start: " + start);
// If ATG is a substring, this would print out an index. If it’s not, this would print out -1.

// 8.
// Next, does the DNA strand have the stop codon TGA?

// Find the index where TGA begins.

// // Find stop codon:
// int stop = dna.indexOf("TGA");
// System.out.println("Stop: " + stop);
// If TGA is a substring, this would print out an index. If it’s not, this would print out -1.

// Find the protein:
// 9.
// Lastly, you’ll find out whether or not there is a protein!

// Let’s start with an if statement that checks for a start codon and a stop codon using the && operator.

// Remember that the indexOf() string method will return -1 if the substring doesn’t exist within a String.

// if (start != -1 && stop != -1) {

//   System.out.println("Condition 1 and 2 are satisfied.");

// }
// Condition 1: start != -1
// Condition 2: stop != -1
// 10.
// Add a third condition that checks whether or not that the number of nucleotides in between the start codon and
// the stop condon is a multiple of 3.

// Remember that the modolo operator % returns the remainder of a division.

// if (start != -1 && stop != -1 && (stop - start) % 3 == 0) {

//   System.out.println("Condition 1 and 2 and 3 are satisfied.");

// }
// Condition 1: start != -1
// Condition 2: stop != -1
// Condition 3: (stop - start) % 3 == 0
// 11.
// Inside the if statement, create a String variable named protein.

// And find this protein in the dna by using the substring() string method. Think about where you want the substring
// to begin and where you want the substring to end.

// Remember that a codon is 3 nucleotides long.

// if (start != -1 &&
//     stop != -1 &&
//     (stop - start) % 3 == 0) {

//   String protein = dna.substring(start, stop+3); 
//   System.out.println("Protein: " + protein);

// }
// Here, we are able to extract the substring from the index start to the end of the protein, which is at index
// stop + 3.

// 12.
// Add an else clause that print out No protein..

// if (start != -1 &&
//     stop != -1 &&
//     (stop - start) % 3 == 0) {

//     String protein = dna.substring(start, stop+3); 
//     System.out.println("Protein: " + protein);

// } else {

//     System.out.println("No protein.");

// }
// 13.
// You are all done!

// Let’s test your code with each DNA strand. These should be the results:

// dna1: Protein.
// dna2: Not a protein.
// dna3: Not a protein.
// Change the dna to dna2 and dna3 to check them.

// DNA Sequencing
public class DNASequencing {
  public static String dna1 = "ATGCGATACGCTTGA";
  public static String dna2 = "ATGCGATACGTGA";
  public static String dna3 = "ATTAATATGTACTGA";
  
  public static void main(String[] args) {

    //  -. .-.   .-. .-.   .
    //    \   \ /   \   \ / 
    //   / \   \   / \   \  
    //  ~   `-~ `-`   `-~ `-

    String dna = dna1;
    System.out.println(dna.length());
    System.out.println("dna1 :\t" + isProtein(dna1));
    System.out.println("dna2 :\t" + isProtein(dna2));
    System.out.println("dna3 :\t" + isProtein(dna3));
  }
  
  public static String isProtein(String sequence) {
    if (sequence.substring(0, 3).equals("ATG")){
      int start = sequence.length() - 3;
      int end = sequence.length();
      if (sequence.substring(start, end).equals("TGA")) {
        String leftover = sequence.substring(3, start);
        if (leftover.length() % 3 == 0) {
          return "Protein.";
        }
      }
    }
    return "Not a Protein.";
  }

}
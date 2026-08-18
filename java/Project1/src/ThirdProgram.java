public class ThirdProgram {
  public static void main(String[] args) {
    String firstName = "Martin";
    String lastName = "Jones";
    String movieTitle = "The Source Code";
    int numberOfTickets = 8;
    double pricePerTicket = 10.57;
    double totalPrice = pricePerTicket * numberOfTickets;
    String userName = firstName.toLowerCase() + lastName.toLowerCase();

    movieTitle = movieTitle.toUpperCase();

    System.out.println("Congratulations!! You have successfully booked the tickets");
    System.out.println("Username: " + userName);
    System.out.println("Movie: " + movieTitle);
    System.out.println("Number of tickets: " + numberOfTickets);
    System.out.println("Price per ticket: " + pricePerTicket);
    System.out.println("Total Price of " + numberOfTickets + " tickets: $" + totalPrice);
    System.out.println(
        "Thank you for choosing us for booking your movie tickets\n\nEnjoy your movie!!!");
  }
}

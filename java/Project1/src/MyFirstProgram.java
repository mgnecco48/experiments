import java.util.Scanner;

public class MyFirstProgram {
    public static void main(String[] args) {
        System.out.println("Im a programmer");
        System.out.println("Im yes a programmer");

        Scanner scanner = new Scanner(System.in);

        int a = 21;
        double b = 5.0;

        System.out.println(a / b);

        int number = 5;
        System.out.println("Number: " + number);
        System.out.println("=============");

        int x = number++;
        System.out.println("x: " + x);
        System.out.println("Number: " + number);

        System.out.println("=============");
        x = ++number;
        System.out.println("x: " + x);
        System.out.println("Number: " + number);

        System.out.print("Enter your name: ");
        String name = scanner.next();

        System.out.print("Enter you age: ");
        int age = scanner.nextInt();

        double agePercentage = (age * 100 / 80);

        System.out.println(name + ", the percentage of your live lived is: " + agePercentage + "%");

    }
}

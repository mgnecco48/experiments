public class SecondProject {

    public static void main(String[] args) {
        // Declare and initialize an array of superhero names
        String[] superheroes = {"Batman", "Superman", "Wonder Woman", "Spider-Man", "Iron Man"};

        // Declare and initialize an array of years
        int[] introductionYears = {1939, 1938, 1941, 1962, 1963};

        // Print the superhero names
        System.out.println("Superhero Names:");
        //TODO 1: Print all the 5 superheroes names as suggested in the example
        for (int i = 0; i < superheroes.length; i ++) {
            System.out.println(superheroes[i]);
        }
        // Print the introduction years
        System.out.println("Introduction Years:");
        //TODO 2: Print the introductionYear of the superheroes.
      for (int i = 0; i < introductionYears.length; i++){
            System.out.println(introductionYears[i]); 

        }
        // TODO 3a: Print the original name of the third superhero
        System. out.println(superheroes[2]);

        // TODO 3b: Modify the third superhero name
        superheroes[2] = "Black Widow";
        
        // TODO 3c: Print the modified name of the third superhero
        
        System.out.println(superheroes[2]);

        // TODO 4a: Print the original year of introduction of the third superhero
        
        System.out.println(introductionYears[2]); 
        
        // TODO 4b: Modify tintroductionYearsuar of introduction of the third superhero
        
        introductionYears[2] = 2026;

        // TODO 4c: Print the modified year of introduction of the third superhero
      
        System.out.println(introductionYears[2]);
        
        // TODO 5a: Print the length of the array containing superhero names
        
        System.out.println(superheroes.length);
        // TODO 5b: Print the length of the array containing superhero year of introduction
    
        System.out.println(introductionYears.length);
 
    }
}

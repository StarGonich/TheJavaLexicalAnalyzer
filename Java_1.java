public class LexemeExample {
    public static void main(String[] args) { //однострочный комментарий
        public number = 9999e+9999;
        /*
        Многострочный комментарий
        Строка 2комментарий
        Строка 3
        */
        String te\u0410xt = '\'';
        String te\u0410xt = '\77';
        if (number > 5) {
            System.out.println(text);
        } else {
            System.out.println("Number is less than or equal to 5");
        }
        
        for (int i = 0; i < number; i++) {
            System.out.print(i + " ");
        }

        while (number > 0) {
            number--;
        }
        
        switch (number) {
            case 0:
                System.out.println("\nNumber is now 0");
                break;
            default:
                System.out.println("\nNumber is not 0");
        }
        
        int[] numbers = {1, 2, 3, 4, 5};
        for (int num : numbers) {
            System.out.print(num + " ");
        }
    }
}
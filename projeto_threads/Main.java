import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Digite o número de threads: ");
        int numThreads = scanner.nextInt();
        scanner.nextLine();

        String password = "";
        while (true) {
            System.out.println("Digite a senha de 4 números a ser quebrada: ");
            password = scanner.nextLine();

            if (password.matches("\\d{4}")) {
                break;
            } else {
                System.out.println("Senha inválida! A senha deve ter exatamente 4 números.");
            }
        }

        // Criar e iniciar as threads
        for (int i = 0; i < numThreads; i++) {
            new PasswordBroken(password, i, numThreads).start();
        }

        scanner.close();
    }
}
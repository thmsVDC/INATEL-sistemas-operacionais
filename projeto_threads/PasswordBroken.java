class PasswordBroken extends Thread {
    private static volatile boolean passwordFound = false;
    private String password;
    private int threadNumber;
    private int totalThreads;

    public PasswordBroken(String password, int threadNumber, int totalThreads) {
        this.password = password;
        this.threadNumber = threadNumber;
        this.totalThreads = totalThreads;
        this.setName("Thread " + threadNumber);
    }

    @Override
    public void run() {
        int start = (10000 / totalThreads) * threadNumber;
        int end = (threadNumber == totalThreads - 1) ? 10000 : (10000 / totalThreads) * (threadNumber + 1);

        for (long i = start; i < end; i++) {
            if (passwordFound) {
                return;
            }

            String attempt = String.format("%04d", i);
            System.out.println(Thread.currentThread().getName() + " tentando a senha: " + attempt);

            if (attempt.equals(password)) {
                passwordFound = true;
                System.out.println("Senha encontrada: " + attempt + " pela " + Thread.currentThread().getName());
                return;
            }
        }
    }
}
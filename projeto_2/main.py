from round_robin.rr_password_breaker import round_robin
from priority_scheduling.priority_password_breaker import priority_scheduler

def main():
    print("\n🔐 Quebrador de senha com múltiplas estratégias\n")
    print("Escolha o algoritmo:")
    print("1 - Round Robin")
    print("2 - Priority Scheduling")

    choice = input("Opção (1 ou 2): ")
    while choice not in ['1', '2']:
        choice = input("Opção inválida. Escolha 1 ou 2: ")

    password = input("\nDigite a senha de 4 dígitos: ")
    while not password.isdigit() or len(password) != 4:
        password = input("Senha inválida. Digite uma senha de 4 dígitos: ")

    num_threads = int(input("Digite o número de threads: "))

    if choice == '1':
        quantum_size = int(input("Digite o tamanho do quantum: "))
        round_robin(password, num_threads, quantum_size)
    else:
        print("Digite as prioridades (menor valor = mais prioridade):")
        priorities = []
        for i in range(num_threads):
            p = int(input(f"Prioridade da Thread-{i}: "))
            priorities.append(p)
        priority_scheduler(password, num_threads, priorities)

if __name__ == "__main__":
    main()
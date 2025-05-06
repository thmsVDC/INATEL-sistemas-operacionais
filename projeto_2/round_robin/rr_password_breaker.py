import threading
import time

password_found = False

class PasswordBreakerRR(threading.Thread):
    def __init__(self, password, start_range, end_range, thread_id, rr_control, quantum_size=5):
        super().__init__()
        self.password = password
        self.start_range = start_range
        self.end_range = end_range
        self.thread_id = thread_id
        self.rr_control = rr_control
        self.quantum_size = quantum_size

    def run(self):
        global password_found
        i = self.start_range

        while i < self.end_range and not password_found:
            if self.rr_control["turn"] != self.thread_id:
                time.sleep(0.001)
                continue

            for _ in range(self.quantum_size):
                if i >= self.end_range or password_found:
                    break

                attempt = f"{i:04}"
                print(f"Thread-{self.thread_id} tentando: {attempt}")

                if attempt == self.password:
                    password_found = True
                    print(f"Senha encontrada: {attempt} por Thread-{self.thread_id}")
                    return

                i += 1

            self.rr_control["turn"] = (self.rr_control["turn"] + 1) % self.rr_control["num_threads"]

def round_robin(password, num_threads, quantum_size=5):
    global password_found
    password_found = False

    start_time = time.time()
    rr_control = {"turn": 0, "num_threads": num_threads}

    interval_size = 10000 // num_threads
    thread_ranges = [(i * interval_size, (i + 1) * interval_size) for i in range(num_threads)]

    threads = []
    for i in range(num_threads):
        start_range, end_range = thread_ranges[i]
        t = PasswordBreakerRR(password, start_range, end_range, i, rr_control, quantum_size=quantum_size)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"\nTempo total (Round Robin): {end_time - start_time:.2f} segundos\n")
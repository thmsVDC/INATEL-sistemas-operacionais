import threading
import time
import heapq

password_found = False
ready_queue = []
semaphores = []
current_thread = None
lock = threading.Lock()

class PasswordBreakerPriority(threading.Thread):
    def __init__(self, password, start_range, end_range, thread_id, priority, quantum=5):
        super().__init__()
        self.password = password
        self.start_range = start_range
        self.end_range = end_range
        self.thread_id = thread_id
        self.priority = priority
        self.quantum = quantum
        self.semaphore = threading.Semaphore(0)
        semaphores.append(self.semaphore)

    def run(self):
        global password_found, current_thread
        i = self.start_range

        while i < self.end_range and not password_found:
            self.semaphore.acquire()
            
            if password_found:
                return

            with lock:
                current_thread = self.thread_id

            for _ in range(self.quantum):
                if i >= self.end_range or password_found:
                    break

                attempt = f"{i:04}"
                print(f"Thread-{self.thread_id} tentando: {attempt}")
                time.sleep(0.001)
                if attempt == self.password:
                    with lock:
                        password_found = True
                    print(f"🔐 Senha encontrada: {attempt} por Thread-{self.thread_id}")
                    break
                i += 1

            with lock:
                current_thread = None
                if i < self.end_range and not password_found:
                    heapq.heappush(ready_queue, (self.priority, self.thread_id))
                
                if password_found:
                    break

def scheduler():
    global current_thread, password_found
    while True:
        with lock:
            if password_found:
                for sem in semaphores:
                    sem.release()
                break

            if current_thread is None and ready_queue:
                _, thread_id = heapq.heappop(ready_queue)
                semaphores[thread_id].release()
        time.sleep(0.001)

def priority_scheduler(password, num_threads, priorities, quantum=5):
    global password_found, ready_queue, semaphores, current_thread
    password_found = False
    ready_queue = []
    semaphores = []
    current_thread = None

    start_time = time.time()

    interval_size = 10000 // num_threads
    thread_ranges = [(i * interval_size, (i + 1) * interval_size) for i in range(num_threads)]

    threads = []
    for i in range(num_threads):
        start_range, end_range = thread_ranges[i]
        t = PasswordBreakerPriority(password, start_range, end_range, i, priorities[i], quantum)
        threads.append(t)
        heapq.heappush(ready_queue, (priorities[i], i))
  
    for t in threads:
        t.start()

    sched_thread = threading.Thread(target=scheduler)
    sched_thread.start()

    for t in threads:
        t.join()
    sched_thread.join()

    end_time = time.time()
    print(f"\n⏱ Tempo total (Priority Scheduling com Semáforo): {end_time - start_time:.2f} segundos\n")

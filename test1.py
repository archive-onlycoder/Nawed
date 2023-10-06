import threading
import queue
import time
# Define a function that returns a value
def my_function(thread_id):
    time.sleep(5)    
    return f"Thread {thread_id} is running"

# Create a list to hold thread objects and a queue to collect results
threads = []
results = queue.Queue()

# Create and start multiple threads
num_threads = 5

for i in range(num_threads):
    thread = threading.Thread(target=lambda i=i: results.put(my_function(i)))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Retrieve results from the queue
while not results.empty():
    result = results.get()
    print(result)

print("All threads have finished")
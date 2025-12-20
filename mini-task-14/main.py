import threading
import time
import os

# Variables for benching
MODULE = 1000000000000066600000000000001  # Prime number!
SIZE = 20
VALUE = None  # Changes in a cycle
TIMES = 10
CONSUMERS_NUMBER = 25
TASKS_NUMBER = 500
# ----------------------

TASK_QUEUE = []
GLOBAL_RESULT = 0
GLOBAL_THREAD_LOCK = threading.Lock()
PRODUCER_IS_DONE = False


def sqr_matrix_mult(mat1, mat2):
    size = len(mat1)
    result = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += mat1[i][k] * mat2[k][j]

    return result


def matrix_power(matrix, times):
    if times <= 0:
        size = len(matrix)
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    result = matrix
    for _ in range(times - 1):
        result = sqr_matrix_mult(result, matrix)

    return result


def producer():
    global PRODUCER_IS_DONE

    for value in range(1, TASKS_NUMBER + 1):
        with GLOBAL_THREAD_LOCK:
            TASK_QUEUE.insert(0, (SIZE, value, TIMES))

    with GLOBAL_THREAD_LOCK:
        PRODUCER_IS_DONE = True


def consumer():
    global GLOBAL_RESULT
    global MODULE

    result = 0

    while True:
        with GLOBAL_THREAD_LOCK:
            if not TASK_QUEUE:
                if PRODUCER_IS_DONE:
                    break
                else:
                    continue
            else:
                size, value, times = TASK_QUEUE.pop()
        matrix = [[(value ** (i + j)) for j in range(size)] for i in range(size)]
        matrix = matrix_power(matrix, times)
        result += sum(sum(line) for line in matrix)

    with GLOBAL_THREAD_LOCK:
        GLOBAL_RESULT = (GLOBAL_RESULT + result) % MODULE


# Main

START_TIME = time.time()

threads = []

prod_thread = threading.Thread(target=producer)
prod_thread.start()
threads.append(prod_thread)

for _ in range(CONSUMERS_NUMBER):
    cons_thread = threading.Thread(target=consumer)
    cons_thread.start()
    threads.append(cons_thread)

while False:
    with GLOBAL_THREAD_LOCK:
        amount_of_tasks = len(TASK_QUEUE)
    print(f"Current amount of tasks: {amount_of_tasks}")
    if not amount_of_tasks:
        break

for thread in threads:
    thread.join()

FINISH_TIME = time.time()

for _ in range(10):
    print()
if os.getenv('PYTHON_GIL') == '1':
    print(f"Time with GIL: {(FINISH_TIME - START_TIME):.4f}")
else:
    print(f"Time without GIL: {(FINISH_TIME - START_TIME):.4f}")
print(f"Result: {GLOBAL_RESULT}")
for _ in range(2):
    print()

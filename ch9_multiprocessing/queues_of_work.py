import argparse
import math
import multiprocessing
import time

FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"


# If your task has a long completion time (at least a sizable fraction of
# a second) with a small amount of communication, a Queue approach
# might be the right answer.

def check_prime(possible_primes_queue, definite_primes_queue):
    while True:
        n = possible_primes_queue.get()
        if n == FLAG_ALL_DONE:
            # flag that our results have all been pushed to the results queue
            definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        else:
            if n % 2 == 0:
                continue
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    break
            else:
                definite_primes_queue.put(n)


# Using two queues for IPC
def check_prime_2(possible_primes_queue, definite_primes_queue):
    processors_indicating_they_have_finished = 0
    while True:
        # block while waiting for results
        new_result = definite_primes_queue.get()

        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            processors_indicating_they_have_finished += 1
            if processors_indicating_they_have_finished == args.nbr_workers:
                break
        else:
            primes.append(new_result)
    assert processors_indicating_they_have_finished == args.nbr_workers
    print("Took:", time.time() - t1)
    print(len(primes), primes[:10], primes[-10:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project description")
    parser.add_argument(
        "--nbr_workers", type=int, help="Number of workers e.g. 1, 2, 4, 8"
    )
    args = parser.parse_args()
    primes = []

    manager = multiprocessing.Manager()
    possible_primes_queue = manager.Queue()
    definite_primes_queue = manager.Queue()

    pool = multiprocessing.Pool(processes=args.nbr_workers)
    processes = []
    for _ in range(args.nbr_workers):
        p = multiprocessing.Process(
            target=check_prime, args=(possible_primes_queue,
                                      definite_primes_queue)
        )
        processes.append(p)
        p.start()

    t1 = time.time()
    number_range = range(100_000_000, 101_000_000)
    # add jobs to the inbound work queue
    for possible_prime in number_range:
        possible_primes_queue.put(possible_prime)

    # add poison pills to stop the remote workers
    for n in range(args.nbr_workers):
        possible_primes_queue.put(FLAG_ALL_DONE)

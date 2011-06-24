#!/export/home/liuhui/opt/bin/python3

from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    pool = Pool(processes=12)               # start 4 worker processes
    result = pool.apply_async(f, [10])     # evaluate "f(10)" asynchronously
    print(result.get(timeout=1))           # prints "100" unless your computer is *very* slow
    print(pool.map(f, range(1000000)))          # prints "[0, 1, 4,..., 81]"

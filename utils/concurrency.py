# Thread pool helpers

from concurrent.futures import ThreadPoolExecutor


def run_parallel(tasks):
    with ThreadPoolExecutor(max_workers=4) as ex:
        ex.map(lambda f: f(), tasks)

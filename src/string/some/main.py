import time
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool

import requests

urls = [
    "https://www.google.com/",
    "https://yandex.ru/",
    "https://mail.ru/",
    "https://yahoo.com/",
    "https://www.python.org/",
]
real_cpu_count = cpu_count()
print(f"cpu count: {real_cpu_count}")

def fetch_data(url):
    response = requests.get(url)
    data = response.content
    len_data = len(data)
    # print(f"{url} - {len(data)}")

for size in range(1, real_cpu_count * 3 + 1):
    time_s = time.time()

    pool = ThreadPool(size)
    results = pool.map(fetch_data, urls * 3)
    pool.close()
    pool.join()

    delta = time.time() - time_s
    print(f"{size} pool: {delta:.2f}s")

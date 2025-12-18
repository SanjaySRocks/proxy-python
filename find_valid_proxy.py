import threading
import queue
import requests

q = queue.Queue()

valid_proxies = []

with open("iplists.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get(
                "http://ipinfo.io/json",
                proxies={"http": proxy, "https": proxy},
                timeout=5  # Add a timeout of 5 seconds
            )
            if res.status_code == 200:
                print(f"Valid proxy: {proxy}")
                valid_proxies.append(proxy)  # Save valid proxies
        except requests.RequestException as e:
            print(f"Failed proxy {proxy}")
        finally:
            q.task_done()  # Signal task completion


threads = []
for _ in range(10):
    t = threading.Thread(target=check_proxies)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()


with open("valid_proxies.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(f"{proxy}\n")


import threading
import queue
import requests

q = queue.Queue()

valid_proxies = []
india_proxies = []
processed_count = 0

url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
response = requests.get(url, timeout=10)
response.raise_for_status()  # good practice

# Split into lines, strip whitespace, remove duplicates and empty lines
proxies = list(dict.fromkeys(
    line.strip() for line in response.text.splitlines() if line.strip()
))

print(f"Loaded {len(proxies)} unique proxies")

for p in proxies:
    q.put(p)

def check_proxies():
    global q, processed_count
    while not q.empty():
        proxy = q.get()
        processed_count += 1
        try:
            res = requests.get(
                "http://ipinfo.io/json",
                proxies={"http": proxy, "https": proxy},
                timeout=5  # Add a timeout of 5 seconds
            )
            if res.status_code == 200:
                print(f"Valid proxy ({processed_count}): {proxy}")
                valid_proxies.append(proxy)  # Save valid proxies
                try:
                    data = res.json()
                    country = data.get('country')
                    if country == 'IN':
                        india_proxies.append(proxy)
                except:
                    pass  # In case JSON parsing fails
        except requests.RequestException as e:
            print(f"Failed proxy ({processed_count}): {proxy}")
        finally:
            q.task_done()  # Signal task completion


threads = []
for _ in range(100):
    t = threading.Thread(target=check_proxies)
    t.start()
    threads.append(t)

try:
    # Wait for all threads to finish
    for t in threads:
        t.join()
except KeyboardInterrupt:
    print("\nInterrupted by user. Saving current results...")

def write_list_to_file(filename, items):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(items))

write_list_to_file("valid_proxies.txt", valid_proxies)
write_list_to_file("in_validips.txt", india_proxies)


print("Results saved.")


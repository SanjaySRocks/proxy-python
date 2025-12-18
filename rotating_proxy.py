import requests

with open("in_validips.txt", "r") as f:
    proxies = [p for p in f.read().split("\n") if p.strip()]

counter = 0
for x in proxies:
    try:
        res = requests.get("http://ipinfo.io/json", proxies={"http":proxies[counter], "https":proxies[counter]})
        print(proxies[counter], res.status_code)

    except:
        print("Failed: ", proxies[counter], res.status_code)
    finally:
        counter += 1
        counter % len(proxies)

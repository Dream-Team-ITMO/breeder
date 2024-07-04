import requests
import json
import sys
import time
import subprocess
from colorama import Fore, Back, Style

j = json.load(open('report.txt', 'r'))

def compile_and_run(dirname, filename):

    url = "https://www.virustotal.com/api/v3/files"

    print(f"Building {filename}...")
    subprocess.run(["pyinstaller", f"{dirname}/{filename}.py", "--onefile", "--noconsole"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    files = { "file": (filename, open(f"dist/{filename}", "rb"), "text/plain") }
    headers = {
        "accept": "application/json",
        "x-apikey": "0caf67c595966452933755a4317cb93f136d6381d65956eef44d1dd448795677" # please hide this
    }

    print(f"Uploading {filename}...")
    response = requests.post(url, files=files, headers=headers)

    id = json.loads(response.text)["data"]["id"]
    url = "https://www.virustotal.com/api/v3/analyses/" + id

    print(f"Analysing {filename}...")
    while True:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        j = json.loads(response.text)
        if j["data"]["attributes"]["status"] == "completed":
            break

    is_ok = True
    for result in j["data"]["attributes"]["results"]:
        if j["data"]["attributes"]["results"][result]["category"] == "malicious" or j["data"]["attributes"]["results"][result]["category"] == "suspicious":
            is_ok = False
            print(Fore.RED + j["data"]["attributes"]["results"][result]["engine_name"] + " " * (30 - len(j["data"]["attributes"]["results"][result]["engine_name"])) + j["data"]["attributes"]["results"][result]["result"] + Style.RESET_ALL)

    if is_ok:
        print(Fore.GREEN + "File is not detected as malicious" + Style.RESET_ALL)

    open(f'report_{dirname}_{filename}.json', 'w').write(json.dumps(j, ))


def breed(dirname):
    print("Breeding...")
    subprocess.call([sys.executable, "breeder.py", "--compress", dirname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    dirname = sys.argv[1]
    filename = sys.argv[2]

    compile_and_run(dirname, filename)
    breed(dirname)
    compile_and_run(dirname, "breeded")

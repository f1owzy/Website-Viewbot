import os
import requests
import threading
import time
from termcolor import colored

def homepage():
    os.system('cls' if os.name == 'nt' else 'clear')
    color = "\033[0;35m" # Dark purple
    print(f"{color}")

    print("""

██╗   ██╗███████╗██╗  ██╗██╗███╗   ██╗
██║   ██║██╔════╝╚██╗██╔╝██║████╗  ██║
██║   ██║█████╗   ╚███╔╝ ██║██╔██╗ ██║
╚██╗ ██╔╝██╔══╝   ██╔██╗ ██║██║╚██╗██║
 ╚████╔╝ ███████╗██╔╝ ██╗██║██║ ╚████║
  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

UI BY tristan#1000
""")

    print(colored("".center(80, "="), "cyan"))
    print(colored("".center(80, " "), "cyan"))
    print(colored("> 1. Send requests".center(80, " "), "magenta"))
    print(colored("> 2. Exit".center(80, " "), "magenta"))
    print(colored("".center(80, " "), "cyan"))
    print(colored("".center(80, "="), "cyan"))


def send_requests():
    url = input("Enter the URL to send requests: ")
    num_requests = int(input("Enter the number of requests to send: "))
    num_threads = int(input("Enter the number of threads to use: "))
    use_proxy = input("Do you want to use proxies? (y/n): ").lower() == "y"

    proxies = []
    if use_proxy:
        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file]

    def send_request(i):
        if use_proxy:
            proxy = proxies[i % len(proxies)]
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
        else:
            response = requests.get(url)

        if response.status_code == 200:
            if use_proxy:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(colored("[v] Request sent successfully.", "green"))
            else:
                print(colored("[v] Request sent successfully.", "green"))
        else:
            print(colored(f"[x] Error sending request. Status code: {response.status_code}", "red"))

    threads = []
    for i in range(num_threads):
        for j in range(num_requests // num_threads):
            thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j,))
            threads.append(thread)
        if i == num_threads - 1 and num_requests % num_threads != 0:
            for j in range(num_requests % num_threads):
                thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j + num_requests // num_threads,))
                threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(colored(f"[v] All {num_requests} requests sent to {url} successfully!", "green"))

while True:
    homepage()
    choice = input("Enter an option: ")
    if choice == "1":
        send_requests()
        input("Press Enter to continue...")
    elif choice == "2":
        break
    else:
        print(colored("Invalid option. Please try again.", "red"))
        input("Press Enter to continue...")

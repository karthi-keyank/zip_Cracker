import pyzipper
import multiprocessing
import os
import time
import pyfiglet
from colorama import init, Fore

init(autoreset=True)

def display_banner():
    print(pyfiglet.Figlet(font='slant').renderText("ZipCracker"))
    print("___________by karthi")

def extract_zip_with_password(zip_path, password, extract_path):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode()
            zf.extractall(path=extract_path)
        return True
    except:
        return False

def password_cracker(zip_path, extract_path, start, end, found, password):
    for attempt in range(start, end):
        if found.value:
            return
        if extract_zip_with_password(zip_path, str(attempt), extract_path):
            with found.get_lock():
                found.value = True
            with password.get_lock():
                password.value = attempt
            return 

def main():
    try:
        zip_path = input("Enter zip file path: ").strip()
        extract_path = input("Enter extraction path: ").strip()
        if not os.path.isfile(zip_path):
            raise FileNotFoundError("Zip file not found.")

        start_range, end_range = int(input("Start range: ")), int(input("End range: "))
        if start_range >= end_range:
            raise ValueError("Start range must be less than end range.")

        num_processes = multiprocessing.cpu_count()
        range_per_process = (end_range - start_range) // num_processes
        password, found = multiprocessing.Value('i', 0), multiprocessing.Value('b', False)
        processes = []

        start_time = time.time()

        for i in range(num_processes):
            start = start_range + i * range_per_process
            end = start + range_per_process if i < num_processes - 1 else end_range
            process = multiprocessing.Process(target=password_cracker, args=(zip_path, extract_path, start, end, found, password))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        print(f"{Fore.CYAN}Password found: {password.value}" if found.value else f"{Fore.RED}Password not found.")
        print(f"Time taken: {time.time() - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    os.system("clear")
    display_banner()
    main()
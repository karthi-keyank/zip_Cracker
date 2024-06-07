import pyzipper
import multiprocessing
import os
import time
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)

def display_banner():
    banner = pyfiglet.figlet_format("CRACKER")
    author = "by karthi"

    print(Fore.GREEN + banner)
    print(Fore.YELLOW + Style.BRIGHT + author)

def extract_zip_with_password(zip_path, extract_to, password):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode('utf-8')
            zf.extractall(path=extract_to)
        print(f"{Fore.GREEN}Extraction successful! Files extracted to: {extract_to} with password: {password}")
        return True
    except (pyzipper.BadZipFile, RuntimeError):
        return False

def password_cracker(zip_path, extract_to, start, end, password, found):
    for attempt in range(start, end):
        if found.value:
            return
        if extract_zip_with_password(zip_path, extract_to, str(attempt)):
            password.value = attempt
            found.value = True
            return

def main():
    try:
        zip_path = input("Enter path to your zip file: ")
        if not os.path.isfile(zip_path):
            raise FileNotFoundError("Zip file not found.")

        extract_to = input("Enter directory to extract to: ")
        if not os.path.isdir(extract_to):
            raise FileNotFoundError("Extraction directory not found.")

        start_range = int(input("Enter start range for password: "))
        end_range = int(input("Enter end range for password: "))

        if start_range >= end_range:
            raise ValueError("Start range must be less than end range.")

        num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
        range_per_process = (end_range - start_range) // num_processes

        password = multiprocessing.Value('i', 0)
        found = multiprocessing.Value('b', False)
        processes = []

        start_time = time.time()

        for i in range(num_processes):
            start = start_range + i * range_per_process
            end = start + range_per_process if i < num_processes - 1 else end_range
            process = multiprocessing.Process(target=password_cracker, args=(zip_path, extract_to, start, end, password, found))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()

        if found.value:
            print(f"{Fore.CYAN}Password found: {password.value}")
            print(f"{Fore.CYAN}Time taken: {end_time - start_time:.2f} seconds")
        else:
            print(f"{Fore.RED}Password not found in the specified range.")

    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Process interrupted by user.")
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: {e}")
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}")

if __name__ == "__main__":
    display_banner()
    main()
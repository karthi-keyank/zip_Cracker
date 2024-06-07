import pyzipper
import multiprocessing
import os

def extract_zip_with_password(zip_path, extract_to, password):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode('utf-8')
            zf.extractall(path=extract_to)
        print(f"Extraction successful! Files extracted to: {extract_to} with password: {password}")
        return True
    except (pyzipper.BadZipFile, RuntimeError) as e:
        return False

def password_cracker(zip_path, extract_to, start, end, password):
    for attempt in range(start, end):
        if extract_zip_with_password(zip_path, extract_to, str(attempt)):
            password.value = attempt
            return

def main():
    try:
        zip_path = input("Enter path to your zip file: ")
        if not os.path.isfile(zip_path):
            raise FileNotFoundError("Zip file not found.")

        extract_to = input("Enter directory to extract to: ")
        if not os.path.isdir(extract_to):
            raise FileNotFoundError("Extraction directory not found.")

        num_processes = 4
        start_range = 100000
        end_range = 1000000
        range_per_process = (end_range - start_range) // num_processes

        password = multiprocessing.Value('i', 0)
        processes = []

        for i in range(num_processes):
            start = start_range + i * range_per_process
            end = start + range_per_process
            process = multiprocessing.Process(target=password_cracker, args=(zip_path, extract_to, start, end, password))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        if password.value != 0:
            print(f"Password found: {password.value}")
        else:
            print("Password not found in the specified range.")

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

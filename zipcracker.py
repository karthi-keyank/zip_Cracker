import pyzipper
import threading
import time
def extract_zip_with_password(zip_path, extract_to, password):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode('utf-8')
            zf.extractall(path=extract_to)
        print(f"Extraction successful! Files extracted to: {extract_to} with password: {password}")
        return True
    except (pyzipper.BadZipFile, RuntimeError):
        return False

def password_cracker(zip_path, extract_to, start, end, event):
    for password in range(start, end):
        if event.is_set():
            return
        if extract_zip_with_password(zip_path, extract_to, str(password)):
            event.set()
            return

def main():
    zip_path = input("path_to_your_zip_file.zip: ")
    extract_to = input("directory_to_extract_to: ")
    num_threads = 7
    start_range = 100000
    end_range =   1000000
    range_per_thread = (end_range - start_range) // num_threads

    event = threading.Event()
    threads = []

    for i in range(num_threads):
        start = start_range + i * range_per_thread
        end = start + range_per_thread
        thread = threading.Thread(target=password_cracker, args=(zip_path, extract_to, start, end, event))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
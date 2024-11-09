from concurrent.futures import ProcessPoolExecutor

def main():
    try:
        zip_path = input(rainbow_text("Enter path to your zip file: "))
        extract_path = input(rainbow_text("Enter path to extract path: "))
        
        if not os.path.isfile(zip_path):
            raise FileNotFoundError(Fore.RED + "Zip file not found.")

        start_range = int(input(rainbow_text("Enter start range for password: ")))
        end_range = int(input(rainbow_text("Enter end range for password: ")))

        if start_range >= end_range:
            raise ValueError(Fore.RED + "Start range must be less than end range.")

        num_processes = multiprocessing.cpu_count()
        range_per_process = (end_range - start_range) // num_processes

        password = multiprocessing.Value('i', 0)
        found = multiprocessing.Value('b', False)

        start_time = time.time()

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = []
            for i in range(num_processes):
                start = start_range + i * range_per_process
                end = start + range_per_process if i < num_processes - 1 else end_range
                futures.append(
                    executor.submit(password_cracker, zip_path, extract_path, start, end, found, password)
                )
            for future in futures:
                future.result()

        end_time = time.time()

        if found.value:
            print(f"{Fore.CYAN}Password found: {password.value}")
            print(f"{Fore.CYAN}Time taken: {end_time - start_time:.2f} seconds")
        else:
            print(f"{Fore.RED}Password not found in the specified range.")

    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Process interrupted by user.")
    except (FileNotFoundError, ValueError) as e:
        print(f"{Fore.RED}Error: {e}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}")

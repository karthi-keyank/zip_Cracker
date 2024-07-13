from rich.console import Console
from rich.text import Text
import colorsys
import pyzipper
import multiprocessing
import os
import subprocess
import time
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)
# Initialize a Console object to print to the terminal
console = Console()

def rainbow_text(text):
    # Get the length of the input text
    n = len(text)
    
    # Create an empty Text object to store the styled text
    rainbow_text = Text()

    # Iterate over each character in the input text
    for i, char in enumerate(text):
        # Calculate the hue value for the current character (a value between 0 and 1)
        hue = i / n
        
        # Convert the hue to RGB values
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
        
        # Append the character to the Text object with the RGB color style
        rainbow_text.append(char, style=f"rgb({r},{g},{b})")

    # Print the styled text to the console
    console.print(rainbow_text)
    space = ""
    # Return the plain text string
    return space 

def display_banner():
    # Use a specific font
    f = pyfiglet.Figlet(font='slant')
    ascii_art = f.renderText("ZipCracker")
    
    # Display the ASCII art with a rainbow effect
    rainbow_text(ascii_art)
    
    # Print the byline
    rainbow_text("__________________________by karthi")
    
def clear():
    subprocess.run("clear")

def extract_zip_with_password(zip_path, password, extract_path):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode('utf-8')
            zf.extractall(path=extract_path)
        return True
    except (pyzipper.BadZipFile, RuntimeError):
        return False

def password_cracker(zip_path, extract_path, start, end, found, password):
    for attempt in range(start, end):
        if found.value:
            return
        if attempt % 1000 == 0:
            print(rainbow_text(f"Attempting password: {attempt}"))
        if extract_zip_with_password(zip_path, str(attempt), extract_path):
            with found.get_lock():
                found.value = True
            with password.get_lock():
                password.value = attempt
            return 

def main():
    try:
        zip_path = input(rainbow_text("Enter path to your zip file: "))
        extract_path = input(rainbow_text("Enter path to extract path: "))
        if not os.path.isfile(zip_path):
            raise FileNotFoundError(Fore.RED+"Zip file not found.")

        start_range = int(input(rainbow_text("Enter start range for password: ")))
        end_range = int(input(rainbow_text("Enter end range for password: ")))

        if start_range >= end_range:
            raise ValueError(Fore.RED+"Start range must be less than end range.")

        num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
        range_per_process = (end_range - start_range) // num_processes

        password = multiprocessing.Value('i', 0)
        found = multiprocessing.Value('b', False)
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
    clear()
    display_banner()
    main()
import requests
import random
import pyfiglet
from colorama import Fore, Style, init
import subprocess
import os
import time
import sys

init(autoreset=True)

# Banner text and social media information
banner_text = "NINJA"
social_media_usernames = [
    ("TELEGRAM", "@black_ninja_pk"),
    ("Coder", "@crazy_arain"),
]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_gradient_banner(text):
    fonts = ['slant', 'banner3-D', 'block', 'digital', 'banner', 'isometric1']
    selected_font = random.choice(fonts)
    banner = pyfiglet.figlet_format(text, font=selected_font).splitlines()
    
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)
        elif i < section_size * 2:
            print(colors[1] + line)
        else:
            print(colors[2] + line)

def display_banner_and_social():
    clear_console()
    create_gradient_banner(banner_text)
    print(Fore.LIGHTMAGENTA_EX + "Follow us on:")
    for platform_name, username in social_media_usernames:
        print(f"{Fore.CYAN}{platform_name + ':'} {Fore.GREEN}{username}")


# Padding functions for AES encryption
def pad(data):
    padding_length = 16 - (len(data) % 16)
    return data + (chr(padding_length) * padding_length).encode()

def check_for_updates():
    print(Fore.YELLOW + "Checking for updates...")
    repo_url = 'BLACK-NINJA-PK/Session-Link-Decoder'
    api_url = f'https://api.github.com/repos/{repo_url}/commits/main'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        latest_commit = response.json().get('sha')
        
        try:
            current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()
        except subprocess.CalledProcessError:
            print(Fore.RED + "Error: Could not retrieve the current commit. Are you in a Git repository?")
            return

        if latest_commit != current_commit:
            print(Fore.RED + "New update available. Updating...")
            update_script()
        else:
            print(Fore.GREEN + "Your script is up to date.")
    except requests.RequestException as e:
        print(Fore.RED + f"Failed to check for updates: {e}")

def update_script():
    try:
        subprocess.run(["git", "pull"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(Fore.GREEN + "Script updated successfully!")
        sys.exit(0)  # Exit after updating
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to update the script: {e}")
        sys.exit(1)  # Exit with error code if the update fails
    except PermissionError:
        print(Fore.RED + "Permission denied. Try running the script with elevated permissions (e.g., 'sudo').")
        sys.exit(1)

if __name__ == "__main__":
    display_banner_and_social()  # Show banner and social media info
    check_for_updates()  # Check for updates

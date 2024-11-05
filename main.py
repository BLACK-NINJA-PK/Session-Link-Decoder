import urllib.parse
import json
import re
from datetime import datetime, timezone
from termcolor import colored
from colorama import init, Fore, Style
import os
import platform
import pyfiglet
import requests
import subprocess
import sys
import time
import random

# Initialize colorama
init(autoreset=True)

def clear_console():
    """Clear the console screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def create_gradient_banner(text):
    """Create a gradient banner from the provided text using a random font."""
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

def gradient_text(text, colors):
    """Apply a gradient to the text using the provided list of colors."""
    gradient_output = ""
    for i, char in enumerate(text):
        gradient_output += colors[i % len(colors)] + char
    return gradient_output

def is_valid_session_link(url):
    """Validate the session link format."""
    pattern = re.compile(r'^https?://.*#tgWebAppData=.*')
    return bool(pattern.match(url))

def decode_session_link(url):
    parsed_url = urllib.parse.urlparse(url)
    fragment = parsed_url.fragment
    fragment_params = urllib.parse.parse_qs(fragment)
    tg_web_app_data = fragment_params.get('tgWebAppData', [''])[0]
    decoded_data = urllib.parse.parse_qs(tg_web_app_data)

    query_id = decoded_data.get('query_id', [''])[0]
    user_data_encoded = decoded_data.get('user', [''])[0]
    auth_date = decoded_data.get('auth_date', [''])[0]
    hash_value = decoded_data.get('hash', [''])[0]
    user_data_json = urllib.parse.unquote(user_data_encoded)
    user_data = json.loads(user_data_json)
    auth_date_timestamp = int(auth_date)
    auth_date_readable = datetime.fromtimestamp(auth_date_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    reconstructed_data = (
        f"query_id={query_id}&"
        f"user={urllib.parse.quote(user_data_json)}&"
        f"auth_date={auth_date}&"
        f"hash={hash_value}"
    )

    clear_console()
    colors = [Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX]

    display_banner_and_social()
    print(gradient_text("Decoded Session Link Data:", colors))
    print(f"{colored('Reconstructed tgWebAppData Query:', 'cyan')} {reconstructed_data}")
    print(f"{colored('Auth Date (Unix):', 'yellow')} {auth_date}")
    print(f"{colored('Auth Date (Readable):', 'green')} {auth_date_readable}")

    print(gradient_text("User Data:", colors))
    print(f"{colored('User ID:', 'cyan')} {user_data.get('id')}")
    print(f"{colored('First Name:', 'cyan')} {user_data.get('first_name')}")
    print(f"{colored('Last Name:', 'cyan')} {user_data.get('last_name')}")
    print(f"{colored('Username:', 'cyan')} {user_data.get('username')}")
    print(f"{colored('Language Code:', 'cyan')} {user_data.get('language_code')}")
    print(f"{colored('Allows Write to PM:', 'cyan')} {user_data.get('allows_write_to_pm')}")

def check_for_updates():
    print(Fore.YELLOW + "Checking for updates...")
    repo_url = 'BLACK-NINJA-PK/URL_DECODER'
    api_url = f'https://api.github.com/repos/{repo_url}/commits/main'
    response = requests.get(api_url)
    latest_commit = response.json().get('sha')
    current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()

    if latest_commit != current_commit:
        print(Fore.RED + "New update available. Updating...")
        update_script()
    else:
        print(Fore.GREEN + "Your script is up to date.")

def update_script():
    try:
        subprocess.run(["git", "pull"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(Fore.GREEN + "Script updated successfully!")
        time.sleep(2)
        print(Fore.CYAN + f"\nTo run the script again, use the command:\npython {__file__}")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to update the script: {e}")
    except PermissionError:
        print(Fore.RED + "Permission denied. Try running the script with elevated permissions (e.g., 'sudo').")

def display_banner_and_social():
    clear_console()
    create_gradient_banner(banner_text)
    print(gradient_text("Follow us on:", [Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]))
    for platform_name, username in social_media_usernames:
        print(f"{colored(platform_name + ':', 'cyan')} {colored(username, 'green')}")

# Main execution
banner_text = "NINJA"
social_media_usernames = [
    ("TELEGRAM", "@black_ninja_pk"),
    ("TELEGRAM", "@black_ninja_pk"),
    ("Coder", "@crazy_arain"),
]

display_banner_and_social()

# Check for updates
check_for_updates()

# Allow user input for session link
while True:
    session_link = input(colored("\nEnter your session link: ", 'cyan'))

    if is_valid_session_link(session_link):
        break
    else:
        print(colored("Please enter a correct session link.", 'red'))
        display_banner_and_social()

# Decode the provided session link
decode_session_link(session_link)

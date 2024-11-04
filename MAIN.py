import urllib.parse
import json
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

# Initialize colorama
init(autoreset=True)

def clear_console():
    """Clear the console screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def create_gradient_banner(text):
    """Create a gradient banner from the provided text."""
    banner = pyfiglet.figlet_format(text, font='slant').splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)  # Green
        elif i < section_size * 2:
            print(colors[1] + line)  # Yellow
        else:
            print(colors[2] + line)  # Red

def gradient_text(text, colors):
    """Apply a gradient to the text using the provided list of colors."""
    gradient_output = ""
    for i, char in enumerate(text):
        gradient_output += colors[i % len(colors)] + char
    return gradient_output

def decode_session_link(url):
    # Split URL to extract the fragment (data after #)
    parsed_url = urllib.parse.urlparse(url)
    fragment = parsed_url.fragment
    
    # Parse the fragment into a dictionary
    fragment_params = urllib.parse.parse_qs(fragment)
    
    # Decode tgWebAppData if present
    tg_web_app_data = fragment_params.get('tgWebAppData', [''])[0]
    decoded_data = urllib.parse.parse_qs(tg_web_app_data)

    # Extract and decode fields
    query_id = decoded_data.get('query_id', [''])[0]
    user_data_encoded = decoded_data.get('user', [''])[0]
    auth_date = decoded_data.get('auth_date', [''])[0]
    hash_value = decoded_data.get('hash', [''])[0]

    # Decode user data JSON
    user_data_json = urllib.parse.unquote(user_data_encoded)
    user_data = json.loads(user_data_json)

    # Convert auth_date to a timezone-aware, human-readable format
    auth_date_timestamp = int(auth_date)
    auth_date_readable = datetime.fromtimestamp(auth_date_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # Reconstruct the full tgWebAppData query string
    reconstructed_data = (
        f"query_id={query_id}&"
        f"user={urllib.parse.quote(user_data_json)}&"
        f"auth_date={auth_date}&"
        f"hash={hash_value}"
    )

    # Output extracted values with gradient colors
    colors = [Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX]

    print(gradient_text("Decoded Session Link Data:", colors))
    print(f"{colored('Reconstructed tgWebAppData Query:', 'cyan')} {reconstructed_data}")
    print(f"{colored('Auth Date (Unix):', 'yellow')} {auth_date}")
    print(f"{colored('Auth Date (Readable):', 'green')} {auth_date_readable}")

    # Print user data in a labeled, formatted style
    print(gradient_text("User Data:", colors))
    print(f"{colored('User ID:', 'cyan')} {user_data.get('id')}")
    print(f"{colored('First Name:', 'cyan')} {user_data.get('first_name')}")
    print(f"{colored('Last Name:', 'cyan')} {user_data.get('last_name')}")
    print(f"{colored('Username:', 'cyan')} {user_data.get('username')}")
    print(f"{colored('Language Code:', 'cyan')} {user_data.get('language_code')}")
    print(f"{colored('Allows Write to PM:', 'cyan')} {user_data.get('allows_write_to_pm')}")

# Function to check for updates from the GitHub repository
def check_for_updates():
    print(Fore.YELLOW + "Checking for updates...")
    repo_url = 'BLACK-NINJA-PK/URL_DECODER'  # Updated GitHub repository
    # Get the latest commit hash from the GitHub repository
    api_url = f'https://api.github.com/repos/{repo_url}/commits/main'
    response = requests.get(api_url)
    latest_commit = response.json().get('sha')
    
    # Get the current commit hash
    current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()

    if latest_commit != current_commit:
        print(Fore.RED + "New update available. Updating...")
        update_script()
    else:
        print(Fore.GREEN + "Your script is up to date.")

# Function to pull the latest changes from the repository
def update_script():
    try:
        subprocess.run(["git", "pull"], check=True)
        print(Fore.GREEN + "Script updated successfully!")
        time.sleep(2)
        os.execv(__file__, ['python'] + sys.argv)  # Restart the script
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to update the script: {e}")

# Main execution
banner_text = "NINJA"
clear_console()  # Clear the console before the banner
create_gradient_banner(banner_text)  # Create and display the gradient banner

# Display social media usernames
social_media_usernames = [
    ("TELEGRAM", "@black_ninja_pk"),
    ("TELEGRAM", "@black_ninja_pk"),
    ("Coder", "@crazy_arain"),
]

print(gradient_text("Follow us on:", [Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]))
for platform_name, username in social_media_usernames:
    print(f"{colored(platform_name + ':', 'cyan')} {colored(username, 'green')}")

# Check for updates
check_for_updates()  # Check for updates before allowing user input

# Allow user input for session link
session_link = input("\nEnter your session link: ")
decode_session_link(session_link)  # Decode the provided session link without clearing the console again

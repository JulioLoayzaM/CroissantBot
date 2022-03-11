# croissantbot/config.py

"""A module to configure CroissantBot.
"""

import os
import sys

from dotenv import load_dotenv, set_key
from pathlib import Path
from shutil import copyfile
from typing import Optional

try:
    from rich import print
    from rich.console import Console
except Exception:
    print(
        "The rich module is not installed."
        " Please install the necessary dependencies and re-run this script."
    )
    sys.exit(1)


console = Console()


def get_dotenv() -> Optional[Path]:
    """Get a .env file.

    Searches for the .env file. If not found, tries to create one from .env.example.
    """

    env_path = Path('.env')
    print("Looking for the [bold cyan].env[/bold cyan] file.. ", end='')

    if env_path.exists():
        print("[bold green]found")
        print("Using [bold cyan].env[/bold cyan]")

    else:
        print("[bold yellow]not found")
        env_path = Path('.env.example')
        print("Looking for the [bold cyan].env.example[/bold cyan] file.. ", end='')

        if env_path.exists():
            print("[bold green]found")

            print(
                "Copying [bold cyan].env.example[/bold cyan] to"
                " [bold cyan].env[/bold cyan]"
            )
            # since the file will contain the token, avoid making it world-readable
            Path('.env').touch(0o660)
            copyfile('.env.example', '.env')

            print("Using [bold cyan].env[/bold cyan]")
            env_path = Path('.env')

        else:
            print("[red]not found")
            print(
                "Please make sure you are running this where CroissantBot is installed"
                " (the [bold cyan]bot.py[/bold cyan] file should be present)"
            )
            return None

    return env_path


def create_logs():
    """Create the logs directory and files.

    Following the setup guide, creates the directory and the four log files.
    """

    print()
    logs_dir_name = os.getenv('LOG_DIR')
    logs_dir = Path(logs_dir_name)
    if not logs_dir.exists():
        print(f"Creating {logs_dir_name} directory.. ", end='')
        logs_dir.mkdir()
        print("[green]done")

    logs = ['INFO', 'DEBUG', 'DISCORD', 'STREAMLINK']

    print("Creating the log files..  ", end='')
    for log in logs:
        log_file_name = os.getenv(f'LOG_{log}')
        log_path = Path(f'{logs_dir_name}/{log_file_name}')
        log_path.touch(0o664)
    print("[green]done")


def set_log_count(dotenv_path: Path):
    """Set the number of days logs are kept.
    """

    print()
    print(
        "By default, the bot keeps 7 days of logs. You can change this "
        "or leave the default value."
    )
    user_input = console.input("How many days of logs should it keep? \\[default: 7] ")

    if user_input:
        try:
            count = int(user_input)
            set_key(dotenv_path, 'LOG_COUNT', str(count))
            print(f"Log count set to {count}")
        except ValueError:
            print("Not a number, skipping")
    else:
        print("Leaving default value")


def set_prefix(dotenv_path: Path):
    """Set the bot prefix.
    """

    print()
    prefix = console.input(
        'What [bold cyan]prefix[/bold cyan] do you want to use?'
        ' \\[default: !] '
    )

    if prefix:
        set_key(dotenv_path, 'BOT_PREFIX', prefix)
        print(f"Prefix set to [bold cyan]{prefix}")
    else:
        print("No prefix given, defaulting to [bold cyan]!")


def set_token(dotenv_path: Path):
    """Get the bot token from the user.
    """

    print()
    print("Now, let's set the bot token (leave empty if you don't have it yet)")
    token = console.input("Bot token: ")

    if token:
        set_key(dotenv_path, 'DISCORD_TOKEN', token)
        print("Token set")
    else:
        print("No token given, pass")


def first_run(dotenv_path: Path):
    """Functions to run when using this setup for the first time.
    """

    create_logs()
    set_log_count(dotenv_path)
    set_prefix(dotenv_path)
    set_token(dotenv_path)

    set_key(dotenv_path, 'FIRST_RUN', '')


def main():
    """Load the env vars, run first_run if necessary.
    """

    dotenv_path = get_dotenv()
    if dotenv_path is None:
        sys.exit(1)

    load_dotenv(dotenv_path, override=True)

    if os.getenv('FIRST_RUN', '') == 'yes':
        print("First run detected: initializing")
        first_run(dotenv_path)

    sys.exit(0)


if __name__ == '__main__':
    main()

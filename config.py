#!/usr/bin/env python
# croissantbot/config.py

"""A module to configure CroissantBot.
"""

import asyncio
import os
import subprocess
import sys

from dotenv import load_dotenv, set_key
from pathlib import Path
from shutil import copyfile
from typing import Optional


RED    = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
CYAN   = '\033[96m'
ENDC   = '\033[0m'

DONE = f'[ {GREEN}done{ENDC}  ]'
OK   = f'[ {GREEN}OK{ENDC}    ]'
WARN = f'[ {YELLOW}warn{ENDC}  ]'
SKIP = f'[ {YELLOW}skip{ENDC}  ]'
MISS = f'[ {YELLOW}miss{ENDC}  ]'
ERR  = f'[ {RED}error{ENDC} ]'


ASYNCPG_INSTALLED = True
try:
    import asyncpg
except Exception:
    ASYNCPG_INSTALLED = False


def get_dotenv() -> Optional[Path]:
    """Get a .env file.

    Searches for the .env file. If found, backs it up. If not found,
    tries to create one from .env.example.
    """

    env_path = Path('.env')

    if env_path.exists():
        print(f'[ {GREEN}found{ENDC} ] Look for {CYAN}.env{ENDC} file')
        Path('.env.bck').touch(0o600)
        copyfile('.env', '.env.bck')
        print(f'{DONE} Back it up')

    else:
        print(f'{MISS} Look for {CYAN}.env{ENDC} file')
        env_path = Path('.env.example')

        if env_path.exists():
            print(f"[ {GREEN}found{ENDC} ] Look for the {CYAN}.env.example{ENDC} file")
            print(f'{DONE} Copy {CYAN}.env.example{ENDC} to {CYAN}.env{ENDC}')
            # since the file will contain the token, avoid making it world-readable
            Path('.env').touch(0o600)
            copyfile('.env.example', '.env')

            env_path = Path('.env')

        else:
            print(f"{ERR} Look for the {CYAN}.env.example{ENDC} file")
            print(
                f"No {CYAN}.env{ENDC} or {CYAN}.env.example{ENDC} files found, please"
                " make sure you are running this where CroissantBot is installed."
            )
            return None

    print(f"Using {CYAN}.env{ENDC}")
    return env_path


def create_dirs() -> None:
    """Create the basic directories needed.
    """

    print()
    dirs = ['LOG', 'MEME', 'MUSIC']

    for dir_name in dirs:
        cur_dir = Path(os.getenv(f'{dir_name}_DIR'))
        if not cur_dir.exists():
            cur_dir.mkdir()
            print(f'{DONE} Create the {CYAN}{cur_dir}{ENDC} directory')
        else:
            print(f'{SKIP} Create the {CYAN}{cur_dir}{ENDC} directory')


def create_logs() -> None:
    """Create the log files.
    """

    print()
    logs_dir_name = os.getenv('LOG_DIR')
    logs = ['INFO', 'DEBUG', 'DISCORD', 'STREAMLINK']
    for log in logs:
        log_file_name = os.getenv(f'LOG_{log}')
        log_path = Path(f'{logs_dir_name}/{log_file_name}')
        log_path.touch(0o644)
        print(f'{DONE} Create the {CYAN}{log_file_name}{ENDC} file')


def copy_rsc_files() -> None:
    """Copy the provided example from rsc/.

    Since the example files aren't meant to be used directly, copy them. That
    way the env vars can be set from the beginning, meaning less setup.
    """

    print()
    vars = ['KILL_PATH', 'KILL_COUNT', 'MUSIC_FAV_LIST', 'TW_FILE', 'YT_FILE']

    for var in vars:

        filename = os.getenv(var, '')
        if filename == '':
            print(f'{SKIP} Could not find {var} variable')
            continue

        path = Path(filename)
        if not path.exists():

            path.touch(0o644)
            print(f'{DONE} Create the {CYAN}{path}{ENDC} file ({var})')

            # If the file did not exist, try to find the provided example and
            # copy the content to the new file
            temp_path = Path(f'rsc/{path.name}.example')
            if temp_path.exists():
                copyfile(temp_path, path)
                print(f'{DONE} Copy the provided example')
            else:
                print(f'{MISS} Provided example not found, skip copy')

        else:
            print(f"{SKIP} The {CYAN}{path}{ENDC} file already exists")


def set_log_count(dotenv_path: Path) -> None:
    """Set the number of days logs are kept.
    """

    print()
    old_count = os.getenv('LOG_COUNT')
    print(
        "By default, the bot keeps 7 days of logs. You can change this "
        "or leave the curreny value."
    )
    print(f'Current log count: {CYAN}{old_count}{ENDC}')
    user_input = input(
        f"How many {CYAN}days of logs{ENDC} should it keep? [{old_count}] "
    )

    if user_input:
        try:
            count = int(user_input)
            set_key(dotenv_path, 'LOG_COUNT', str(count))
            print(f"Log count set to {CYAN}{count}{ENDC}")
        except ValueError:
            print("Not a number, using current value")
    else:
        print("Using current value")


def set_prefix(dotenv_path: Path) -> None:
    """Set the bot prefix.
    """

    print()
    cur_prefix = os.getenv('BOT_PREFIX')
    print(f'Current prefix: {CYAN}{cur_prefix}{ENDC}, default: {CYAN}!{ENDC}')
    prefix = input(f'What {CYAN}prefix{ENDC} do you want to use? [{cur_prefix}] ')

    if prefix:
        set_key(dotenv_path, 'BOT_PREFIX', prefix)
        print(f"Prefix set to {CYAN}{prefix}{ENDC}")
    else:
        print("No prefix given, using current prefix")


def set_token(dotenv_path: Path) -> None:
    """Get the bot token from the user.
    """

    print()
    print("Now, let's set the bot token (leave empty if you don't have it yet)")
    token = input("Bot token: ")

    if token:
        set_key(dotenv_path, 'BOT_TOKEN', token)
        print("Token set")
    else:
        print("No token given, pass")


async def set_database() -> bool:
    """Initialize the Postgres database for the Playlist cog.
    """

    print()

    if not ASYNCPG_INSTALLED:
        print(f'{MISS} asyncpg is not installed, can\' initialize playlist database')
        return False
    print(f'{OK} asyncpg is installed')

    proc = subprocess.Popen(
        ["pgrep -u postgres -f -- -D"],
        stdout=subprocess.PIPE, shell=True
    )
    (out, _) = proc.communicate()
    out = out.decode()
    out = out.split('\n')
    try:
        if int(out[0]) > 0:
            print(f'{OK} Postgres server is running')
    except Exception as error:
        print(f'{MISS} Postgres server is not running, skipping database initialization')
        print(error)
        return False

    resp = input('Do you want to initialize the database? [Y/n] ').lower()
    if (resp != 'y') and (resp != ''):
        return False

    host     = os.getenv('DB_MUSIC_HOST')
    port     = os.getenv('DB_MUSIC_PORT')
    user     = os.getenv('DB_MUSIC_USER')
    password = os.getenv('DB_MUSIC_PASSWORD')
    database = os.getenv('DB_MUSIC_DATABASE')

    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print(f'{DONE} Connect to database {database}')
    except Exception as error:
        print(f'{ERR} Connect to database {database}')
        print(error)
        return False

    create_playlists = """
        CREATE TABLE playlists (
            list_id  serial      PRIMARY KEY,
            title    varchar(80) NOT NULL,
            owner_id varchar(20) NOT NULL
        );
    """
    create_songs = """
        CREATE TABLE songs (
            song_id   serial      PRIMARY KEY,
            title     varchar(80) NOT NULL,
            url       varchar(80) NOT NULL,
            thumbnail varchar(80) NOT NULL
        );
    """
    create_songs_in_lists = """
        CREATE TABLE songs_in_lists (
            song_id int NOT NULL,
            list_id int NOT NULL,
            FOREIGN KEY (song_id)
                REFERENCES songs (song_id)
                ON DELETE CASCADE,
            FOREIGN KEY (list_id)
                REFERENCES playlists (list_id)
                ON DELETE CASCADE
        );
    """

    tables = ['playlists', 'songs', 'songs_in_lists']
    queries = {
        'playlists': create_playlists,
        'songs': create_songs,
        'songs_in_lists': create_songs_in_lists
    }

    try:
        for table in tables:
            await conn.execute(queries.get(table))
            print(f"{DONE} Create table {CYAN}{table}{ENDC}")
    except Exception as error:
        print(f"{ERR} Create table {table}")
        print(error)
        await conn.close()
        return False

    await conn.close()
    print(f"{DONE} Close connection")

    print(f"Playlist database {GREEN}initialized{ENDC}")
    return True


def first_run(dotenv_path: Path):
    """Functions to run when using this setup for the first time.
    """

    create_dirs()
    create_logs()
    copy_rsc_files()

    set_log_count(dotenv_path)
    set_prefix(dotenv_path)
    set_token(dotenv_path)

    loop = asyncio.get_event_loop()
    _ = loop.run_until_complete(set_database())

    print()
    print(f'{DONE} Finish configuration')
    set_key(dotenv_path, 'FIRST_RUN', '')


def main():
    """Load the env vars, run first_run if necessary.
    """

    dotenv_path = get_dotenv()
    if dotenv_path is None:
        sys.exit(1)

    load_dotenv(dotenv_path, override=True)

    if os.getenv('FIRST_RUN', '') == 'yes':
        print(f"{YELLOW}First run detected{ENDC}: initializing")
        first_run(dotenv_path)

    sys.exit(0)


if __name__ == '__main__':
    main()

# meme.py

This Cog enables the bot's meme-sending capabilities. It uses `asyncpraw`, or the Asynchronous Python Reddit API Wrapper, to download images from Reddit.

## Requirements

- First, install the `asyncpraw` package, which can be installed with `pip`:

  ```
  pip3 install -U asyncpraw
  ```

- [According to the docs](https://asyncpraw.readthedocs.io/en/latest/getting_started/quick_start.html), to use `asyncpraw` we need:

  - A Reddit account: to create a new account, head to [reddit.com](https://www.reddit.com/). You can create an account without providing an email address (just omit it), but be aware this means **there's no way to recover the account if the password is lost**.
  - A Client ID and Secret: see [this guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).
  - A User Agent: this Cog already generates one following the format provided by [Reddit's API guide](https://github.com/reddit-archive/reddit/wiki/API). Thus, I recommend letting the bot take care of that with the information provided by `.env`. Note that the `APP_VERSION` is set arbitrarily; for now it is the same as the bot's version.
  
- Finally, create a directory to store the memes and list files, and set `MEME_DIR` in `.env` accordingly.

## How it works

It saves the memes and list files in `MEME_DIR`.

A meme's filename is derived from its `i.redd.it` URL. For example, from `i.redd.it/thisisnotameme.jpg` we get `thisisnotameme.jpg`.

List files use the guild's name or the private channel's ID as its filename. They should be automatically generated when using the command for the first time in a server or DM.

They store the full `i.redd.it` URL to check if the corresponding meme was already sent to the current context (guild or DM). Even if the meme isn't on the list, the Cog checks if the file itself isn't already downloaded: since the 'hot' posts don't change that fast, the meme could have been sent to another context in the meantime.

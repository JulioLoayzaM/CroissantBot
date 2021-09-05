# Commands

Lists of all available commands.

Use the `help` command to get a list of all available commands *in the current context*: some commands are guild-only, meaning they can't be used in DMs (eg. music commands). Others can only be used by the bot's owner (eg. `exit` to stop the bot).

### bot.py

| Commands  | Aliases | Description                                                  | Comments   |
| --------- | ------- | ------------------------------------------------------------ | ---------- |
| `exit`    |         | Closes the bot                                               | Owner-only |
| `ping`    |         | Pings the bot                                                |            |
| `test`    |         | Replace function as needed                                   | Owner-only |
| `version` | `ver`   | Check the current version, can check the latest remote version. | Owner-only |

### meme.py

| Command | Aliases | Description                                       | Comments |
| ------- | ------- | ------------------------------------------------- | -------- |
| `meme`  |         | Sends a meme from a subreddit, r/memes by default |          |

### misc.py

| Command      | Aliases       | Description                                                  | Comments                                 |
| ------------ | ------------- | ------------------------------------------------------------ | ---------------------------------------- |
| `add`        |               | Adds two integers                                            | Basic example of `discord.py` converters |
| `poggers`    |               | Responds with a poggers emote, if available                  | Guild-only                               |
| `croissant`  |               | Sends a gif                                                  | 🥐                                        |
| `kill`       |               | Kill your enemies (and your friends)                         | Guild-only                               |
| `kill_count` | `count`, `kc` | Shows your kill count, can specify a user to check your stats against them | Guild-only                               |

### music.py

> All music commands are guild-only.

| Command          | Aliases         | Help                                                         |
| ---------------- | --------------- | ------------------------------------------------------------ |
| `join`           | `j`             | Tells the bot to join your current voice channel             |
| `leave`          |                 | Tells the bot to disconnect from its current voice channel   |
| `move`           | `m`             | Moves a song's position in the queue                         |
| `move_here`      | `mh`            | Moves the bot to your voice channel if the bot's current channel is empty |
| `now_playing`    | `now`           | Displays the currently playing song                          |
| `pause`          |                 | Pauses the currently playing song                            |
| `play`           | `p`             | Plays first search result from youtube. For URLs, use `play_from` |
| `play_from`      | `pf`            | Plays a song from an URL. Use `search_youtube` to get a list of related links |
| `remove`         |                 | Removes a song from the queue through its `index`, 0 means no song is selected |
| `resume`         | `res`           | Resumes a paused song                                        |
| `search_youtube` | `yt`, `youtube` | Shows a list of the top 5 results of your search from youtube |
| `show_queue`     | `q`, `queue`    | Displays the current queue                                   |
| `skip`           | `s`             | Skips `index` number of songs, 1 by default                  |
| `stop`           |                 | Stops the currently playing (or paused) song and clears the queue |
| `volume`         | `vol`           | Changes the volume, range: 0-100                             |
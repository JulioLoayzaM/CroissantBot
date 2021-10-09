# music.py

This Cog contains the bot's music-playing commands.

## Requirements

- *New in version 1.1.0*
  
  The `yt-dlp` package, which can be installed with `pip`:
  
  ```
  pip3 install -U yt-dlp
  ```
  
- *Deprecated since version 1.1.0*
  
  The use of the `youtube-dl` package in this bot is deprecated since version `1.1.0`.
  Backwards compatibility is maintained but installing `yt-dlp` is recommended.
  
- `FFmpeg` is used by `yt-dlp` to extract the audio. Install instructions can be found at [ffmpeg.org](https://www.ffmpeg.org/).

- The `MAX_DURATION` variable from `.env` indicates the maximum length in seconds a video can have in order to be downloaded. The default is 600 seconds or 10 minutes.

- `MUSIC_DIR` indicates where to download the music. Create the directory and set the variable accordingly.

- *New in version 1.1.0*

  `MUSIC_FAV_LIST` is the name of the JSON file where the list of each user's favourite songs are saved. This file is kept in `rsc/`. The name is `favourite_songs.json` by default.

## How it works

The bot uses `yt-dlp` to download the video and extracts the audio using `FFmpeg`.
This means the songs take drive space.
It also means that playing a song for the first time may take a bit while the download finishes.
But if this cache isn't cleared, the next time the same song is requested there should be no delay in playing it.
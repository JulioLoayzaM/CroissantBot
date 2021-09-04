# music.py

This Cog contains the bot's music-playing commands.

## Requirements

- The `youtube-dl` package, which can be installed with `pip`:

  ```
  pip3 install -U youtube-dl
  ```

- `FFmpeg` is used by `youtube-dl` to extract the audio. Install instructions can be found at [ffmpeg.org](https://www.ffmpeg.org/).

- The `MAX_DURATION` variable from `.env` indicates the maximum length in seconds a video can have in order to be downloaded. The default is 600 seconds or 10 minutes.

- `MUSIC_DIR` indicates where to download the music. Create the directory and set the variable accordingly.

## How it works

The bot uses `youtube-dl` to download the video and extracts the audio using `FFmpeg`. This means the songs take drive space. It also means that playing a song for the first time may take a bit while the download finishes. But if this cache isn't cleared, the next time the same song is requested there should be no delay in playing it.
# youtube.py

This Cog enables the bot's YouTube livestream-checking capabilities. It uses `streamlink` to get the stream's URL and `yt_dlp` to get the stream's title and thumbnail.

**NOTE**: This Cog can be disabled by setting `ENABLE_YT` to an empty string `""` in `.env`.

## Requirements

- The `streamlink` package, which can be installed with `pip`:

  ```
  pip3 install -U streamlink
  ```

- *New in version 1.1.0*
  The `yt_dlp` package, which can be installed with `pip`:

  ```
  pip3 install -U yt-dlp
  ```

  > For backwards compatibility with the pre-v1.1.0 `music` cog, the `youtube-dl` package can be used. However its use in this bot is deprecated and installing `yt-dlp` is recommended.
  
- The `YT_FILE` variable in `.env` must be set. It represents the path to a JSON file which contains the IDs of the Discord users to notify and the info of the streamers to check.

  The format to use for `YT_FILE` is as follows:

  ```json
  {
  	"discord_user_ID_1": {
  		"youtube_channel_1": {
  			"nickname": "streamers_nickname_1",
  			"url": "channel_url_1"
  		},
  		"youtube_channel_2": {
  			"nickname": "streamers_nickname_2",
  			"url": "channel_url_2"
  		}
  	},
  	"discord_user_ID_2": {
  		"youtube_channel_1": {
  			"nickname": "streamers_nickname_1",
  			"url": "channel_url_1"
  		},
  		"youtube_channel_3": {
  			"nickname": "streamers_nickname_3",
  			"url": "channel_url_3"
  		}
  	}
  }
  ```

  > Note: The `youtube_channel` and `nickname` keys are arbitrary. `youtube_channel` is used to make it easier to identify the channel in the logs, while `nickname` is used to have an identifiable name in the message (since we can't get that info through the API). They can have the same value.

  Fill it with the corresponding information and set `YT_FILE` in `.env`. The Discord user's ID can be found by right-clicking the user's name.

- Finally, the Cog implicitly uses `TW_FREQUENCY`, which indicates how often the bot checks the streams, in minutes. This is used in `bot.py` and is shared with `twitch.py`. If need be, just create `YT_FREQUENCY` in `.env` and make the appropriate changes in `bot.py`.
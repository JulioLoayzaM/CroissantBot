# twitch.py

This Cog enables the bot's Twitch livestream-checking capabilities. It uses  Twitch's API to get the information needed.

**NOTE**: This Cog can be disabled by setting the `ENABLE_TW` variable in `.env` to an empty string `""` or by commenting it (put a `#` before).

## Requirements

- No Twitch package is needed. It uses `requests`, which should be already installed. If it's not, the package can be installed with `pip`:

  ```
  pip3 install -U requests
  ```

- However, to use the API we need the **Client ID** and **Secret**. To get them, follow Step 1 of this [getting started guide](https://dev.twitch.tv/docs/api/#step-1-register-an-application). Fill `TW_CLIENT_ID` and `TW_CLIENT_SECRET` with these values.

- Then, we need an **Access Token**. There are three ways to get one:

  - The easiest one is letting the bot take care of it. Just uncomment `TW_TOKEN`: the bot checks the token validity when starting, so the empty token will generate an error and the bot will automatically try to get a new token.

  - However, if the automatic way fails there are two manual ways to get it. The Twitch CLI is one option. [Step 2](https://dev.twitch.tv/docs/api/#step-2-authentication-using-the-twitch-cli) of the aforementioned guide explains how to use it.

  - Finally, a simple script (based on [this Stack Overflow answer](https://stackoverflow.com/a/66536359)) can be used instead of downloading the CLI:

    ```python
    import requests
    
    # Fill these variables with the credentials obtained
    # on the previous step.
    client_id = ''
    client_secret = ''
    
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': "client_credentials"
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    
    keys = r.json()
    
    print(keys)
    ```

    A sample result of the above script:

    ```json
    {"access_token": "132456789abcdefgh", "expires_in": 3600, "token_type": "bearer"}
    ```

    > Note that API tokens expire, as shown by the `expires_in` field in the example above. App access tokens (the ones used by the bot) are valid for 60 days and can't be refreshed. Instead, when the token is about to or has already expired, the bot gets a new one and stores it in the `.env` file.

- We must set the `TW_FILE` variable in `.env`. It represents the path to a JSON file that stores the IDs of the Discord users to notify and the Twitch channels to check for each one.

  The format to use for `TW_FILE` is as follows:

  ```json
  {
  	"discord_user_ID_1": [
  		"twitch_channel_1",
  		"twitch_channel_2"
  	],
  	"discord_user_ID_2": [
  		"twitch_channel_1",
  		"twitch_user_login_3"
  	]
  }
  ```

  Fill it with the corresponding information and set `TW_FILE` in `.env`.
  A Discord user's ID can be found by right-clicking the user's name.
  You can either use the URL of the streamer's channel or its `user_login`, which is the last portion of said URL.

- Finally, we also have to set `TW_FREQUENCY`. This variables indicates how often the bot will check Twitch, in minutes. It should be a string, so casting to `int` is done in `bot.py`.
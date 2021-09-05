# bot.py

A guide on how to create the bot on Discord and add it to a server.

## Requirements

- The `discord.py[voice]` package, which can be installed with `pip`:

  ```
  pip3 install -U discord.py[voice]
  ```
  
- The `packaging` package, which may be already included, can be installed with `pip`:

  ```
  pip3 install -U packaging
  ```


## Creating the bot

To create the bot on Discord's side of things and get the bot's token, I recommend following [this guide](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal). Here's a quick rundown of the steps to follow:

- If needed, create a Discord account and verify your email.
- Login to the [developer portal](https://discord.com/developers/applications).
- Create a new application.
- In the Bot section (on the left), create a bot. You can change the default name.
- Grab the token.
- Scroll down and enable the `server members intent` under Privileged Gateway intents.

## Adding it to a server

To add the bot to a server (a guild in the API's terminology) see [this part](https://realpython.com/how-to-make-a-discord-bot-python/#adding-a-bot-to-a-guild) of the previous guide. Essentially:

- In the [developer portal](https://discord.com/developers/applications), go to the OAuth2 tab.

- In the OAuth2 URL Generator, select **bot** in Scopes.

- As for permissions, there are two options: for a private server, Administrator is the easier choice, but for a bigger server, it's better to select only the permissions needed for the bot to run correctly.

  For now, the permissions I'm using with the bot are:

  | Permissions                  |
  | ---------------------------- |
  | View channels                |
  | Send messages                |
  | Embed links                  |
  | Attach files                 |
  | Add reactions [not used yet] |
  | Manage messages              |
  | Read message history         |
  | Use Application Commands     |
  | Connect                      |
  | Speak                        |
  | Use voice activity           |

  


# misc.py

This Cog contains miscellaneous commands.

## Requirements

- No package is required besides `dotenv`.

- It does require some files to be set on `.env`:

  - `KILL_PATH` is a `txt` file which contains all possible messages. There should be only one message per line. To insert the nickname of the user using the command, put `<killer>` in the message. Likewise, to insert the victim's nickname, use `<victim>`. These tags are automatically replaced before sending the message. You can put as many of these per message as you want, or none at all. For example, if Alice calls the command on Bob, the phrase:

    ```
    <killer> shot <victim>.
    ```
  
    becomes:
  
    ```
    Alice shot Bob.
    ```
  
  - `KILL_COUNT` is a JSON file that keeps track of how many times a user used the command on someone on that server. When creating the bot it should at least contain an empty dictionary `{}`. It uses the following format:
  
    ```json
    {
    	"guild_id": {
    		"killer_id_1": {
    			"victim_id_1": 3,
    			"victim_id_2": 10
    		},
    		"killer_id_2": {
    			"victim_id_3": 14,
    			"victim_id_1": 2
    		}
    	}
    }
    ```
  
  - `CROISSANT_PATH` points to `croissant.gif`, which is the gif sent when using the [`croissant`](./commands.md#miscpy) command. See [the README](../README.md#Origin) for more info on this command's existence.


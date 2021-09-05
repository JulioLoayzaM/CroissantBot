# twitch.py

Este Cog contiene las funciones para buscar streams en Twitch. Utiliza el API de Twitch para obtener la información necesaria.

**NOTA:** Este Cog puede ser desactivado asignando una cadena vacía `""` o comentando (añadiendo un numeral `#`) la variable `ENABLE_TW` en `.env`.

## Requisitos

- No se necesita un paquete de Twitch. Se utiliza `requests`, que debería estar instalado. Si no es el caso, se puede instalar con `pip`:

  ```
  pip3 install -U requests
  ```

- Sin embargo, para usar el API se necesita un '**Client ID**' y un '**Client Secret**' (ID y secreto de cliente). Para conseguirlos, sigue el primer paso de [esta guía de introducción](https://dev.twitch.tv/docs/api/#step-1-register-an-application). Completa `TW_CLIENT_ID` y `TW_CLIENT_SECRET` con estos valores.

- Luego, necesitamos un '**Access Token**' (ficha de acceso). Existen tres opciones para conseguir una:

  - La más fácil es dejar que el bot se encargue. Solo retira los `#` de `TW_TOKEN`: el bot verifica la validez de la ficha al iniciar, así que al leer una ficha vacía intentará obtener una nueva automáticamente.

  - Si esto fallara, hay dos formas manuales. El CLI de Twitch es una. Sigue [el paso 2](https://dev.twitch.tv/docs/api/#step-2-authentication-using-the-twitch-cli) de la guía precedente para obtener la ficha.

  - Sino, un script sencillo (basado de [esta respuesta en Stack Overflow](https://stackoverflow.com/a/66536359)) puede ser utilizado en vez de descargar el CLI:

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

    Un ejemplo del resultado:

    ```json
    {"access_token": "132456789abcdefgh", "expires_in": 3600, "token_type": "bearer"}
    ```

    > Como lo muestra el campo `expires_in` (expira en), las fichas del API expiran. Las fichas de acceso utilizadas por el bot son válidas por 60 días y no pueden recargarse. En su lugar, cuando la ficha expiró o está a punto de hacerlo, el bot consigue una nueva y la guarda en `.env`.

- Asigna la variable `TW_FILE` en `.env`. Apunta a un archivo JSON que guarda las ID de los usuarios de Discord por notificar y los canales de Twitch a revisar por cada usuario.

  El formato usado en `TW_FILE` es el siguiente:

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

  Llénalo con la información correspondiente y asigna `TW_FILE` en `.env`.
  Puedes encontrar el ID de un usuario de Discord al hacer click derecho en su nombre.
  Puedes usar tanto la dirección del canal del streamer como su `user_login`, que es la última parte de la dirección.

- Por último, asigna también `TW_FREQUENCY`. Esta variable determina la frecuencia a la cual el bot comprueba Twitch, en minutos. Debería ser una cadena de caracteres, así que el cambio a `int` se realiza en `bot.py`.
# youtube.py

Este Cog contiene las funciones para buscar streams en YouTube. Utiliza `streamlink` para obtener el URL del stream y `yt_dlp` para obtener el título y la miniatura.

**NOTA:** Este Cog puede ser desactivado asignando una cadena vacía `""` o comentando (añadiendo un numeral `#`) la variable `ENABLE_YT` en `.env`.

## Requisitos

- El paquete `streamlink`, instalable con `pip`:

  ```
  pip3 install -U streamlink
  ```

- *Nuevo en la versión 1.1.0*
  El paquete `yt_dlp`, instalable con `pip`:

  ```
  pip3 install -U yt-dlp
  ```

  > Para mantener la compatibilidad con el cog `music` pre-v1.1.0, el paquete `youtube-dl` puede ser utilizado. Sin embargo, puede que su uso sea obsoleto en futuras versiones del bot, así que se recomienda instalar `yt-dlp`.
  
- Asigna la variable `YT_FILE` en `.env`. Esta apunta a un archivo JSON que contiene las ID de los usuarios de Discord por notificar y la información de los streamers a revisar.

  El formato usado por `YT_FILE` es el siguiente:

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

  > Nota: las llaves `youtube_channel` y `nickname` (canal de YouTube y apodo, respectivamente) son arbitrarias. `youtube_channel` se utiliza para identificar fácilmente el canal en el registro, mientras que `nickname` se utiliza para tener un nombre identificable en el mensaje (ya que no se puede obtener esa información a través del API). Pueden tener el mismo valor.

  Completa con la información correspondiente y asigna `YT_FILE` en `.env`. Puedes encontrar el ID de un usuario de Discord al hacer click derecho en su nombre.

- Finalmente, el Cog utiliza `TW_FREQUENCY` de forma implícita. Esta variable determina la frecuencia a la cual el bot comprueba YouTube, en minutos. Es utilizada en `bot.py` y es compartida con `twitch.py`. Si se necesita, es posible crear `YT_FREQUENCY` en `.env` y hacer los cambios necesarios en `bot.py`.


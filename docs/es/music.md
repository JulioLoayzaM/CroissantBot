# music.py

Este Cog contiene los comandos de música.

## Requisitos

- *Nuevo en la versión 1.1.0*
  El paquete `yt-dlp`, instalable con `pip`:

  ```
  pip3 install -U yt-dlp
  ```

- *En desuso desde la versión 1.1.0*
  El paquete `youtube-dl` está obsoleto en este bot desde la versión `1.1.0`.
  Se mantiene la compatibilidad con versiones anteriores, pero se recomienda instalar `yt-dlp`.

- `FFmpeg` es utilizado por `yt-dlp` para extraer el audio. Para instalarlo, ve a [ffmpeg.org](https://www.ffmpeg.org/).

- La variable `MAX_DURATION` en `.env` indica la duración máxima (en segundos) que un video puede tener para ser descargado. El valor por defecto son 600 segundos (10 minutos).

- `MUSIC_DIR` apunta a dónde descargar la música. Crea la carpeta y configura la variable con el nombre.

- `MUSIC_FAV_LIST` es el nombre del archivo JSON donde se guardan la lista de canciones favoritas de cada usuario. El archivo se guarda en `rsc/`. El nombre por defecto es `favourite_songs.json`.

## Cómo funciona

El bot utiliza `yt-dlp` para descargar el vídeo y extrae el audio usando `FFmpeg`.
Esto significa que las canciones ocupan espacio en el disco.
También significa que puede haber una ligera demora para reproducir una canción por primera vez, el tiempo que finalice la descarga.
Pero si no se limpia el caché, la próxima vez que la misma canción sea solicitada no debería haber ninguna demora.

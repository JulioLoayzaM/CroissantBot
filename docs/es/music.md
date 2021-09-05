# music.py

Este Cog contiene los comandos de música.

## Requisitos

- El paquete `youtube-dl`, instalable con `pip`:

  ```
  pip3 install -U youtube-dl
  ```

- `FFmpeg` es utilizado por `youtube-dl` para extraer el audio. Para instalarlo, ve a [ffmpeg.org](https://www.ffmpeg.org/).

- La variable `MAX_DURATION` en `.env` indica la duración máxima (en segundos) que un video puede tener para ser descargado. El valor por defecto son 600 segundos (10 minutos).

- `MUSIC_DIR` apunta a dónde descargar la música. Crea la carpeta y configura la variable con el nombre.

## Cómo funciona

El bot utiliza `youtube-dl` para descargar el vídeo y extrae el audio usando `FFmpeg`.
Esto significa que las canciones ocupan espacio en el disco.
También significa que puede haber una ligera demora para reproducir una canción por primera vez, el tiempo que finalice la descarga.
Pero si no se limpia el caché, la próxima vez que la misma canción sea solicitada no debería haber ninguna demora.

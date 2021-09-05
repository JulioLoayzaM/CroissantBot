# meme.py

Este Cog activa las funciones para mandar memes. Utiliza `asyncpraw`, o "Asynchronous Python Reddit API Wrapper", para descargar imágenes de Reddit.

## Requisitos

- Primero, instala el paquete `asyncpraw` usando `pip`:

  ```
  pip3 install -U asyncpraw
  ```

- [Según su documentación](https://asyncpraw.readthedocs.io/en/latest/getting_started/quick_start.html), para usar `asyncpraw` necesitas:

  - Una cuenta de Reddit: para crear una nueva cuenta, dirígete a [reddit.com](https://www.reddit.com/). Puedes crear una cuenta sin indicar una dirección de correo electrónico (solo omítela), pero ten en cuenta que esto significa que **no hay forma de recuperar la cuenta si pierdes la contraseña**.
  - Un 'Client ID' y un 'Client Secret': utiliza [esta guía](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).
  - Un 'User Agent': este Cog genera uno automáticamente, siguiendo el formato indicado en [la guía del API de Reddit](https://github.com/reddit-archive/reddit/wiki/API). Por ende, recomiendo dejar que el bot se haga cargo de eso con la información provista por `.env`. Cabe remarcar que `APP_VERSION` es definida de forma arbitraria; de momento es la misma que la versión del bot.

- Finalmente, crea una carpeta para guardar los memes y las listas, y completa `MEME_DIR` en `.env` con el nombre.

## Cómo funciona

El bot guarda los memes y las listas en `MEME_DIR`.

El nombre de archivo de un meme es obtenido de su dirección `i.redd.it`. Por ejemplo, de `i.redd.it/estenoesunmeme.jpg` obtenemos `estenoesunmeme.jpg`.

Los archivos de lista usan el nombre del servidor o el ID del canal privado como nombre de archivo. Deberían ser automáticamente creados cuando se utiliza el comando por primera vez en ese servidor o mensaje privado.

Las listas guardan la dirección `i.redd.it` completa para comprobar si el meme correspondiente ya fue enviado al contexto actual (servidor o mensaje directo). Incluso si el meme no está en la lista, el Cog comprueba si el archivo mismo ya fue descargado: como la sección 'hot' de memes no se actualiza con frecuencia, puede que el meme ya haya sido enviado a otro contexto.
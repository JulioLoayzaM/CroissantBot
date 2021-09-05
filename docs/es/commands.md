# Comandos

Listas de los comandos disponibles.

Usa el comando `help` para obtener una lista de todos los comandos *disponibles en el contexto actual*: algunos ('guild-only') solo pueden ser usados en servidores y no en mensajes directos (por ejemplo los comandos de música).
Otros ('owner-only') solo pueden ser usados por el dueño del bot (por ejemplo `exit` para cerrar el bot).

### bot.py

| Comandos  | Aliases | Descripción                                                  | Comentarios              |
| --------- | ------- | ------------------------------------------------------------ | ------------------------ |
| `exit`    |         | Cierra el bot                                                | Solo usable por el dueño |
| `ping`    |         | Comprueba que el bot está conectado                          |                          |
| `test`    |         | Sin función definida, comodín                                | Solo usable por el dueño |
| `version` | `ver`   | Muestra la versión actual del bot, puede comprobar si está actualizado | Solo usable por el dueño |

### meme.py

| Comando | Aliases | Descripción                                        | Comentarios |
| ------- | ------- | -------------------------------------------------- | ----------- |
| `meme`  |         | Envía un meme de un subreddit, r/memes por defecto |             |

### misc.py

| Comandos     | Aliases       | Descripción                                                  | Comentarios                                        |
| ------------ | ------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| `add`        |               | Suma dos números enteros                                     | Ejemplo básico de los 'converters' de `discord.py` |
| `poggers`    |               | Responde con un emote poggers, si existe                     | Solo usable en servidores                          |
| `croissant`  |               | Manda un gif                                                 | 🥐                                                  |
| `kill`       |               | Mata a tus enemigos (y a tus amigos)                         | Solo usable en servidores                          |
| `kill_count` | `count`, `kc` | Muestra tu recuento de muertes, se puede especificar un usuario para mostrar tu recuento en contra suya | Solo usable en servidores                          |

### music.py

> Todos los comandos de música son utilizables únicamente en servidores

| Comandos         | Aliases         | Descripción                                                  |
| ---------------- | --------------- | ------------------------------------------------------------ |
| `join`           | `j`             | Indica al bot que se una a tu canal de voz actual            |
| `leave`          |                 | Indica al bot que se desconecte de su canal de voz actual    |
| `move`           | `m`             | Mueve la posición de una canción en la cola                  |
| `move_here`      | `mh`            | Mueve el bot a tu canal de voz actual si el canal del bot está vacío |
| `now_playing`    | `now`           | Muestra la canción en reproducción                           |
| `pause`          |                 | Pausa la canción en reproducción                             |
| `play`           | `p`             | Reproduce el primer resultado de búsqueda de YouTube. Para links, usar `play_from` |
| `play_from`      | `pf`            | Reproduce una canción a partir de un link. Usa `search_youtube` para obtener una lista de resultados |
| `remove`         |                 | Quita una canción de la cola por su índice ('index'), 0 significa que ninguna canción es seleccionada |
| `resume`         | `res`           | Reanuda una canción pausada                                  |
| `search_youtube` | `yt`, `youtube` | Muestra una lista de los primeros 5 resultados de YouTube de tu búsqueda |
| `show_queue`     | `q`, `queue`    | Muestra la cola actual                                       |
| `skip`           | `s`             | Salta `index` número de canciones, 1 por defecto             |
| `stop`           |                 | Detiene la canción en reproducción (o pausada) y borra la cola |
| `volume`         | `vol`           | Cambia el volumen, rango: 0-100                              |
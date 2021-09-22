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
| `poggers`    |               | Responde con un emote poggers, si existe                     | Solo usable en servidores, oculto                  |
| `croissant`  |               | Manda un gif                                                 | 🥐                                                  |
| `kill`       |               | Mata a tus enemigos (y a tus amigos)                         | Solo usable en servidores                          |
| `kill_count` | `count`, `kc` | Muestra tu recuento de muertes, se puede especificar un usuario para mostrar tu recuento en contra suya | Solo usable en servidores                          |

### music.py

> Todos los comandos de música son utilizables únicamente en servidores

| Comandos         | Aliases         | Descripción                                                  |
| ---------------- | --------------- | ------------------------------------------------------------ |
| `join`           | `j`             | Indica al bot que se una a tu canal de voz actual<br /><br />*Nuevo en la versión 1.1.0*<br />El bot puede unirse automáticamente a tu canal de voz usando `play` |
| `leave`          |                 | Indica al bot que se desconecte de su canal de voz actual    |
| `move`           | `m`             | Mueve la posición de una canción en la cola                  |
| `move_here`      | `mh`            | Mueve el bot a tu canal de voz actual si el canal del bot está vacío |
| `now_playing`    | `now`           | Muestra la canción en reproducción                           |
| `pause`          |                 | Pausa la canción en reproducción                             |
| `play`           | `p`             | Reproduce una canción a partir de su URL o el primer resultado de búsqueda de YouTube, usa `search_youtube <busqueda>` para obtener más resultados |
| `play_from`      | `pf`            | *En desuso desde la versión 1.1.0*<br />Reproduce una canción a partir de un link, usa `search_youtube` para obtener una lista de resultados. Oculto desde la versión 1.1.1. |
| `remove`         |                 | Quita una canción de la cola por su índice ('index'), 0 significa que ninguna canción es seleccionada |
| `resume`         | `res`           | Reanuda una canción pausada                                  |
| `search_youtube` | `yt`, `youtube` | Muestra una lista de los primeros 5 resultados de YouTube de tu búsqueda |
| `show_queue`     | `q`, `queue`    | Muestra la cola actual                                       |
| `skip`           | `s`             | Salta `index` número de canciones, 1 por defecto             |
| `stop`           |                 | Detiene la canción en reproducción (o pausada) y borra la cola |
| `volume`         | `vol`           | Cambia el volumen, rango: 0-100                              |

#### Subcomandos de `favourites`

*Nuevo en la versión 1.1.0*

| Comando      | Descripción                                                  | Comentario                            |
| ------------ | ------------------------------------------------------------ | ------------------------------------- |
| `favourites` | Comando de base para administrar las canciones favoritas     |                                       |
| `list`       | Muestra la lista de tus canciones favoritas: puedes obtener información más detallada seleccionando una canción por su índice | Subcomando                            |
| `add`        | Guarda una canción a tu lista a partir de su URL             | Subcomando                            |
| `remove`     | Quita una canción de tu lista a partir de su índice, 0 significa que no se elimina ninguna canción | Subcomando                            |
| `now`        | Guarda la canción en curso de reproducción a tu lista        | Subcomando, solo usable en servidores |
| `play`       | Reproduce una canción de tu lista a partir de su índice      | Subcomando, solo usable en servidores |


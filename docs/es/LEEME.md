# CroissantBot

<p align="center">
    <a href="//www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54"></a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/releases"><img src="https://img.shields.io/github/v/release/JulioLoayzaM/CroissantBot?sort=semver"></a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/JulioLoayzaM/CroissantBot?style=flat"></a>
</p>


CroissantBot es un bot para Discord, programado en Python usando la versión ['rewrite' de `discord.py`](https://github.com/Rapptz/discord.py).

Si bien el bot mismo no está disponible al público, su código si lo está.
Este repositorio apunta a ser una plantilla para facilitar la creación de un nuevo bot, permitiendo a cualquiera\* clonarlo, llenar los espacios en blanco con [la documentación](./) y usarlo en su máquina.

*se recomienda algo de experiencia con Python

<!-- omit in toc -->
## Índice

- [Información importante](#información-importante)
- [Características](#características)
	- [Reproductor de música](#reproductor-de-música)
	- [Memes](#memes)
	- [Mensajes](#mensajes)
	- [Estado de transmisiones en vivo](#estado-de-transmisiones-en-vivo)
	- [Registros](#registros)
- [Como usarlo](#como-usarlo)
	- [Dependencias](#dependencias)
	- [Instalación completa](#instalación-completa)
	- [Desactivando cogs/instalación parcial](#desactivando-cogsinstalación-parcial)
	- [Mantener el bot en línea](#mantener-el-bot-en-línea)
	- [Modificar el código](#modificar-el-código)
- [Por hacer](#por-hacer)
- [Considerando](#considerando)
- [Origen](#origen)
- [Licencia](#licencia)
- [Contribuir](#contribuir)
- [Versionado](#versionado)

## Información importante

El desarrollo de `discord.py` [se detuvo por completo](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1), en parte por la introducción del nuevo `Message.content` 'privileged intent'.
Según [este post de los desarrolladores de Discord](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Access-Deprecation-for-Verified-Bots), este nuevo 'privileged intent' (un permiso para leer mensajes, otorgado manualmente por Discord) no debería ser afectar a "Bot no verificados que estén en menos de 100 servidos".

Aún así, nuevos cambios efectuados al API no serán reflejados por `discord.py`, así que estoy esperando a ver si/cuando un fork viable surge.
Por ahora, seguiré trabajando en el bot como si nada hubiera pasado.

## Características

> Para una lista de todos los comandos, ver [la documentación](commands.md).

### Reproductor de música

Reproduce música de YouTube en canales de voz. Permite reproducir en varios servidos simultáneamente, con una cola para cada uno. Guarda tus canciones favoritas en una lista.

### Memes

Saca memes de Reddit. Mantiene un registro de los memes enviados a cada servidor para evitar duplicados.

### Mensajes

Manda un mensaje

### Estado de transmisiones en vivo

A veces las notificaciones de Twitch no son fiables, así que el bot puede notificar a usuarios de nuevas transmisiones por mensaje privado. También funciona con transmisiones de YouTube. **Esta característica puede ser desactivada.**

### Registros

Transmite información básica y errores por `stdout`. Información de depuración (debug) es registrada en un archivo. Debería permitir de al menos encontrar que función causó un error.

## Como usarlo

La mayoría de los comandos depende de un *Cog*, una extensión usada para reagrupar comandos. Por ejemplo, todos los comandos de música pertenecen al [Cog de música](./../../cogs/music.py).

El bot usa un archivo `.env`. Esto permite guardar todos los credenciales en un solo lugar, en vez de ponerlos en el código fuente, y permite apagar o prender fácilmente algunas características.

Por ejemplo, los cogs `twitch` y `youtube` puede desactivarse ([ver más abajo](LEEME.md#desactivando-cogsinstalación-parcial)). *Se recomienda desactivarlos* si no planeas usarlos, para evitar configurarlos. Se pueden activar luego.

El **prefijo por defecto** es `!`. Puedes cambiarlo en `.env`.

### Dependencias

He probado el bot con `Python 3.6.9` en Ubuntu 18.04 y con `Python 3.6.1` en Windows 10 usando los paquetes siguientes:

| Paquete             | Uso                                                          | Versión probada |
| ------------------- | ------------------------------------------------------------ | --------------- |
| `discord.py[voice]` | API wrapper para Discord con soporte para voz                | `1.7.3`         |
| `python-dotenv`     | Para guardar llaves de API y otros secretos en un archivo `.env` | `0.18.0`        |
| `asyncpraw`         | Asynchronous Python Reddit API Wrapper, para obtener memes de Reddit | `7.3.0`         |
| `streamlink`        | Para chequear transmisiones en vivo de YouTube               | `2.3.0`         |
| `packaging`         | Para comprobar la versión del bot                            | `20.9`          |
| `yt-dlp`            | *Nuevo en la versión 1.1.0*<br />Para obtener música e información de transmisiones en vivo de YouTube | `2021.9.2`      |
| `youtube-dl`        | *En desuso desde la versión 1.1.0*<br />Para obtener música de YouTube | `2021.6.6`      |

### Instalación completa

- Si tienes una cuenta de GitHub, [clona el repositorio](https://docs.github.com/es/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository).

  - Si no, puedes crear una o dirigirte a [la página de lanzamientos](https://github.com/JulioLoayzaM/CroissantBot/releases) para obtener la última versión.

    > Se recomienda clonar el bot para poder actualizarlo fácilmente con Git.

- Instala Python 3.6+: usa un 'package manager' o dirígete a [la página de descargas](https://www.python.org/downloads/).

  > Esto debería instalar `pip`, el instalador de paquetes de Python. Si no estás seguro, lee [las instrucciones de `pip`](https://pip.pypa.io/en/stable/getting-started/) para verificar o instalarlo si.

- Opcional pero recomendado: crea un [entorno virtual](https://python-docs-es.readthedocs.io/es/3.9/tutorial/venv.html?highlight=pip#creating-virtual-environments) para evitar conflictos entre las dependencias.

- Instala los paquetes necesarios con el comando `pip install -U -r requirements.txt`.

- Crea el bot en Discord y consigue su ficha ('token') con [este documento](bot.md).

- Consigue los credenciales de los cogs necesarios: [meme](meme.md), [misc](misc.md) y [música](music.md).

  - Si están activados, consigue los credenciales de los cogs opcionales: [twitch](twitch.md) y/o [youtube](youtube.md). Si estás usando el cog `music`, instala `FFmpeg` usando un 'package manager' o a través de [su página de descargas](https://www.ffmpeg.org/download.html).

- Usa los credenciales para llenar [`.env.example`](./../../.env.example).

- Cambia el nombre del archivo a `.env`.

- Añade el bot a un servidor: vuelve a las instrucciones de [este documento](bot.md).

- Finalmente, ejecuta `bot.py`:

  - Linux/macOS:

    ```
    python3 bot.py
    ```

  - Windows:

    ```
    python bot.py
    ```

### Desactivando cogs/instalación parcial

Los cogs `twitch` y `youtube` son opcionales. Se utilizan para notificar a usuarios de nuevas transmisiones en vivo en esas plataformas (la característica [Estado de transmisiones en vivo](LEEME.md#estado-de-transmisiones-en-vivo)).

Para desactivarlos, asigna una cadena vacía `""` o comenta (precediendo la línea con un numeral `#`) las variables `ENABLE_TW` y `ENABLE_YT` del archivo `.env`, respectivamente.

Desactivar un cog significa que sus variables `.env` no son requeridas:

- En el caso del cog `twitch`, esto permite omitir la configuración necesaria para usar el API de Twitch.

- En cuando al cog `youtube`, desactivarlo significa que su dependencia `streamlink` no es necesaria.

  > El cog `music` también utiliza `yt-dlp` así que no olvides instalarlo incluso si desactivas el cog `youtube`!

### Mantener el bot en línea

Para mantener el bot funcionando continuamente en mi Raspberry Pi 4 utilizo [`tmux`](https://github.com/tmux/tmux/wiki).
Puede crear una sesión desprendible que mantiene el programa ejecutándose en el fondo, permitiendo que el usuario interactúe normalmente con el shell.
Una sesión de `tmux` puede ser conectada al mismo o a un nuevo terminal o sesión de `ssh`.

### Modificar el código

La idea de esta plantilla es de permitir cualquier modificación del código.
Como tal, y como explicado [más abajo](LEEME.md#licencia), el código puede ser libremente modificado bajo una condición: el contenido del [archivo LICENSE](https://github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md) (y no el archivo LICENCIA) debe ser incluido en todas las copias o partes substanciales del código.
Para más información, leer los archivos LICENCIA y LICENSE.
Para un ejemplo de cómo funciona esto, ver el [cog de música](./../../cogs/music.py), que contiene código del [ejemplo basic_voice](https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py) de `discord.py`.

## Por hacer

- [x] Un comando para música - combinar `play`/`play_from`
- [x] Turnar los registros
- [x] Pasar de `youtube-dl` a `yt-dlp`
- [x] Obtener la miniatura de una transmisión con `ytdl(p)`
- [x] Pasar de `requests` a `aiohttp`
- [ ] Probar trasmitir música en lugar de descargarla
- [x] Conectar automáticamente a un canal de voz al usar `play`

## Considerando

- [ ] Traducir la documentación al francés
- [ ] Comandos de moderación
- [ ] Embeds con colores definidos
- [ ] Manera de desactivar otros cogs
- [ ] Hacer de este repositorio una plantilla?
- [ ] Eliminar el intent `members`
- [ ] Añadir soporte para 'slash commands'
- [ ] Ejemplos de scripts para borrar los cachés

## Origen

No pude encontrar el video original, pero este meme es la inspiración para el nombre y el comando  `croissant`: https://www.youtube.com/watch?v=s8VJ4QuVDBE.

## Licencia

Este proyecto está disponible bajo la licencia MIT. Ver [LICENSE.md](./../../LICENSE.md) y [LICENCIA.md](LICENCIA.md) para más información.

## Contribuir

Todas las contribuciones son bienvenidas, para más información lee [CONTRIBUIR](CONTRIBUIR.md).

## Versionado

Las versiones de este repositorio siguen las reglas del [Versionado Semántico 2.0.0](https://semver.org/lang/es/).
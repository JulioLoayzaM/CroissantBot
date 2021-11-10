# CroissantBot

<p align="center">
    <a href="//www.python.org/">
      <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54">
    </a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/releases">
      <img src="https://img.shields.io/github/v/release/JulioLoayzaM/CroissantBot?sort=semver">
    </a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md">
      <img src="https://img.shields.io/github/license/JulioLoayzaM/CroissantBot?style=flat">
    </a>
    <a href='https://croissantbot.readthedocs.io/es/latest/?badge=latest'>
      <img src='https://readthedocs.org/projects/croissantbot-spanish/badge/?version=latest' alt='Documentation Status' />
    </a>
</p>


CroissantBot es un bot para Discord, programado en Python usando la versión ['rewrite' de `discord.py`](https://github.com/Rapptz/discord.py).

Comenzó como un remplazo personal de Dankmemer y Groovy, y terminó siendo un proyecto que quise compartir: si bien el bot mismo no está disponible al público, su código si lo está.
Este repositorio tiene por objetivo proveer una plantilla para permitir que cualquiera\* pueda crear su propio bot con solo clonar el repo, llenar los espacios en blanco con [la documentación](https://croissantbot.readthedocs.io/es/latest/) y usarlo en su máquina.

*se recomienda algo de experiencia con Python

<!-- omit in toc -->
## Índice

- [Información importante](#información-importante)
- [Características](#características)
  - [Reproductor de música](#reproductor-de-música)
  - [Listas de reproducción](#listas-de-reproducción)
  - [Memes](#memes)
  - [Mensajes](#mensajes)
  - [Estado de transmisiones en vivo](#estado-de-transmisiones-en-vivo)
  - [Registros](#registros)
- [Como usarlo](#como-usarlo)
- [Modificar el código](#modificar-el-código)
- [Origen](#origen)
- [Licencia](#licencia)
- [Contribuir](#contribuir)
- [Versionado](#versionado)

## Información importante

El desarrollo de `discord.py` [se detuvo por completo](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1) hace unos meses, en parte por la introducción del nuevo `Message.content` 'privileged intent'.

Según [este post de los desarrolladores de Discord](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Access-Deprecation-for-Verified-Bots), este nuevo 'privileged intent' (un permiso para leer mensajes, otorgado manualmente por Discord) no debería ser afectar a "Bots no verificados que estén en menos de ~~100~~ 75 servidos".

Así que a menos que quieras usar tu bot en más de 75 servidores, no debería causarte problemas. Eso, claro está, hasta que se introduzca un cambio importante en la API de Discord que no será reflejado en `discord.py`.

Todavía no comencé a buscar alternativas para migrar: eso tomará un tiempo, y dependerá de cuantas personas usen este bot, y de mi propio uso.

## Características

> Para una lista de todos los comandos, ver [la documentación](https://croissantbot.readthedocs.io/es/latest/getting_started/commands.html).

### Reproductor de música

Reproduce música de YouTube en canales de voz, con la posibilidad de reproducir música en varios servidores a la vez.

### Listas de reproducción

Guarda cuantas listas por usuario quieras con una base de datos PostgreSQL y el cog Playlist. O utiliza el cog Favourites para guardar canciones en una sola lista por usuario sin usar PostgreSQL.

### Memes

Saca memes de Reddit, manteniendo un registro de los memes enviados a cada servidor para evitar duplicados.

### Mensajes

Basado en Dankmemer, manda un mensaje dirigido a un miembro del servidor. También lleva la cuenta de los kills en cada servidor. Los mensajes no están incluídos.

### Estado de transmisiones en vivo

A veces las notificaciones de Twitch no son fiables, así que el bot puede notificar a usuarios de nuevas transmisiones por mensaje privado. También funciona con transmisiones de YouTube.

### Registros

Transmite información básica y errores por `stdout`. Información de depuración (debug) es registrada en un archivo. Debería permitir de al menos encontrar que función causó un error.

## Como usarlo

Ahora la guía de instalación se encuentra en la página de la documentación, aunque la traducción al español no está completa.
Puedes encontrar la versión anterior e incompleta (pre-2.0.0) [aquí](docs/es).

## Modificar el código

La idea de esta plantilla es de permitir cualquier modificación del código.
Como tal, y como explicado [más abajo](LEEME.md#licencia), el código puede ser libremente modificado bajo una condición: el contenido del [archivo LICENSE](https://github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md) (y no el archivo LICENCIA) debe ser incluido en todas las copias o partes substanciales del código.
Para más información, leer los archivos LICENCIA y LICENSE.
Para un ejemplo de cómo funciona esto, ver el [cog de música](./../../cogs/music.py), que contiene código del [ejemplo basic_voice](https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py) de `discord.py`.

## Origen

No pude encontrar el video original, pero este meme es la inspiración para el nombre y el comando  `croissant`: https://www.youtube.com/watch?v=s8VJ4QuVDBE.

## Licencia

Este proyecto está disponible bajo la licencia MIT. Ver [LICENSE.md](./../../LICENSE.md) y [LICENCIA.md](LICENCIA.md) para más información.

## Contribuir

Todas las contribuciones son bienvenidas, para más información lee [CONTRIBUIR](CONTRIBUIR.md).

## Versionado

Las versiones de este repositorio siguen las reglas del [Versionado Semántico 2.0.0](https://semver.org/lang/es/).
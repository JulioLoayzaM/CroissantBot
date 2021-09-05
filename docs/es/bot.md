# bot.py

Una guía sobre como crear el bot en Discord y añadirlo a un servidor.

## Requisitos

- El paquete `discord.py[voice]`, instalable con `pip`:

  ```
  pip3 install -U discord.py[voice]
  ```

- El paquete `packaging`, que podría ya estar incluido, puede instalarse con `pip`:

  ```
  pip3 install -U packaging
  ```

## Crear el bot

Para crear el bot en Discord mismo y conseguir el 'token', recomiendo seguir [esta guía](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal). Aquí sigue un resumen de los pasos a seguir:

- Si necesario, crea una cuenta Discord y verifica tu dirección de correo.
- Conéctate al [portal de desarrolladores](https://discord.com/developers/applications).
- Crea una nueva aplicación.
- En la sección Bot (a la izquierda), crea un bot. Puedes cambiar el nombre asignado por defecto.
- Recupera el 'token'.
- Desplázate hacia abajo y activa `server members intent` en la categoría 'Privileged Gateway'.

## Añadirlo a un servidor

Para añadir el bot a un servidor (un 'guild' según la terminología del API) sigue [esta parte](https://realpython.com/how-to-make-a-discord-bot-python/#adding-a-bot-to-a-guild) de la guía precedente. En resumen:

- En el [portal de desarrolladores](https://discord.com/developers/applications), ve a la pestaña OAuth2.

- En el 'OAuth URL Generator', selecciona **bot** en la parte Scopes.

- En cuanto a permisos, tienes dos opciones: para un servidor privado, 'Administrator' es la opción más sencilla, pero para un servidor más grande, es mejor seleccionar únicamente los permisos que el bot necesita para funcionar correctamente.

  Por ahora, los permisos que uso con el bot son:

  | Permisos                     |
  | ---------------------------- |
  | View channels                |
  | Send messages                |
  | Embed links                  |
  | Attach files                 |
  | Add reactions [not used yet] |
  | Manage messages              |
  | Read message history         |
  | Use Application Commands     |
  | Connect                      |
  | Speak                        |
  | Use voice activity           |
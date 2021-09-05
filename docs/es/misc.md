# misc.py

Este Cog contiene diversos comandos.

## Requisitos

- Aparte de `dotenv` no se requiere ningún paquete.

- Si requiere configurar algunos archivos en `.env`:

  - `KILL_PATH` es un archivo de texto (`.txt`) que contiene los todos los mensajes posibles. Solo debería añadirse un mensaje por línea. Para insertar el apodo del usuario que invocó el comando, escribe `<killer>` en el mensaje. Asimismo, para insertar el apodo de la víctima, escribe `<victim>`. Estas etiquetas son remplazadas automáticamente antes de enviar el mensaje. Puedes poner cuantas quieras por mensaje, o ninguna. Por ejemplo, si Alice utiliza el comando con Bob, la frase:

    ```
    <killer> le disparó a <victim>.
    ```

    se convierte en:

    ```
    Alice le disparó a Bob.
    ```

  - `KILL_COUNT` es un archivo JSON que lleva la cuenta de las veces que un usuario utilizó el comando con alguien de ese servidor. Al crear el bot el archivo debería contener al menos un diccionario vacío `{}`. Se utiliza el formato siguiente:

    ```json
    {
    	"guild_id": {
    		"killer_id_1": {
    			"victim_id_1": 3,
    			"victim_id_2": 10
    		},
    		"killer_id_2": {
    			"victim_id_3": 14,
    			"victim_id_1": 2
    		}
    	}
    }
    ```

  - `CROISSANT_PATH` apunta a `croissant.gif`, el gif que se envía al usar el comando [`croissant`](commands.md#miscpy). El [LEEME](LEEME.md) contiene más información sobre la existencia de este comando.
# Contribuir a CroissantBot

Antes que nada, gracias por considerar contribuir a CroissantBot! :)

Lo que sigue es un conjunto de guías para contribuir al repositorio. Son guías y no reglas estrictas.

- [¡Esto es muy largo, yo solo quiero hacer una pregunta!](#esto-es-muy-largo-yo-solo-quiero-hacer-una-pregunta)
- [¿Qué tipo de contribuciones se permiten?](#qué-tipo-de-contribuciones-se-permiten)
- [Tu primera contribución](#tu-primera-contribución)
- [Guías de código](#guías-de-código)
	- [Ejemplo de comando](#ejemplo-de-comando)
	- [Ejemplo de docstring](#ejemplo-de-docstring)
	- [Ser explícito](#ser-explícito)
- [Contribuir código](#contribuir-código)
- [Proceso de revisión](#proceso-de-revisión)
- [Reportando bugs](#reportando-bugs)
	- [Divulgación de seguridad](#divulgación-de-seguridad)
	- [Bugs estándar](#bugs-estándar)
	- [Sugerir una característica o una mejora](#sugerir-una-característica-o-una-mejora)
- [Preguntas y otros problemas](#preguntas-y-otros-problemas)

## ¡Esto es muy largo, yo solo quiero hacer una pregunta!

Puedes [abrir un issue](https://github.com/JulioLoayzaM/CroissantBot/issues) y usar la etiqueta `question`.

## ¿Qué tipo de contribuciones se permiten?

Todas las contribuciones son bienvenidas: comparte sugerencias, ideas de nuevas características y reporte de bugs [abriendo un issue](https://github.com/JulioLoayzaM/CroissantBot/issues).

Contribuciones de código también son bienvenidas, haz un fork del repositorio y [crea un pull request](https://github.com/JulioLoayzaM/CroissantBot/pulls).

Sigue leyendo para más información.

## Tu primera contribución

¿Quieres contribuir pero no sabes dónde comenzar? Puedes buscar:

- la etiqueta [`good first issue`](https://github.com/JulioLoayzaM/CroissantBot/labels/good%20first%20issue), para problemas que generalmente no requieren más que unas líneas de código.
- la etiqueta [`help wanted`](https://github.com/JulioLoayzaM/CroissantBot/labels/help%20wanted), para problemas que requieren más atención, pero no son necesariamente más difíciles.

¿Trabajando en tu primer pull request? [Esta guía](https://opensource.guide/how-to-contribute/) puede ser útil (está disponible en Español, cambiando el idioma en la parte de arriba a la derecha). Si todavía tienes dudas, no dudes en pedir ayuda. ;)

## Guías de código

Algunas cosas para considerar antes de enviar código:

1. Documenta y comenta tu código (ejemplos más abajo):
   - Los comandos deben tener los campos `name` y `help`, incluso si la función y el comando tienen el mismo nombre.
   - En general, las funciones deben estar 'type-hinted' (indicio de tipo) y tener una descripción clara en el 'docstring'.
   - No dudes en añadir comentarios: si hubieron demasiados comentarios (innecesarios), pueden ser limpiados antes del merge.
   - Recuerda, [explícito es mejor que implícito](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python): usar nombres descriptivos, evitar 'one-liners'.
   - Usa tabulaciones.
2. Pon a prueba tus cambios.
3. Comienza el mensaje del commit con una acción: add|remove|changed|fix|deprecate (añade|quita|cambia|arregla|discontinua).

### Ejemplo de comando

Usando el decorador `@command`, tenemos:

```python
@bot.command(
	name="ping",
	help="Pings the bot"
)
async def ping_back(ctx: commands.Context):
```

Esto define su nombre en vez de utilizar el nombre de la función. Nos permite tener un nombre más explícito para la función, mientras mantenemos un nombre corto, fácil de recordar para el comando (de preferencia una sola palabra).

Esto también define el texto de ayuda en vez de utilizar el docstring. La ayuda debería ser una frase que explique el uso del comando, mientras que el docstring debe tener una descripción del funcionamiento interno de la función, como lo ilustra el ejemplo siguiente.

### Ejemplo de docstring

Sacado de `queue.insert`:

```python
def insert(self, song: Song, index: int) -> str:
	"""
	Inserts a song at queue[index].
	
	Parameters:
		- song: the song to be inserted.
		- index: the index on the list to insert to, as passed by the user.
	Returns:
		- a message about the result of the operation.
	Raises:
		- IndexError if index is out of range.
	"""
```

Vemos que la función:

- Tiene indicios de tipo (type-hinted), i.e. el tipo de los parámetros y de los valores de retorno están indicados.
  - La única excepción, aquí y en el resto del código, es el parámetro `self`. Si la función no retorna valores, solo omitelo.
- Tiene una descripción de su comportamiento.
- Explica sus diferentes parámetros, valores de retorno, y posibles errores, cuando aplica.
  - Las excepciones son los parámetros `self` y `ctx`, dado que se usan en la mayoría de las funciones y especificar su uso no es necesario.

Añadir índices de tipo fuera de los docstring es bienvenido, especialmente para clases importadas, dado que los editores (IDE) suelen usarlos para mostrar sugerencias.

### Ser explícito

En `bot.check_token`, usamos dos URL diferentes: en vez de llamarlos `url1` y `url2`, usamos nombres descriptivos como `validate_url` y `token_url`.

## Contribuir código

La siguiente guía está basada en https://github.com/MarcDiethelm/contributing/blob/master/README.md:

- Crea un fork personal del proyecto en GitHub.
- Clona el fork en tu computadora personal. Tu repositorio remoto en GitHub se llama `origin`.
- Añade el repositorio original como un remoto llamado `upstream`.
- Si ya creaste un fork hace tiempo, asegúrate de **'pull' los cambios de** `upstream` a tu repositorio local.
- Crea una nueva branch a partir de `develop` en la cual trabajar. Ponle un nombre distintivo como `develop/traduccion`.
- Implementa o arregla tu función, comenta tu código.
- Sigue el estilo de código del proyecto: consulta las [guías de código](#guías-de-código).
- Añade o modifica la documentación según sea necesario.
- Combina ('squash') los commits en uno sólo con la [herramienta rebase](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase) de `git`. Crea una nueva 'branch' si necesario.
- Push la branch a tu fork en GitHub, el remoto `origin`.
- Desde tu fork, abre un pull request en el branch `develop`.
- …
- Si el mantenedor pide cambios adicionales, solo haz un push a tu branch, el pull request se actualizará automáticamente.
- Una vez que el pull request sea aprobado y combinado, puedes pull los cambios de `upstream` a tu repositorio local y eliminar la(s) branch extra.

Para más información sobre los comandos relacionados, puedes ver este gist (en inglés): https://gist.github.com/adamloving/5690951.

## Proceso de revisión

Revisaré todo el código enviado, lo antes posible. Si después de revisarlo, un lapso de tiempo razonable ha pasado, y no recibo respuesta alguna, consideraré cerrar el pull request.

Todos los tags/releases deben ser firmados por mi.

## Reportando bugs

### Divulgación de seguridad

Si encuentras un problema de seguridad, **no abras un issue**. Envíame un correo electrónico a croissantbot[punto]jlm[arroba]gmail[punto]com.

### Bugs estándar

Crea un issue usando la plantilla para reporte de bug y llénala con todo el detalle posible.

¡Crea un pull request si encontraste una solución!

### Sugerir una característica o una mejora

Crea un issue usando la plantilla para 'feature request' y llénala con todo el detalle posible.

¡Crea un pull request si ya comenzaste a implementarla!

## Preguntas y otros problemas

De momento solo hay plantillas para reportes de bugs y sugerencias de característica, así que no dudes en usar un issue en blanco si tu pregunta no corresponde a ninguna de esas categorías.
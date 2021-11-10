import asyncpg
import asyncio

from dotenv import load_dotenv
from os import getenv


async def main():
	"""
	Creates the tables used by the Playlist cog:

		playlists: stores the playlists.
		songs: stores the songs.
		songs_in_playlists: matches the songs with the playlists.
	"""

	load_dotenv()

	host = getenv('host')
	port = getenv('port')
	user = getenv('user')
	pasw = getenv('passw')
	data = getenv('db')

	try:
		conn = await asyncpg.connect(
			host=host,
			port=port,
			user=user,
			password=pasw,
			database=data
		)
		print(f"Connected to the database {data}.")
	except Exception as error:
		print(error)
		await conn.close()
		raise Exception("Could not connect to the database, stopping.")

	pl_create = """
		CREATE TABLE playlists (
			list_id  serial      PRIMARY KEY,
			title    varchar(42) NOT NULL,
			owner_id varchar(20) NOT NULL
		);
	"""
	sg_create = """
		CREATE TABLE songs (
			song_id   serial      PRIMARY KEY,
			title     varchar(80) NOT NULL,
			url       varchar(80) NOT NULL,
			thumbnail varchar(80) NOT NULL
		);
	"""
	sl_create = """
		CREATE TABLE songs_in_lists (
			song_id   int NOT NULL,
			list_id int NOT NULL,
			FOREIGN KEY (song_id)
				REFERENCES songs (song_id)
				ON DELETE CASCADE,
			FOREIGN KEY (list_id)
				REFERENCES playlists (list_id)
				ON DELETE CASCADE
		);
	"""

	try:
		print("Creating the table playlists... ", end="")
		await conn.execute(pl_create)
		print("Done.")
	except Exception as error:
		print(error)
		await conn.close()
		raise Exception("Error creating the table playlists, stopping.")

	try:
		print("Creating the table songs... ", end="")
		await conn.execute(sg_create)
		print("Done.")
	except Exception as error:
		print(error)
		await conn.close()
		raise Exception("Error creating the table songs, stopping.")

	try:
		print("Creating the table songs_in_lists... ", end="")
		await conn.execute(sl_create)
		print("Done.")
	except Exception as error:
		print(error)
		await conn.close()
		raise Exception("Error creating the table songs_in_lists, stopping.")

	print("Closing connection... ", end="")
	await conn.close()
	print("Done.")


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(main())
	except Exception as error:
		print(error)

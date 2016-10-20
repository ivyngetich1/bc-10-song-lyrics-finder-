import json
import urllib.parse
import urllib.request
import musixmatch
import sqlite3
import sys
from tabulate import tabulate
from termcolor import colored, cprint


apikey = '24ede36df0f39765313f6ffa4058c083'
apiurl = "http://api.musixmatch.com/ws/1.1/"



def songfind(song_name):
	query_string = song_name
	search_for = apiurl + "track.search?q=" + (urllib.parse.quote(query_string)) + "&apikey=" + apikey + "&format=plain"
	request = urllib.request.Request(search_for)
	response = urllib.request.urlopen(request, timeout=3600) 
	content = response.read()
	retrieved_obj = json.loads(content.decode('utf-8'))

	song_list = retrieved_obj['message']['body']['track_list']

	x = 0
	all_songs_list = []
	while x < len(song_list):
		each_song_list = []
		song_id = song_list[x]['track']['track_id']
		song_title = song_list[x]['track']['track_name']
		artist_name = song_list[x]['track']['artist_name']
		x += 1
		each_song_list.append(song_id)
		each_song_list.append(song_title)
		each_song_list.append(artist_name)
		
		all_songs_list.append(each_song_list)
		
	print(colored(tabulate(all_songs_list, headers=["song_id","song_title", "song_artist"]), 'blue'))


def songview(song_id):
	save = False
	query_lyrics = song_id

	conn = sqlite3.connect('my_playlist.db')
		
	c = conn.cursor()

	db_lyrics = c.execute("SELECT * FROM my_lyrics WHERE song_id="+query_lyrics)
	result = db_lyrics.fetchone()
	if result is not None:
		print(result[1])
	else:
		print(colored('Id Missing from DB. Searching from API...',"magenta"))
		lyrics_request = urllib.request.Request(apiurl + "track.lyrics.get?track_id=" + query_lyrics +"&apikey=" + apikey + "&json")
		response =  urllib.request.urlopen(lyrics_request, timeout=3600) 
		lyrics_content = response.read()
		lyrics_retrieved = json.loads(lyrics_content.decode('utf-8'))
		if len(lyrics_retrieved['message']['body'])==0:
			print(colored('Lyrics not Found from API',"magenta"))
		else:
			song_lyrics = lyrics_retrieved["message"]["body"]["lyrics"]["lyrics_body"]
			print(song_lyrics)



	


def savesong(song_id):
	
		query_lyrics = song_id
		lyrics_request = urllib.request.Request(apiurl + "track.lyrics.get?track_id=" + query_lyrics +"&apikey=" + apikey + "&json")
		response =  urllib.request.urlopen(lyrics_request, timeout=3600) 
		lyrics_content = response.read()
		lyrics_retrieved = json.loads(lyrics_content.decode('utf-8'))
		if len(lyrics_retrieved['message']['body'])==0:
			print(colored('Lyrics not Found from API'),"magenta")
		else:
			song_lyrics = lyrics_retrieved["message"]["body"]["lyrics"]["lyrics_body"]
		


		conn = sqlite3.connect('my_playlist.db')
	
		c = conn.cursor()
		

		c.execute("CREATE TABLE IF NOT EXISTS my_lyrics(song_id INTEGER,song_lyrics TEXT)")
		
		query_lyrics = c.execute("INSERT INTO my_lyrics (song_id, song_lyrics) VALUES(?,?)", (query_lyrics,song_lyrics))
		result = query_lyrics.fetchone()
		if result is not None:
			print ("Lyrics already in database")

		else:

			conn.commit()
			print(colored("successfully saved","magenta"))


			conn.close()

def songclear(song_clear):
		song_clear = input(colored("input y to clear and n to exit", "magenta"))
		

		if song_clear == "n": 
			sys.exit()
		elif song_clear == "y":

			conn = sqlite3.connect('my_playlist.db')
			
			c = conn.cursor()

			c.execute("DELETE FROM my_lyrics")
			
			conn.commit()
			print (colored ("successfully cleared", "magenta"))

			conn.close()








import json
import urllib.parse
import urllib.request
import musixmatch
import sqlite3
import sys
from tabulate import tabulate


apikey = '24ede36df0f39765313f6ffa4058c083'
apiurl = "http://api.musixmatch.com/ws/1.1/"



def songfind():

	
	query_string = input("what song are you looking for?")
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
		
	print(tabulate(all_songs_list, headers=["song_id","song_title", "song_artist"]))

songfind()

def songview():
	save = False
	query_lyrics = input ("input song id")
	lyrics_request = urllib.request.Request(apiurl + "track.lyrics.get?track_id=" + query_lyrics +"&apikey=" + apikey + "&json")
	response =  urllib.request.urlopen(lyrics_request, timeout=3600) 
	lyrics_content = response.read()
	lyrics_retrieved = json.loads(lyrics_content.decode('utf-8'))



	song_lyrics = lyrics_retrieved["message"]["body"]["lyrics"]["lyrics_body"]
	print(song_lyrics)

	x = input("Want to save? True/False")
	if x == "True":
		save = True
		if save:
			query_lyrics = input ("input song id")
			conn = sqlite3.connect('my_playlist.db')
		
			c = conn.cursor()

			c.execute("CREATE TABLE IF NOT EXISTS my_lyrics(song_id INTEGER,song_lyrics TEXT)")

			c.execute("INSERT INTO my_lyrics (song_id, song_lyrics) VALUES(?,?)", (query_lyrics,song_lyrics))

			conn.commit()
			print ("successfully saved")


			conn.close()
			song_clear = input("Do you want to clear the database? y/n")

			if song_clear == "n": 
				sys.exit()
			elif song_clear == "y":

				conn = sqlite3.connect('my_playlist.db')
				
				c = conn.cursor()

				c.execute("DELETE FROM my_lyrics")
				
				conn.commit()
				print ("successfully cleared")

				conn.close()

songview()

	




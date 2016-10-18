import json
import urllib.parse
import urllib.request
import musixmatch


apikey = '24ede36df0f39765313f6ffa4058c083'
apiurl = "http://api.musixmatch.com/ws/1.1/"

def songfind():
	query_string = input("type your querry")
	search_for = apiurl + "track.search?q=" + (urllib.parse.quote(query_string)) + "&apikey=" + apikey + "&format=plain"
	request = urllib.request.Request(search_for)
	response = urllib.request.urlopen(request, timeout=3600) 
	content = response.read()
	retrieved_obj = json.loads(content.decode('utf-8'))

	song_list = retrieved_obj['message']['body']['track_list']

	x = 0
	while x < len(song_list):
		song_id = song_list[x]['track']['track_id']
		song_title = song_list[x]['track']['track_name']
		artist_name = song_list[x]['track']['artist_name']
		x += 1
		print(str(song_id) + ' ' + song_title + ' ' + artist_name)
songfind()

def songview():
	query_lyrics = input ("input song id")
	lyrics_request = urllib.request.Request(apiurl + "track.lyrics.get?track_id=" + query_lyrics +"&apikey=" + apikey + "&json")
	response =  urllib.request.urlopen(lyrics_request, timeout=3600) 
	lyrics_content = response.read()
	lyrics_retrieved = json.loads(lyrics_content.decode('utf-8'))



	song_lyrics = lyrics_retrieved["message"]["body"]["lyrics"]["lyrics_body"]
	
	print(song_lyrics)

songview()



def songview(songId):
	pass


def songsave(songId):
	pass
	

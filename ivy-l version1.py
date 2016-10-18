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
	
	refined = retrieved_obj['message']['body']['track_list'][0]
	print(refined)

songfind()


def songview(songId):
	pass


def songsave(songId):
	pass
	

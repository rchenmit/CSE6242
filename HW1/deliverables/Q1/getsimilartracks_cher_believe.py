##
## CSE 6242 Pset 1 Part 1
## Robert Chen
## due Sept 8, 2014
##
## grab similar tracks to Cher's "Believe" from last.fm
##
## follow these instructions to start: http://www.last.fm/api/desktopauth
##
## todo:
## 		-make sure you get 100 similars to the original (Cher, Believe)
##			-some got removed in the initial pruining, so add some to get to 100 #line 188: nparr_similartracks_origArtist = removeTracksWithMissingMbid(nparr_similartracks_origArtist) 
## 		-make sure you get 10 "similars to the similars" for each of the 100 similars to original
##			-pruning process for these was in the loop line 193 to 212
##		-remove duplicates from the dataframe df_trackId_similarTrackId (one track + one similar track) final output #lines 233-242



import urllib2
import time
from lxml import etree
from StringIO import StringIO
import json
import webbrowser
import md5
import numpy as np
import pandas as pd
import collections
import urllib
import urlparse

## last.fm API root address
API_ROOT_ADDRESS = "http://ws.audioscrobbler.com/2.0/"

## define api token
API_KEY = "27caacb0c5a55b33e72f02fabfb6ebf7"
API_SECRET = "e88cad96fd686f9a635ba39e2143b939"
USER = "rchen87"
## input what artist/ song
ORIG_ARTIST_NAME = "cher"
ORIG_SONG_NAME = "believe"

######################################################################

def fetchRequestToken(api_key, api_sig):
    '''
    make api call to auth.getToken
    '''
    base_url = ''.join(["http://ws.audioscrobbler.com/2.0/",
                       "?method=auth.gettoken",
                       "&api_key=", API_KEY,
                       "&format=json"])
    response = urllib2.urlopen(base_url, timeout=200)
    response_json = response.read()
    response_dict = json.loads(response_json)
    print response_json
    return base_url, response_dict #return dictionary

def requestAuthorization(api_key, token):
	'''
	request authorization from user; given the API KEY and TOKEN, will open the webbrowser tab and authentication request;
	user has to click "allow access" in this
	'''
	print token
	request_url = ''.join(["http://www.last.fm/api/auth",
						"?api_key=", api_key,
						"&token=", token])

	#now, open web brwoser!
	new = 2 #open in a new tab
	#open the request_url in the new browser tab
	webbrowser.open(request_url, new=new)
	return

def createWebServiceSession(api_key, token, api_sig):
	'''
	this is not working right now
	'''
	request_url = ''.join(["http://ws.audioscrobbler.com/2.0/",
							"?method=", "auth.getSession",
							"&api_key=", api_key,
							"&api_sig=", api_sig
							])
	#response = urllib2.urlopen(request_url, timeout=200)

	return request_url


def url_fix(s, charset='utf-8'):
    # '''
    # Sometimes you get an URL by a user that just isn't a real
    # URL because it contains unsafe characters like ' ' and so on.  This
    # function can fix some of the problems in a similar way browsers
    # handle data entered by the user:
    # 
    # >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklarung)')
    # 'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    # :param charset: The target charset for the URL if the url was
    #                 given as unicode string.
    # '''
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def getSimilarTracks(api_key, artist=None, songtitle=None, mbid=None, autocorrect=None, limit=None):
	'''
	get similar songs to the songe name "songtitle" by artiest "artist"
	'''
	#repace all spaces with character %20
	request_url = ''.join([API_ROOT_ADDRESS,
						  "?method=", "track.getSimilar", 
						  "&api_key=", api_key,
						  "&format=json"
						  ])
	if mbid:
		request_url = request_url + "&mbid=" + str(mbid)
	elif (not artist and not songtitle):
		return {'similartracks': 'NA'}
	else:
		request_url = request_url + "&artist=" + artist
		request_url = request_url + "&track=" + songtitle


	if autocorrect and autocorrect==0 or autocorrect==1:
		request_url = request_url + "&autocorrect=" + str(autocorrect)
	if limit and type(limit)==int:
		request_url = request_url + "&limit=" + str(limit)
	request_url = url_fix(request_url)
	print "HTTP GET: " + request_url
	response = urllib2.urlopen(request_url, timeout=200)
	response_json = response.read()
	try:
		response_dict = json.loads(response_json)
	except:
		return {'similartracks': 'NA'}
	return response_dict

def removeTracksWithMissingMbid(nparr_tracks):
	'''
	input: nparr_tracks: np array of tracks (dict form)
	'''
	l_index_missing_mbid = []
	for i in range(len(nparr_tracks)):
		track = nparr_tracks[i]
		if not 'mbid' in track: # if the track does NOT have an mbid
			print "no mbid"
			l_index_missing_mbid.append(i)
		elif track['mbid'] == None:
			print "no mbid -- None"
			l_index_missing_mbid.append(i)
		elif track['mbid'] == '':
			print "no mbid -- empty string"
			l_index_missing_mbid.append(i)
	#now, delete the entries where there is no mbid
	nparr_tracks_parsed = np.delete(nparr_tracks, tuple(l_index_missing_mbid))	
	return nparr_tracks_parsed


#############################################################################################




### inro
print "* this script pulls from last.fm 100 similar tracks to what is specified"

### authentification
# fetch authetification request token
print "* fetching authentification request token with api_key and api_signature:  " 
auth_token = fetchRequestToken(API_KEY, API_SECRET)[1]["token"]
#+ fetchRequestToken(API_KEY, API_SIG)[0]

# request authorization from user, using HTTP GET request
print "* request authorization from user, using HTTP GET request"
requestAuthorization(API_KEY, auth_token)

print "* create api signature for auth.getSession call"
api_sig_str = ''.join(["api_key", API_KEY, "method", "auth.getSession", "token", auth_token, API_SECRET])
api_sig = md5.new(api_sig_str).digest()

print "* create a web service section, using API_KEY, auth_token and api_sig (md5 hashed)"
get_session = createWebServiceSession(API_KEY, auth_token, api_sig)

print "** authentification done ***********************************"


### crawl
print "* getting similar tracks to the song: artist = {0}, track = {1}".format("cher", "believe")
#get a dictionary of the similar tracks
d_getSimilarTracks_origArtist = getSimilarTracks(API_KEY, artist=ORIG_ARTIST_NAME, songtitle=ORIG_SONG_NAME, mbid=None, autocorrect=None, limit=100)

### parse the dictionary of similar tracks

#kick out any track where there is no mbid
nparr_similartracks_origArtist = np.array(d_getSimilarTracks_origArtist['similartracks']['track'])
nparr_similartracks_origArtist = removeTracksWithMissingMbid(nparr_similartracks_origArtist)


#now, loop through each track and find the 10 most similar tracks
t_10mostSimilarTracks_toOriginalSimilars = ()
for track in nparr_similartracks_origArtist:
	this_artist = track['artist']['name']
	this_track_name = track['name']
	this_mbid = track['mbid']
	d_getSimilarTracks_thisTrack = getSimilarTracks(API_KEY, artist=this_artist,songtitle=this_track_name, mbid=this_mbid, limit=10) #use API to get similar tracks to this track
	
	if 'similartracks' in d_getSimilarTracks_thisTrack:
		if 'track' in d_getSimilarTracks_thisTrack['similartracks']:
			if type(d_getSimilarTracks_thisTrack['similartracks']['track']) == list: 
				nparr_similarTracks_thisTrack = np.array(d_getSimilarTracks_thisTrack['similartracks']['track'])
			elif type(d_getSimilarTracks_thisTrack['similartracks']['track']) == dict:
				nparr_similarTracks_thisTrack = nparr(d_getSimilarTracks_thisTrack['similartracks'])
			else:
				continue
	else:
		continue
	nparr_similarTracks_thisTrack = removeTracksWithMissingMbid(nparr_similarTracks_thisTrack)

	#make list of mbid for similar tracks to this track
	l_mbid_similarTracks_thisTrack = []
	for t in nparr_similarTracks_thisTrack:
		l_mbid_similarTracks_thisTrack.append(t['mbid'])
	t_10mostSimilarTracks_toOriginalSimilars = t_10mostSimilarTracks_toOriginalSimilars + ((this_mbid,l_mbid_similarTracks_thisTrack),)# append tuple (this_mbid,l_mbid_similarTracks_thisTrack) to the tuple t_10mostSimilarTracks_toOriginalSimilars


### create the output file for tracks.csv
l_mbid = []
l_track_name = []
l_artist = []
for track in nparr_similartracks_origArtist:
	l_mbid.append(track['mbid'])
	l_track_name.append(track['name'])
	l_artist.append(track['artist']['name'])
od_tracks_parsed = collections.OrderedDict((('id', l_mbid), ('track_name', l_track_name), ('artist',l_artist)))

df_tracks_parsed = pd.DataFrame.from_dict(od_tracks_parsed)

#output tracks.csv
df_tracks_parsed.to_csv("tracks.csv",encoding='utf-8', index = False)


### create the output file for track_id_sim_track_id.csv
l_orig_mbid = []
l_similar_mbid = []
for t_track_listOfSimilars in t_10mostSimilarTracks_toOriginalSimilars:
	for mbid_in_sim_list in t_track_listOfSimilars[1]: #for each similar mbid in the list of 10 similar mbids
		l_orig_mbid.append(t_track_listOfSimilars[0])
		l_similar_mbid.append(mbid_in_sim_list)
od_trackId_similarTrackId = collections.OrderedDict((('source', l_orig_mbid), ('target', l_similar_mbid)))
df_trackId_similarTrackId = pd.DataFrame.from_dict(od_trackId_similarTrackId)

#remove duplicates
lt_trackId_similarTrackId_GROUPED = df_trackId_similarTrackId.groupby(['source', 'target']).groups.keys()
lt_source_target_sorted = []
for tup in lt_trackId_similarTrackId_GROUPED:
	lt_source_target_sorted.append(tuple(np.sort(tup)))
nparry_source_target_sorted_NO_DUPLICATES = np.unique(lt_source_target_sorted)
df_trackId_similarTrackId_NO_DUPLICATES = pd.DataFrame(data = nparry_source_target_sorted_NO_DUPLICATES, columns = ['source','target'])

#save files
df_trackId_similarTrackId.to_csv("track_id_sim_track_id.csv", encoding='utf-8', index= False)











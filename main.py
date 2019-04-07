import spotipy as sp
from spotipy import util
import random
import sys

assert len(sys.argv) >= 3, '''You need to specify 2 command args: playlist name, and playlist length, 
and optionally- number of artists considered when getting data for creating playlist'''
playlist_name = sys.argv[1]
playlist_len = int(sys.argv[2])
artists_num = int(sys.argv[3]) if len(sys.argv) == 4 else 10


def get_sample_playlist(spotify, related_artists):
    assert isinstance(related_artists, list)
    songs = []
    for a in related_artists:
        for k in a.keys():
            try:
                top_songs = spotify.artist_top_tracks(k)['tracks']
            except Exception as e:
                print(e)
            break
        for s in top_songs:
            songs.append(s)
    random.shuffle(songs)
    return songs[:playlist_len]


def main():
    token = util.prompt_for_user_token(username='your_username',
                                       scope='user-top-read',
                                       client_id='your_client_id',
                                       client_secret='your_client_secret',
                                       redirect_uri='http://something/'
                                       )
    spotify = sp.Spotify(auth=token)

    top_artists = spotify.current_user_top_artists(limit=artists_num)
    artist_ids = {artist['name']: artist['id'] for artist in top_artists['items']}
    related_list = []

    for artist, aid in artist_ids.items():
        related = spotify.artist_related_artists(aid)
        for a in related['artists']:
            artist_data = {a['id'] : {'Name': a['name'], 'Genres': a['genres']}}
            related_list.append(artist_data)
    sample_playlist = get_sample_playlist(spotify, related_list)
    sample_playlist = [song['id'] for song in sample_playlist]
    playlist = spotify.user_playlist_create('your_username', playlist_name)
    spotify.user_playlist_add_tracks('your_username', playlist['id'], sample_playlist)


if __name__ == '__main__':
    main()
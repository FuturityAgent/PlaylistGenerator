import spotipy as sp
from spotipy import util
import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("name", help="What's name of playlist?")
parser.add_argument("--num_songs", default=10, help="How many songs include in playlist?")
parser.add_argument("--num_artists", default=10, help="How many artists should be considered?")
parser.add_argument("--include", help="What genres should be included?")
parser.add_argument("--ignore", help="What genres should be ignored?")
args = parser.parse_args()
playlist_name = args.name
playlist_len = int(args.num_songs)
artists_num = int(args.num_artists)
excluded_genres = ''.join(args.ignore).replace("\"", '').split(",") if args.ignore else None
included_genres = ''.join(args.include).replace("\"", '').split(",") if args.include else None


def drop_genres(artist_data):
    artist_data = list(artist_data.values())[0]
    if any([genre in excluded_genres for genre in artist_data['Genres']]):
        return False
    return True


def select_genres(artist_data):
    artist_data = list(artist_data.values())[0]
    if any([genre in included_genres for genre in artist_data['Genres']]):
        return True
    return False


def get_sample_playlist(spotify, related_artists):
    assert isinstance(related_artists, list)
    songs = []
    for a in related_artists:
        for k in a.keys():
            top_songs = spotify.artist_top_tracks(k)['tracks']
            break
        for s in top_songs:
            songs.append(s)
    random.shuffle(songs)
    return songs[:playlist_len]


def main():
    token = util.prompt_for_user_token(username='your-username',
                                       scope='user-top-read',
                                       client_id='your-client-id',
                                       client_secret='your-client-secret',
                                       redirect_uri='http://something/'
                                       )
    spotify = sp.Spotify(auth=token)

    top_artists = spotify.current_user_top_artists(limit=artists_num)
    artist_ids = {artist['name']: artist['id'] for artist in top_artists['items']}
    related_list = []

    for artist, aid in artist_ids.items():
        related = spotify.artist_related_artists(aid)
        for a in related['artists']:
            artist_data = {a['id']:{'Name': a['name'], 'Genres': a['genres']}}
            related_list.append(artist_data)
    if excluded_genres is not None:
        related_list = list(filter(drop_genres, related_list))
    elif included_genres is not None:
        related_list = list(filter(select_genres, related_list))
    num_items = 10 if len(related_list) > 10 else len(related_list)
    if num_items > 0:
        related_sample = random.sample(related_list, num_items)
        sample_playlist = get_sample_playlist(spotify, related_sample)
        sample_playlist = [song['id'] for song in sample_playlist]
        playlist = spotify.user_playlist_create('your-username', playlist_name)
        spotify.user_playlist_add_tracks('your-username', playlist['id'], sample_playlist)
    else:
        raise Exception("Couldn't find any songs :(")


if __name__ == '__main__':
    main()
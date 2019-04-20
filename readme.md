Script to generate playlist based on top user's artists

Uses [Spotipy](https://github.com/plamere/spotipy)

## Usage
Before you start you need to register your app on [developers.spotify](https://developer.spotify.com/dashboard/)
and then you need to replace token parameters with your parameters.
Also you need to replace username at lines 49 and 50 with your username.

python3 main.py playlist_name -- num_songs playlist_length --num_artists num_of_artists_considered --include included_genres --ignore ignored_genres

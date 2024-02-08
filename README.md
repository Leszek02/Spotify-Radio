# Api functions

## Requesting info through SpotifyRequests class:
classInterface(function_name, *args)

*args are all the arguments the function you're executing needs, seperated with coma.

Example: response = spotify.classInterface("playlistContentRequest", 1231245)

## stopRequest()

Stops the current playback, if it's already stoped returns 403 response_code.

## playRequest(albumUri = "", type="", offset = 0)
### If no arguments provided:
Plays the current playback, if it's already stoped returns 403 response_code.
### If arguments provided:
albumUri - Item id that you want to transfer to current playback
type - one of these: "album", "playlist", "artist", "track"
offset - for first three types only, starts playing from 0 + offset track position (first song is at position 0).

## availableDevicesRequest()

Returns data about active devices current user have.

## transferPlaybackRequest(deviceId)

Changes the user's active device to the one with deviceId.

## skipToNextRequest()

Plays the next track from the queue.

## skipToPreviousRequest()

Plays the previous track from the queue.

## playlistsRequest()

Returns details about active user's playlists.

## playlistContentRequest(playlistId)

Returns names and ids of all tracks from the playlist with playlistId. The order of the tracks is the same as it is in the playlist.

## changeVolumeRequest(volumeValue)

Sets user's playback volume to volumeValue. This value has to be from range <0, 100>.

## searchForItemRequest(searchedString, type, offset)

Returns 10 first items that match given parameters.

searchedString - name of an item we want to search for.

type - one of these: "album", "artist", "playlist", "track", "show", "episode", "audiobook"

offset - how many first items from the search you want to omit.

## toggleShuffleRequest(shuffle)

Enables shuffle if shuffle = True, disable shuffle if shuffle = False

## repeatModeRequest(state)

state = "track" - repeats the current track

state = "context" - repeats current context (album, playlist etc.)

state = "off" - disables repeat

## userProfileRequest()

Returns all data about current user

## playbackStateRequest()

Returns all data about current user's playback state


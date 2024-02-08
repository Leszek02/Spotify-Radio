import requests
import base64
import json
from urllib.parse import urlencode

class SpotifyRequests:


    def handleError(function_name, result): # Print every error according to Spotify manual
        if result == 400:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Bad Request")
        elif result == 401:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Bad Or Expired Token")
            SpotifyRequests.refreshAccessToken() #Refreshing token
        elif result == 403:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Forbidden Request (server refused to execute it)")
        elif result == 404:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Not Found - resource could not be found")
        elif result == 405:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Not Allowed")
        elif result == 429:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Too Many Requests")
        elif result == 500:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Internal Server Error ('You should never receive this error because our clever coders catch them all')")
        elif result == 502:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Bad Gateway")
        elif result == 503:
            print(f"Error when executing function: {function_name}")
            print(f"{result} - Service Unavailable")


    def classInterface(function_name, *args): # Use all methods using only this function, as error handling is here
        try:
            response = ""
            if callable(getattr(SpotifyRequests, function_name)):
                func = getattr(SpotifyRequests, function_name)
                response = func(*args)
                SpotifyRequests.handleError(function_name, response.status_code)
                if response.status_code == 401: # If token was expired, exec the function one again
                    response = func()
                    SpotifyRequests.handleError(function_name, response.status_code)
                print(f"Executed {function_name}.")
        except Exception as e:
            print(f"There was a problem executing {function_name}: ({e})")
        return response
    

    def authorizationRequest(): # returns authorization link, never manually use this function, server.py has only access to it
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            clientId = data.get("clientId")
            redirectUri = data.get("redirectUri")

        url = "https://accounts.spotify.com/authorize"
        scope = "user-modify-playback-state user-read-playback-state playlist-read-private"
        params = {
            "client_id": clientId,
            "response_type": "code",
            "redirect_uri": redirectUri,
            "scope": scope
        }
        
        authorization_url = f"{url}?{urlencode(params)}" # url to redirect the user
        print(f"Authorization url: {authorization_url}") 
        return authorization_url;

   
    def accessTokenRequest(): # Returns access and refresh token (Should only be used at the beggining, I guess only by the web page)
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            clientId = data.get("clientId")
            redirectUri = data.get("redirectUri")
            clientCode = data.get("clientCode")
            clientSecret = data.get("clientSecret")

        url = "https://accounts.spotify.com/api/token"
        params = {
            "grant_type": "authorization_code",
            "code": clientCode,
            "redirect_uri": redirectUri
        }
        clientString = f"{clientId}:{clientSecret}"
        step1 = clientString.encode('utf-8')
        step2 = base64.b64encode(step1)
        encodedClient = step2.decode('utf-8') # Now encoding is for sure correct, verified
        headers = {
            "Authorization": f"Basic {encodedClient}",
            "Content-Type": "application/x-www-form-urlencoded"   # need to convert these strings to base64
        }

        response = requests.post(url=url, params=params, headers=headers)
        json_data = response.json()
        data["accessToken"] = json_data.get("access_token")
        data["refreshToken"] = json_data.get("refresh_token")

        with open("./data/data.json", 'w') as json_file:
            json.dump(data, json_file, indent=2)

        return response;


    def refreshAccessToken(): # returns new access token (It is used in error handling, don't exec it manually)
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            clientId = data.get("clientId")
            clientSecret = data.get("clientSecret")
            refreshToken = data.get("refreshToken")

        url = "https://accounts.spotify.com/api/token"
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refreshToken
        }
        clientString = f"{clientId}:{clientSecret}"
        step1 = clientString.encode('utf-8')
        step2 = base64.b64encode(step1)
        encodedClient = step2.decode('utf-8') # Now encoding is for sure correct, verified
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encodedClient}"
        }

        response = requests.post(url=url, params=params, headers=headers)
        json_data = response.json()
        data["accessToken"] = json_data.get("access_token")

        with open("./data/data.json", 'w') as json_file:
            json.dump(data, json_file, indent=2)

        return response;


# ================================================================================================================================================================
    def stopRequest(): # Stops the music if it is played
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = "https://api.spotify.com/v1/me/player/pause"
        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        response = requests.put(url=url, headers=headers)
        return response;


    def playRequest(albumUri = "", type="", offset = 0): # Plays the music on user's device, supply whole playlist and number from what track to start (counting from 0!!!!)
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")
            deviceId = data.get("deviceId")

        url = "https://api.spotify.com/v1/me/player/play"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json",
            "device_id": deviceId
        }

        if type in ("album", "playlist", "artist"):
            params = {
                "context_uri": f"spotify:{type}:{albumUri}",
                "offset": {"position": offset}
            }
            response = requests.put(url=url, headers=headers, json=params)
        elif type == "track":
            params = {
                "uris": [f"spotify:{type}:{albumUri}"],
            }
            response = requests.put(url=url, headers=headers, json=params)
        else:
            response = requests.put(url=url, headers=headers)
        
        return response;


    def availableDevicesRequest(): # Collect all available devices and save Id of our raspberry, I think it should be executed with each boot
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")
        
        url = "https://api.spotify.com/v1/me/player/devices"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }
        response = requests.get(url=url, headers=headers)

        return response;


    def transferPlaybackRequest(deviceId): # Change active device for the one in data.json, for love of god I don't know why sometimes it works, and sometimes it just doesn't
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")
            deviceId = data.get("deviceId")

        url = "https://api.spotify.com/v1/me/player"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }
        params = {
            "device_ids": [deviceId], # it has to be one element array for some reasons
            "play": False
        }

        response = requests.put(url=url, headers=headers, data=json.dumps(params))
        print(response.status_code)
        return response;


    def skipToNextRequest(): # Play next track
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")
            deviceId = data.get("deviceId")

        url = "https://api.spotify.com/v1/me/player/next"
        headers = {
            "Authorization": f"Bearer {accessToken}"
        }
        params = {
            "device_id": deviceId
        }

        response = requests.post(url=url, headers=headers, data=json.dumps(params))
        return response;


    def skipToPreviousRequest(): # Play previous track
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")
            deviceId = data.get("deviceId")

        url = "https://api.spotify.com/v1/me/player/previous"
        headers = {
            "Authorization": f"Bearer {accessToken}"
        }
        params = {
            "device_id": deviceId
        }

        response = requests.post(url=url, headers=headers, data=json.dumps(params))
        return response;


    def playlistsRequest(): # Get user's playlists
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {accessToken}"
        }
        params = {
            "limit": 50,
            "offset": 0
        }

        response = requests.get(url=url, headers=headers, params=params)
        return response;


    def playlistContentRequest(playlistId): # Get playlist's all tracks (All names and their id's in Spotify order)
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/playlists/{playlistId}"
        headers = {
            "Authorization": f"Bearer {accessToken}"
        }
        params = {
            "fields": "tracks.items(track(name,id))" # Without space after comma, spent to much time on this 
        }

        response = requests.get(url=url, headers=headers, params=params)
        return response;


    def searchForItemRequest(searchedString, type, offset):  # SearchedString - item's name, type - album, artist, track etc., offset - I set to return 10 items only, set offset to +10 to receive ten next items
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/search?q={searchedString}&type={type}&market=PL&limit=10&offset={offset}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "type": "album"
        }

        response = requests.get(url=url, headers=headers)
        return response;


    def changeVolumeRequest(volumeValue):
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volumeValue}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.put(url=url, headers=headers)
        return response;


    def toggleShuffleRequest(shuffle):
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/me/player/shuffle?state={shuffle}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.put(url=url, headers=headers)
        return response;


    def repeatModeRequest(state):
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/me/player/repeat?state={state}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.put(url=url, headers=headers)
        return response;

    
    def userProfileRequest():
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.get(url=url, headers=headers)
        return response;


    def playbackStateRequest():
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)
            accessToken = data.get("accessToken")

        url = f"https://api.spotify.com/v1/me/player"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }

        response = requests.get(url=url, headers=headers)
        return response;
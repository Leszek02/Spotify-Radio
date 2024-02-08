import json
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from spotifyClass import SpotifyRequests

app = Flask(__name__, template_folder='WebPage')  # WebPage is a folder for our page
CORS(app)


@app.route('/')  # Spotify redirects here, needs this to scrap the auth code
def redirectPath():
    if 'code' in request.args:
        with open("./data/data.json", 'r') as json_file:
            data = json.load(json_file)

        data["clientCode"] = request.args.get('code')

        with open("./data/data.json", 'w') as json_file:
            json.dump(data, json_file, indent=2)

        spotify.accessTokenRequest()  # use client code to receive access token and refresh token
    return redirect(url_for('mainPage'))  # redirect user to mainPage


@app.route('/main')
def mainPage():
    app.logger.info('Rendering page')
    return render_template('index.html');


@app.route('/getAuthorizationRequest')  # Execute authorization methods
def receiveAuthUrl():
    url = spotify.authorizationRequest()
    return { "url": url }  # return spotify authentication URL (needs to be done once, if we have auth code saved it can be used as long as the user does not delete it)


@app.route('/putPlaySongRequest/<playlist_id>/<track>', methods=['PUT'])  #
def receivePlaySongUrl(playlist_id, track):
    try:
        response = spotify.classInterface("playRequest", playlist_id, "playlist", track)
        return str(response.status_code)
    except Exception as e:
        return str(e), 500


@app.route('/putPlayRequest', methods=['PUT'])  #
def receivePlayUrl():
    try:
        response = spotify.classInterface("playRequest")
        return str(response.status_code)
    except Exception as e:
        return str(e), 500


@app.route('/putStopRequest', methods=['PUT', 'GET'])  #
def receiveStopUrl():
    try:
        response = spotify.classInterface("stopRequest")
        return str(response.status_code)
    except Exception as e:
        return str(e), 500 


@app.route('/putNextSkipRequest', methods=['POST'])  #
def receiveSkipToNextUrl():
    try:
        response = spotify.classInterface("skipToNextRequest")
        return str(response.status_code)
    except Exception as e:
        return str(e), 500


@app.route('/putPreviousSkipRequest', methods=['POST'])  #
def receiveSkipToPreviousUrl():
    try:
        response = spotify.classInterface("skipToPreviousRequest")
        return str(response.status_code)
    except Exception as e:
        return str(e), 500


@app.route('/playbackStateRequest', methods=['GET'])  #
def receiveplaybackStateRequestUrl():
    try:
        response = spotify.classInterface("playbackStateRequest")
        return response.json()
    except Exception as e:
        return str(e), 500


@app.route('/playlistContentRequest/<name_id>', methods=['GET'])  #
def receiveplaylistContentRequest(name_id):
    try:
        response = spotify.classInterface("playlistContentRequest", name_id);
        return response.json()
    except Exception as e:
        return str(e), 500 


@app.route('/playlistRequest', methods=['GET'])  #
def receiveplaylistRequest():
    try:
        response = spotify.classInterface("playlistsRequest");
        return response.json()
    except Exception as e:

        return str(e), 500 
    

@app.route('/toggleRepeat/<option>', methods=['PUT', 'GET'])  #
def toggleRepeat(option):
    try:
        response = spotify.classInterface("repeatModeRequest", option);
        return response.json()
    except Exception as e:
        # Log the exception or handle it appropriately
        return str(e), 500  # Return an error message and set the status code to 500
    

@app.route('/toggleShuffle/<option>', methods=['PUT', 'GET'])  #
def toggleShuffle(option):
    try:
        response = spotify.classInterface("toggleShuffleRequest", option);
        return response.json()
    except Exception as e:
        # Log the exception or handle it appropriately
        return str(e), 500  # Return an error message and set the status code to 500


# Main program here
if __name__ == '__main__':
    spotify = SpotifyRequests;
    app.run(port=5500, debug=True)
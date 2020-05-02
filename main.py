from Analyzer import Analyzer
from Game import Game, GameProperties
from Grid import Grid
from PrefixTrie import PrefixTrie
from flask import Flask, render_template, request, session  
from flask_socketio import SocketIO, send, emit, join_room, leave_room

GAMELIMIT = 10

app = Flask(__name__)
socketio = SocketIO(app)

def send_game_update(gid, transition, message):
    if gid in games.keys():
        socketio.emit("game_state_update", {"transition": transition, "message": message, "game": games[str(gid)].encode()}, room = str(gid))

def list_request_callback(gid):
    if gid in games.keys():
        socketio.emit("list_request", room = str(gid))

def send_analysis_callback(gid, analysis):
    if gid in games.keys():
        socketio.emit("game_analysis", analysis, room = str(gid))

@app.route("/lobby")
def temporary_redirect():
    return "Please go to /join/GAME to join a game."

@app.route("/create/<gid>/<int:height>/<int:width>/<int:min_letters>/<int:minutes>/<language>")
def create_game(gid, height, width, min_letters, minutes, language):
    if gid not in games.keys():
        grid = Grid(width, height, True)
        analyzer = Analyzer(lexicons.get(language.lower(), lexicons["english"]), language)
        games[gid] = Game(gid, GameProperties(min_letters = min_letters, minutes = minutes), grid, analyzer, send_game_update, list_request_callback, send_analysis_callback)
        return "Successfully created game {gid} with size {height}x{width}, letter minimum {min_letters}, time limit {minutes} minutes, and language {language}".format(gid = games[gid].gid, height = games[gid].grid.height, width = games[gid].grid.width, min_letters = games[gid].properties.min_letters, minutes = games[gid].properties.minutes, language = games[gid].analyzer.language)
    else:
        return "Game already exists!"

@app.route("/game/<gid>")
def join_game(gid):
    if gid not in games.keys():
        return "Game {0} not found!".format(gid)
    return render_template("game.html", gid = gid)

@socketio.on("game_join")
def handle_game_join_event(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if games[json["gid"]].add_player(json["username"]):  
        player_map[request.sid] = (json["gid"], json["username"])      
        join_room(json["gid"])
        send_game_update(json["gid"], None, "{0} has joined the game!".format(json["username"]))
    else:
        emit("join_failed_error")

@socketio.on("disconnect")
def handle_disconnect(methods = ["GET", "POST"]):
    # Only handle this if the player is still in a game.
    if request.sid in player_map.keys():
        gid, username = player_map[request.sid]
        games[gid].remove_player(username)
        if games[gid].num_players() == 0:
            del games[gid]
        else:
            send_game_update(gid, None, "{0} has left the game!".format(username))
        del player_map[request.sid]

@socketio.on("game_leave")
def handle_game_leave_event(json, methods = ["GET", "POST"]):
    if json["gid"] in games.keys():
        games[json["gid"]].remove_player(json["username"])
        if games[json["gid"]].num_players() == 0:
            del games[json["gid"]]
        else:
            send_game_update(json["gid"], None, "{0} has left the game!".format(json["username"]))
        del player_map[request.sid]
        leave_room(json["gid"])

@socketio.on("game_start")
def handle_game_start_event(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if not games[json["gid"]].has_player(json["username"]):
        emit("wrong_game_error")
    games[json["gid"]].start_round()
    send_game_update(json["gid"], "ROUND_START", "Round has begun!")

@socketio.on("list_submit")
def handle_list_submit(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if not games[json["gid"]].add_player_list(json["username"], json["list"]):
        emit("list_submit_failed_error")
    
@socketio.on("chat_message")
def handle_chat_message(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if not games[json["gid"]].has_player(json["username"]):
        emit("wrong_game_error")
    emit("chat_message", json, room = str(json["gid"]))
    
if __name__ == "__main__":    
    print('Starting Boggle server!')
    print('Loading dictionaries...')
    lexicons = dict()
    lexicons["english"] = PrefixTrie("lexicons/csw_en.txt")
    lexicons["french"] = PrefixTrie("lexicons/ods5_fr.txt")
    print('Dictionaries loaded!')

    # Maps GID to Game.
    games = dict()

    # Maps Flask SocketIO Session ID to (gid, username) pairs.
    player_map = dict()

    socketio.run(app, debug=True)
    #socketio.run(app, host='0.0.0.0', debug=False)
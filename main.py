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
        socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")
        

@app.route("/lobby")
def temporary_redirect():
    return render_template("lobby.html")

@app.route("/game/<gid>")
def join_game(gid):
    if gid not in games.keys():
        return "Game {0} not found!".format(gid)
    return render_template("game.html", gid = gid)

@socketio.on("lobby_join")
def handle_lobby_join(methods = ["GET", "POST"]):
    join_room("lobby")
    socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() })

@socketio.on("game_create")
def handle_game_create(json, methods = ["GET", "POST"]):
    if json["gid"] == "lobby" or json["gid"] in games.keys():
        return
    grid = Grid(json["width"], json["height"], True)
    analyzer = Analyzer(lexicons.get(json["language"].lower(), lexicons["english"]), json["language"])
    games[json["gid"]] = Game(json["gid"], GameProperties(min_letters = json["minLetters"], minutes = json["minutes"]), grid, analyzer, send_game_update, list_request_callback, send_analysis_callback)
    socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")

@socketio.on("game_join")
def handle_game_join_event(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if games[json["gid"]].add_player(json["username"]):  
        player_map[request.sid] = (json["gid"], json["username"])      
        join_room(json["gid"])
        send_game_update(json["gid"], None, "{0} has joined the game!".format(json["username"]))
        socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")
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
        socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")
        del player_map[request.sid]

@socketio.on("game_leave")
def handle_game_leave_event(json, methods = ["GET", "POST"]):
    if json["gid"] in games.keys():
        games[json["gid"]].remove_player(json["username"])
        if games[json["gid"]].num_players() == 0:
            del games[json["gid"]]
        else:
            send_game_update(json["gid"], None, "{0} has left the game!".format(json["username"]))
        socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")
        del player_map[request.sid]
        leave_room(json["gid"])

@socketio.on("lobby_leave")
def handle_lobby_leave_event(methods = ["GET", "POST"]):
    leave_room("lobby")

@socketio.on("game_start")
def handle_game_start_event(json, methods = ["GET", "POST"]):
    if json["gid"] not in games.keys():
        emit("game_dne_error")
        return
    if not games[json["gid"]].has_player(json["username"]):
        emit("wrong_game_error")
    games[json["gid"]].start_round()
    socketio.emit("game_list_update", { gid:(g.encode()) for gid,g in games.items() }, room = "lobby")
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
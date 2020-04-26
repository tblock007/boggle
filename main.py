from Analyzer import Analyzer
from Game import Game, GameProperties
from Grid import Grid
from PrefixTrie import PrefixTrie
from flask import Flask, render_template, request, session  
from flask_socketio import SocketIO, send, emit, join_room, leave_room

GAMELIMIT = 10

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def temporary_redirect():
    return "Please go to *.html/join/GAME to join a game."

@app.route("/create/<gid>/<int:height>/<int:width>/<int:min_letters>/<int:minutes>/<language>")
def create_game(gid, height, width, min_letters, minutes, language):
    grid = Grid(width, height, True)
    analyzer = Analyzer(lexicons.get(language.lower(), english_lexicon), language)
    games[gid] = Game(gid, GameProperties(min_letters = min_letters, minutes = minutes), grid, analyzer)
    return "Successfully created game {gid} with size {height}x{width}, letter minimum {min_letters}, time limit {minutes} minutes, and language {language}".format(gid = games[gid].gid, height = games[gid].grid.height, width = games[gid].grid.width, min_letters = games[gid].properties.min_letters, minutes = games[gid].properties.minutes, language = games[gid].analyzer.language)

@app.route("/join/<gid>")
def join_game(gid):
    if gid not in games.keys():
        return "Game {0} not found!".format(gid)
    return "Joined {0}!".format(gid)

@socketio.on("game_join")
def handle_join_game_event(json, methods = ["GET", "POST"]):
    gid = json["id"]
    username = json["username"]
    if gid not in games.keys():
        emit("game_join_response", '{ "response": "DOES_NOT_EXIST" }')
        return
    join_room(gid)
    games[gid].add_player(username)

@socketio.on("game_start")
def handle_game_start_event(json, methods = ["GET", "POST"]):
    gid = json["gid"]
    username = json["username"]
    if gid not in games.keys():
        emit("game_start_response", '{ "response": "DOES_NOT_EXIST" }')
        return
    if not games[gid].has_player(username):
        emit("game_start_response", '{ "response": "GAME_NOT_JOINED" }')
    games[gid].start_round()

    

if __name__ == "__main__":    
    print('Starting Boggle server!')
    print('Loading dictionaries...')
    lexicons = dict()
    # englishDictionary = PrefixTrie("dictionaries/csw_en.txt")
    # frenchDictionary = PrefixTrie("dictionaries/ods5_fr.txt")
    english_lexicon = PrefixTrie("lexicons/prefix_trie_test.txt")
    print('Dictionaries loaded!')

    games = dict()
    player_map = dict()

    socketio.run(app, debug=True)
    #socketio.run(app, host='0.0.0.0', debug=False)
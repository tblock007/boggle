from Game import Game
from PrefixTrie import PrefixTrie
from flask import Flask, render_template      
from flask_socketio import SocketIO, send, emit, join_room, leave_room

GAMELIMIT = 5

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def render_client():
    return render_template("home.html")


@socketio.on('connect')
def handle_connection(methods = ['GET', 'POST']):
    print('User joined!')
    emit('user_join_response')


@socketio.on('game_creation')
def handle_game_creation_event(json, methods = ['GET', 'POST']):

    user = json['user']
    gid = json['gid']
    ogid = json['old_gid']
    if ogid:        
        leave_room(str(ogid))
        games[ogid].removePlayer(user)

    if gid in games.keys():
        emit('game_creation_response', '{ "response": "NOTUNIQUE" }')
    elif len(games) >= GAMELIMIT:
        emit('game_creation_response', '{ "response": "TOOMANY" }')
    else:
        games[gid] = Game(gid, 4, False, englishDictionary) # these will be obtained from response eventually
        join_room(str(gid))
        games[gid].addPlayer(user)
        emit('game_creation_response', '{{ "response": "OK", {0} }}'.format(str(games[gid])))


@socketio.on('game_join')
def handle_game_join_event(json, methods = ['GET', 'POST']):

    user = json['user']
    gid = json['gid']
    ogid = json['old_gid']
    if ogid:
        leave_room(str(ogid))
        games[ogid].removePlayer(user)

    if gid not in games.keys():
        emit('game_join_response', '{ "response": "DOESNOTEXIST" }')
    else:
        join_room(str(gid))
        games[gid].addPlayer(user)
        emit('game_join_response', '{{ "response": "OK", {0} }}'.format(str(games[gid])))


@socketio.on('board_gen')
def handle_board_gen_event(json, methods = ['GET', 'POST']):

    gid = json['gid']

    if gid not in games.keys():
        emit('new_board', '{ "response": "DOESNOTEXIST" }')
    else:
        games[gid].newRound()
        emit('new_board', '{{ {0} }}'.format(str(games[gid])), room = str(gid))


@socketio.on('end_game')
def handle_end_game(json, methods = ['GET', 'POST']):

    gid = json['gid']    
    emit('list_request', room = str(gid))


@socketio.on('list_submit')
def handle_list_submit(json, methods = ['GET', 'POST']):

    gid = json['gid']
    user = json['user']
    wordList = json['list']

    games[gid].setList(user, wordList)
    if (games[gid].allListsSubmitted()):
        result = games[gid].roundResult()
        emit('game_result', result, room = str(gid))


if __name__ == "__main__":    

    print('Starting Boggle server!')
    print('Loading dictionaries...')
    englishDictionary = PrefixTrie("dictionaries/english.txt")
    frenchDictionary = PrefixTrie("dictionaries/french.txt")
    print('Dictionaries loaded!')

    games = dict()

    #socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', debug=False)
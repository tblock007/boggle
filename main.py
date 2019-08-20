from Game import Game
from PrefixTrie import PrefixTrie
from flask import Flask, render_template, request      
from flask_socketio import SocketIO, send, emit, join_room, leave_room

GAMELIMIT = 5

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def render_client():
    return render_template("game.html")

@app.route("/old")
def render_game():
    return render_template("home.html")


@socketio.on('connect')
def handle_connection(methods = ['GET', 'POST']):
    print('\n** USER UPDATE: User joined! SID: {0}\n'.format(request.sid))
    emit('user_join_response')

@socketio.on('disconnect')
def handle_disconnection(methods = ['GET', 'POST']):
    global games
    print('\n** USER UPDATE: {0} disconnected\n'.format(request.sid))
    for gid in games.keys():
        games[gid].removePlayer(request.sid)
    games = { i:g for i,g in games.items() if g.numPlayers() > 0 }

@socketio.on('game_creation')
def handle_game_creation_event(json, methods = ['GET', 'POST']):

    gid = json['gid']
    ogid = json['old_gid']
    height = json['height']
    width = json['width']
    minLetters = json['minimumLetters']
    includeDoubleLetterCube = json['includeDoubleLetterCube']
    language = json['language']

    if gid in games.keys():
        emit('game_creation_response', '{ "response": "NOTUNIQUE" }')
        return

    if len(games) >= GAMELIMIT:
        emit('game_creation_response', '{ "response": "TOOMANY" }')
        return

    if ogid and ogid != gid and ogid in games.keys():        
        leave_room(str(ogid))
        games[ogid].removePlayer(request.sid)
        if games[ogid].numPlayers() == 0:
            del games[ogid]

    games[gid] = Game(gid, height, width, minLetters, includeDoubleLetterCube, frenchDictionary if language.lower() == 'french' else englishDictionary)
    join_room(str(gid))
    games[gid].addPlayer(request.sid)
    emit('game_creation_response', '{{ "response": "OK", {0} }}'.format(str(games[gid])))


@socketio.on('game_join')
def handle_game_join_event(json, methods = ['GET', 'POST']):

    gid = json['gid']
    ogid = json['old_gid']

    if gid not in games.keys():
        emit('game_join_response', '{ "response": "DOESNOTEXIST" }')
        return

    if ogid and ogid == gid:
        emit('game_join_response', '{ "response": "ALREADYJOINED" }')
        return

    if ogid and ogid != gid and ogid in games.keys():
        leave_room(str(ogid))
        games[ogid].removePlayer(request.sid)
        if games[ogid].numPlayers() == 0:
            del games[ogid]
           
    join_room(str(gid))
    games[gid].addPlayer(request.sid)
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
    games[gid].resetResults()    
    emit('list_request', room = str(gid))

@socketio.on('solve_game')
def handle_end_game(json, methods = ['GET', 'POST']):

    gid = json['gid']
    result = {}
    result['wordlist'] = games[gid].solve()   
    emit('game_solution', result, room = str(gid))

@socketio.on('list_submit')
def handle_list_submit(json, methods = ['GET', 'POST']):

    username = json['username']
    gid = json['gid']
    wordList = json['list']

    games[gid].setList(request.sid, username, wordList)
    if (games[gid].allListsSubmitted()):
        result = {}
        result['results'] = games[gid].roundResult()
        emit('game_result', result, room = str(gid))

@socketio.on('new_message')
def handle_new_message(json, methods = ['GET', 'POST']):
    gid = json['gid']
    
    print('\n\n NEW MESSAGE {0}\n\n'.format(json['message']))
    emit('incoming_message', json, room = str(gid))


if __name__ == "__main__":    

    print('Starting Boggle server!')
    print('Loading dictionaries...')
    englishDictionary = PrefixTrie("dictionaries/csw_en.txt")
    frenchDictionary = PrefixTrie("dictionaries/ods5_fr.txt")
    print('Dictionaries loaded!')

    games = dict()

    #socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', debug=False)
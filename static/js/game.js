function log_message(usr, msg) {
    if (usr == '') {
        $('#log').append('<div><b>' + msg + '</b></div>')
    }
    else {
        $('#log').append('<div><b>' + usr + ':</b> ' + msg + '</div>')
    }
    console.log(usr + ' - ' + msg)
}

function draw_board(grid, width, height) {
    board = grid.split(',')
    html = ''
    var i = 0
    for (let row = 0; row < height; row++) {
        for (let col = 0; col < width; col++) {
            html += '<div class="lettercontainer"><div class="letter">' + board[i] + '</div></div>'
            i++
        }
    }
    $('#board').html(html)
}


function rotate(grid, width, height) {

    board = grid.split(',')
    newboard = []

    for (var col = width - 1; col >= 0; col--) {
        for (var row = 0; row < height; row++) {
            var i = (row * width) + col
            newboard.push(board[i]) 
        }
    }

    return newboard.join(',')
}

var main = (function () {

    let gameSocket = io.connect('http://' + document.domain + ':' + location.port);
    let gameGid = null
    let gameHeight = 5
    let gameWidth = 5
    let gameGrid = null

    let words = []

    $('#writeword').keydown(function (e) {
        if (e.keyCode == 13) { // the enter key code            
            let w = $('#writeword').val().toUpperCase()
            if (w !== '') {
                $('#writeword').val('')            
                words.push(w)
                $('#wordlist').append('<li>' + w + '</li>')
            }
        }
        else if (e.keyCode == 46) { // the delete key code
            words.pop()
            $('#wordlist li:last-child').remove()
        }
    })

    gameSocket.on('connect', function () {
        gameSocket.emit('user_join')

        $('#createform').on('submit', function (e) {
            e.preventDefault()
            let game_id = $('#creategameid').val()
            let user = $('#usernameField').val()
            if (game_id !== '') {
                gameSocket.emit('game_creation', {
                    user: user,
                    old_gid: gameGid,
                    gid: game_id
                })
                $('#creategameid').val('')
            }
            else {
                log_message('ERROR', 'Please enter a game ID')
            }
        })
        $('#joinform').on('submit', function (e) {
            e.preventDefault()
            let game_id = $('#joingameid').val()
            let user = $('#usernameField').val()
            if (game_id !== '') {
                gameSocket.emit('game_join', {
                    user: user,
                    old_gid: gameGid,
                    gid: game_id
                })
                $('#joingameid').val('')
            }
            else {
                log_message('ERROR', 'Please enter a game ID')
            }
        })

        $('#genform').on('submit', function (e) {
            e.preventDefault()
            let user = $('#usernameField').val()
            gameSocket.emit('board_gen', {
                user: user,
                gid: gameGid
            })
        })

        $('#endform').on('submit', function (e) {
            e.preventDefault()
            let user = $('#usernameField').val()
            gameSocket.emit('end_game', {
                user: user,
                gid: gameGid
            })
        })

        $('#rotate').on('submit', function (e) {
            e.preventDefault()
            gameGrid = rotate(gameGrid, gameWidth, gameHeight)
            var temp = gameWidth
            gameWidth = gameHeight
            gameHeight = temp
            draw_board(gameGrid, gameWidth, gameHeight)
        })
    })


    gameSocket.on('game_creation_response', function (msg) {
        resp = JSON.parse(msg)
        if (resp.response == 'OK') {
            gameGid = resp.gid
            gameGrid = resp.grid
            draw_board(gameGrid, gameWidth, gameHeight)
            log_message('Server', 'Game created: ' + resp.gid)
            log_message('Server', 'Joined game: ' + gameGid)
        }
        else if (resp.response == 'NOTUNIQUE') {
            log_message('Server', 'Error: game already exists!')
        }
        else if (resp.response == 'TOOMANY') {
            log_message('Server', 'Game limit reached!  Please wait before creating new games')
        }
    })

    gameSocket.on('game_join_response', function (msg) {
        resp = JSON.parse(msg)
        if (resp.response == 'OK') {
            gameGid = resp.gid
            gameGrid = resp.grid
            draw_board(gameGrid, gameWidth, gameHeight)
            log_message('Server', 'Joined game: ' + gameGid)
        }
        else if (resp.response == 'DOESNOTEXIST') {
            log_message('Server', 'Error: game does not exist.')
        }
    })

    gameSocket.on('user_join_response', function (msg) {
        console.log('Received response from server')
    })

    gameSocket.on('new_board', function (msg) {
        resp = JSON.parse(msg)
        if (resp.gid == gameGid) { 
            gameGrid = resp.grid   
            words = []
            $('#wordlist').html('')
            log_message('', 'Game starting in 5 seconds!')
            setTimeout(function() {
                draw_board(gameGrid, gameWidth, gameHeight)
                log_message('Server', 'New board has been set!')
            }, 5000)    
        }
    })

    gameSocket.on('list_request', function () {

        log_message('', 'Submitting list of found words')
        let user = $('#usernameField').val()
        gameSocket.emit('list_submit', {
            user: user,
            gid: gameGid,
            list: words
        })
    })

    gameSocket.on('game_result', function (msg) {
        resp = JSON.parse(msg)
        scoreboardHTML = '<div id ="scoreboard"><div class="closebutton">CLOSE</div>'
        for (let key in resp) {
            if (resp.hasOwnProperty(key)) {
                scoreboardHTML += '<div class="playerscoreboard">'
                scoreboardHTML += key
                scoreboardHTML += ':<br/>Score: '
                scoreboardHTML += resp[key].totalScore
                scoreboardHTML += '<ul>'
                for (let i in resp[key].invalid) {
                    scoreboardHTML += '<li><s>' + resp[key].invalid[i] + '</s>???</li>'
                }
                for (let i in resp[key].struck) {
                    scoreboardHTML += '<li><s>' + resp[key].struck[i] + '</s></li>'
                }
                for (let i in resp[key].scored) {
                    scoreboardHTML += '<li><div class="wordscore">' + resp[key].scores[i] + '</div> ' + resp[key].scored[i] + '</li>'
                }
                scoreboardHTML += '</ul></div>'
            }
        }
        scoreboardHTML += '</div>'
        $('body').append(scoreboardHTML)

        $('.closebutton').on('click', function () {
            $('#scoreboard').remove()
        })
    })


})();





class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: null,
            gid: props.gid,
            gameState: null,
            letters: [[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']],
            minimumLetters: null,
            minutes: null,
            language: null,
            playerScores: null,

            socket: null,
            words: [],
            messages: [],

            roundEndTime: null,
            modalMessage: null,
            lastScoreboard: null,
            lastSolvedList: null
        };
    }

    updateGameState(game) {
        this.setState({
            gid: game.gid,
            gameState: game.state,
            minimumLetters: game.min_letters,
            minutes: game.minutes,
            language: game.language,
            playerScores: game.player_scores,
        });

        if (game.grid !== null) {
            this.setState({ letters: game.grid });
        }
    }

    componentDidMount() {
        this.state.socket = io.connect("http://" + document.domain + ":" + location.port);
        this.state.socket.on("game_state_update", (resp) => {
            this.updateGameState(resp.game);
            this.log("Server", resp.message);
        });
        this.state.socket.on("list_request", () => {
            this.state.socket.emit("list_submit", {
                username: this.state.username,
                gid: this.state.gid,
                list: this.state.words
            });
        }); 
        this.state.socket.on("chat_message", resp => { 
            this.log(resp.username, resp.message); 
            $('.messages').scrollTop($('.messages')[0].scrollHeight + 300);
        });
        this.state.socket.on("game_dne_error", () => {
            alert('Game ' + this.state.gid + ' no longer exists!');
        });
        this.state.socket.on("wrong_game_error", () => {
            alert('You are not authorized to participate in game ' + this.state.gid + '. Please log out and try re-joining.');
        });
        this.state.socket.on("join_failed_error", () => {
            alert('Could not join game ' + this.state.gid + '. Either a round is in progress, or there could be a username conflict.');
        });
        this.state.socket.on("list_submit_failed_error", () => {
            alert('Could not submit word list to game ' + this.state.gid);
        });        
        
        setInterval(() => {this.forceUpdate()}, 1000);
    }

    padzero(n) {
        if (n <= 9) return ("0" + n.toString());
        return n.toString();
    }

    log(sender, message) {
        let now = new Date();
        this.setState({ messages: this.state.messages.concat([{
            timestamp: this.padzero(now.getHours()) + ":" + this.padzero(now.getMinutes()) + ":" + this.padzero(now.getSeconds()),
            sender: sender,
            content: message
        }])});
    }

    addWord(w) {
        this.setState({ words: [w.toUpperCase()].concat(this.state.words)});
    }

    removeWord() {
        this.setState({ words: this.state.words.slice(1)});
    }

    sendMessage(msg) {
        this.state.socket.emit('chat_message', { 
            gid: this.state.gid, 
            username: this.state.username, 
            message: msg
        });
    }

    startRound() {
        this.state.socket.emit("game_start", {
            username: this.state.username,
            gid: this.state.gid,
        });
    }

    // TODO: Eliminate this call in favor of server-side scheduling
    endRound() {
        this.state.socket.emit("game_end", {
            username: this.state.username,
            gid: this.state.gid,
        });
    }

    rotateBoard() {
        const height = this.state.letters.length;
        const width = this.state.letters[0].length;
        const oldLetters = this.state.letters;

        let newLetters = [];
        for (let col = width - 1; col >= 0; col--) {
            newLetters.push([]);
            for (let row = 0; row < height; row++) {
                newLetters[width - 1 - col].push(oldLetters[row][col]);
            }
        }
        this.setState({ letters: newLetters });
    }

    flipBoardHorizontal() {
        const height = this.state.letters.length;
        const width = this.state.letters[0].length;
        const oldLetters = this.state.letters;
        let newLetters = [];
        for (let row = 0; row < height; row++) {
            newLetters.push([]);
            for (let col = width - 1; col >= 0; col--) {
                newLetters[row].push(oldLetters[row][col]);
            }
        }
        this.setState({ letters: newLetters });
    }

    flipBoardVertical() {
        const height = this.state.letters.length;
        const width = this.state.letters[0].length;
        const oldLetters = this.state.letters;
        let newLetters = [];
        for (let row = height - 1; row >= 0; row--) {
            newLetters.push([]);
            for (let col = 0; col < width; col++) {
                newLetters[height - 1 - row].push(oldLetters[row][col]);
            }
        }
        this.setState({ letters: newLetters });
    }

    timeRemaining() {
        return "0:00"
    }

    render() {
        if (this.state.gameState === null) {
            return (
                <div>
                    <LoginDialog
                        setUsername={(name) => {
                            if (name !== "") {
                                this.setState({ username: name });
                                this.state.socket.emit("game_join", {
                                    username: name,
                                    gid: this.state.gid,
                                });
                            }
                        }}
                    />
                </div>
            )
        }
        return (
            <div>
                <Game 
                    letters={this.state.letters}
                    words={this.state.words}
                    addWord={(w) => this.addWord(w)} 
                    removeWord={() => this.removeWord()}
                    rotate={() => this.rotateBoard()}
                    flipH={() => this.flipBoardHorizontal()}
                    flipV={() => this.flipBoardVertical()} 
                />
                <ControlPanel 
                    gid={this.state.gid}
                    minLetters={this.state.minimumLetters}
                    language={this.state.language}
                    messages={this.state.messages}
                    roundTimeRemaining={this.timeRemaining()}                   
                    onEnterMessage={(msg) => this.sendMessage(msg)}
                    onStartClicked = {() => this.startRound()}
                    onEndClicked = {() => this.endRound()}
                    onRotateClicked = {() => this.rotateBoard()}
                    onFlipHorizontalClicked = {() => this.flipBoardHorizontal()}
                    onFlipVerticalClicked = {() => this.flipBoardVertical()}
                />
            </div>
        )
    }
}


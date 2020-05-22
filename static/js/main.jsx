class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: null,
            gid: props.gid,
            gameState: null,
            letters: [[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']],
            minLetters: null,
            minutes: null,
            language: null,
            playerScores: null,

            socket: null,
            words: [],
            messages: [],

            roundEndTime: null,
            scoreboard: null,
            solution: null,
            mostInvalid: null,
            mostStruck: null,
            longestWord: null,
            gamePanelMode: "word-input",
        };
    }

    updateGameState(game) {
        this.setState({
            gid: game.gid,
            gameState: game.state,
            minLetters: game.min_letters,
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
            if (resp.transition != null) {
                if (resp.transition === "ROUND_START") {
                    this.setState({ words: [], scoreboard: null, solution: null, gamePanelMode: "word-input" });         
                    this.setState({ roundEndTime: new Date((new Date().getTime()) + this.state.minutes * 60 * 1000) });
                }
                else if (resp.transition === "ROUND_END") {
                    this.setState({ gamePanelMode: "scoreboard" });
                }
            }   
            
            if (resp.message != null) {
                this.log("Server", resp.message);  
                $('.messages').scrollTop($('.messages')[0].scrollHeight + 300); 
            }         
        });
        this.state.socket.on("list_request", () => {
            this.state.socket.emit("list_submit", {
                username: this.state.username,
                gid: this.state.gid,
                list: this.state.words
            });
        });
        this.state.socket.on("game_analysis", resp => {
            this.setState({ scoreboard: resp.scoreboard, solution: resp.solution, mostInvalid: resp.most_invalid, mostStruck: resp.most_struck, longestWord: resp.longest_word });
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
        window.addEventListener("beforeunload", (event) => {
            this.leaveGame(false);
        });
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

    requestDefinition(word) {
        this.state.socket.emit('definition_request', {
            gid: this.state.gid,
            username: this.state.username,
            language: this.state.language,
            word: word
        });
    }

    startRound() {
        this.state.socket.emit("game_start", {
            username: this.state.username,
            gid: this.state.gid,
        });
    }

    setGamePanelMode(mode) {
        this.setState({ gamePanelMode: mode });
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

    leaveGame(redirect) {
        this.state.socket.emit("game_leave", {
            username: this.state.username,
            gid: this.state.gid,
        });
        if (redirect) {
            // Redirect back to lobby after 0.2s to allow game_leave to send.
            setTimeout(() => { window.location = "/lobby"; }, 200);
        }
    }

    timeRemaining() {
        if (this.state.roundEndTime === null) {
            return null;
        }
        const now = new Date().getTime();
        const distance = this.state.roundEndTime - now;
        if (distance < 0) {
            return null;
        }
        const minutes = Math.floor(distance / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        return minutes.toString() + ":" + ((seconds <= 9) ? "0" : "") + seconds.toString();
    }

    render() {
        if (this.state.gameState === null) {
            return (
                <div>
                    <LoginDialog
                        setUsername={(name) => {
                            if (name !== "" && name.toLowerCase() !== "server" && name.toLowerCase() !== "definition") {
                                this.setState({ username: name });
                                this.state.socket.emit("game_join", {
                                    username: name,
                                    gid: this.state.gid,
                                });
                            }
                        }}
                        gid={this.state.gid}
                    />
                </div>
            )
        }
        return (
            <div>
                <Game 
                    letters={this.state.letters}
                    minLetters={this.state.minLetters}
                    words={this.state.words}
                    addWord={(w) => this.addWord(w)} 
                    removeWord={() => this.removeWord()}
                    rotate={() => this.rotateBoard()}
                    flipH={() => this.flipBoardHorizontal()}
                    flipV={() => this.flipBoardVertical()} 
                    scoreboard={this.state.scoreboard}
                    solution={this.state.solution}
                    mostInvalid = {this.state.mostInvalid}
                    mostStruck = {this.state.mostStruck}
                    longestWord = {this.state.longestWord}
                    gamePanelMode={this.state.gamePanelMode}
                    setGamePanelMode={(mode) => this.setGamePanelMode(mode)}
                    requestDefinition = {(word) => this.requestDefinition(word)}
                />
                <ControlPanel 
                    gid={this.state.gid}
                    gameState={this.state.gameState}
                    minLetters={this.state.minLetters}
                    language={this.state.language}
                    messages={this.state.messages}
                    roundTimeRemaining={this.timeRemaining()}                   
                    onEnterMessage={(msg) => this.sendMessage(msg)}
                    onStartClicked = {() => this.startRound()}
                    onRotateClicked = {() => this.rotateBoard()}
                    onFlipHorizontalClicked = {() => this.flipBoardHorizontal()}
                    onFlipVerticalClicked = {() => this.flipBoardVertical()}
                    onLeaveGameClicked = {() => this.leaveGame(true)}
                    requestDefinition = {(word) => this.requestDefinition(word)}
                    playerScores = {this.state.playerScores}
                />
            </div>
        )
    }
}


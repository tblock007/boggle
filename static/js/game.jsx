class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = { username: "" };
    }

    render() {        
        return (
            <div className="login">
                <input 
                    type="text" value={this.state.username} 
                    onChange={(e) => this.setState({ username: e.target.value })} 
                    placeholder="Enter username" 
                />
                <button className="other-button" onClick={() => this.props.setUsername(this.state.username)}>JOIN!</button>
            </div>
        );
    }
}

class WordInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = { word: "" };
    }

    handleKeyDown(e) {
        if (e.keyCode == 13) { // the enter key code    
            if (this.state.word !== "") {
                this.setState({ word: "" });
                this.props.onEnter(this.state.word);
            }
        }
        else if (e.keyCode == 46) { // the delete key code
            this.props.onDel();
        }
    }

    render() {
        const list = this.props.words.map((word, index) => {
            return (<li key={index}>{word}</li>);
        });

        return (
            <div className="word-input">
                <div className="tooltip">
                    <div className="tooltiptext">
                        Type words found and press Enter to add them to your list.  Press DEL at any time to delete the most recent entry from your list.
                    </div>
                    <input type="text" value={this.state.word} onKeyDown={(e) => this.handleKeyDown(e)} onChange={(e) => this.setState({ word: e.target.value })} placeholder="Enter found words" />
                </div> 
                <div id="wordlist">
                    <ul>{list}</ul>
                </div>
            </div>
        );
    }
}

function Square(props) {
    const sizeStyle = {
        height: props.pixelHeight + "px",
        width: props.pixelHeight + "px",
        fontSize: Math.floor(props.pixelHeight/2) + "px"
    };

    return (
        <button className="square" style={sizeStyle}>
            {props.letter}
        </button>
    );
}

function Board(props) {
    let pixelHeight = Math.floor(480 / props.height) - 2;
    const rows = []
    for (let i = 0; i < props.height; i++) {
        const squares = []
        for (let j = 0; j < props.width; j++) {
            index = i * props.width + j;
            let l = props.letters[index];
            squares.push(<Square letter={l} key={index} pixelHeight={pixelHeight} />)
        }
        rows.push(<div className="board-row" key={i}>{squares}</div>)
    }
    return (<div className="game-board">{rows}</div>)
}

class Game extends React.Component {    
    render() {
        const height = this.props.height;
        const width = this.props.width;
        const letters = this.props.letters;
        const words = this.props.words;

        return (
            <div className="game">
                <Board
                        height={height}
                        width={width}
                        letters={letters}
                />
                <WordInput words={words} onEnter={(w) => this.props.addWord(w)} onDel={() => this.props.removeWord()} />
            </div>
        );
    }
}

class ControlPanel extends React.Component {
    constructor(props) {
        super(props);
        this.state = { message: "" };
    }

    handleKeyDownMessage(e) {
        if (e.keyCode == 13) { // the enter key code   
            if (this.state.message !== "") {
                this.setState({ message: "" });            
                this.props.onEnterMessage(this.state.message);
            }
        }
    }

    updateMessage(e) {
        this.setState({ message: e.target.value });
    }

    render() {
        const info = (<div className="status">
            <div><b>Currently connected to game: {this.props.gid}</b></div>
            <div><i>Language</i>: {(this.props.language) ? this.props.language.toUpperCase() : null}</div>
            <div><i>Minimum Letters</i>: {this.props.minLetters}</div>
        </div>);        
        const messages = this.props.messages.map((m, index) => {
            return (<div className="message" key={index}>
                        [{m.timestamp}] <b>{m.sender}</b>  : {m.content}
                    </div>
                    );
        });

        return (
            <div className="control">
                <div className="panel">
                    {info}
                    <button className="other-button" onClick={() => this.props.onRotateClicked()}>ROTATE BOARD</button>
                    <div className="timer">{this.props.roundTimeRemaining}</div>                                     
                </div>
                <div className="chat">
                    <input type="text" value={this.state.message} onKeyDown={(e) => this.handleKeyDownMessage(e)} onChange={(e) => this.updateMessage(e)} placeholder="Enter chat message here" style={{ width: "99.5%" }} />
                    <div className="messages">
                        {messages}
                    </div>
                </div>                
            </div>
        );
    }
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: null,
            gid: props.gid,
            gameState: null,
            height: 5,
            width: 5,
            letters: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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
            this.setState({
                height: game.grid.length,
                width: game.grid[0].length,
                letters: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', 'A', 'A'],
            });
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

    // TODO: Implement start and end round

    sendMessage(msg) {
        this.state.socket.emit('chat_message', { 
            gid: this.state.gid, 
            username: this.state.username, 
            message: msg
        });
    }

    rotateBoard() {
        const width = this.state.width;
        const height = this.state.height;
        const oldLetters = this.state.letters;

        let newLetters = [];
        for (let col = width - 1; col >= 0; col--) {
            newLetters.push([]);
            for (let row = 0; row < height; row++) {
                newLetters[width - 1 - col].push(oldLetters[row][col]);
            }
        }
        this.setState({ height: width, width: height, letters: newLetters });
    }

    // TODO: implement letter shortcuts?
    flipBoardHorizontal() {
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
        this.rotateBoard()
        this.flipBoardHorizontal()
        this.rotateBoard()
        this.rotateBoard()
        this.rotateBoard()
    }

    timeRemaining() {
        return "0:00"
    }

    render() {
        if (this.state.gameState === null) {
            return (
                <div>
                    <Login
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
                    height={this.state.height} 
                    width={this.state.width} 
                    letters={this.state.letters} 
                    words={this.state.words}
                    addWord={(w) => this.addWord(w)} 
                    removeWord={() => this.removeWord()}    
                />
                <ControlPanel 
                    gid={this.state.gid}
                    minLetters={this.state.minimumLetters}
                    language={this.state.language}
                    messages={this.state.messages}
                    roundTimeRemaining={this.timeRemaining()}                   
                    onEnterMessage={(msg) => this.sendMessage(msg)}
                    onRotateClicked = {() => this.rotateBoard()}
                    onFlipHorizontalClicked = {() => this.flipBoardHorizontal()}
                    onFlipVerticalClicked = {() => this.flipBoardVertical()}
                />
            </div>
        )
    }
}


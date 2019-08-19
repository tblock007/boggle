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

    updateValue(e) {
        this.setState({ word: e.target.value });
    }

    render() {
        const list = this.props.words.map((word, index) => {
            return (<li key={index}>{word}</li>);
        });

        return (
            <div>
                <input type="text" value={this.state.word} onKeyDown={(e) => this.handleKeyDown(e)} onChange={(e) => this.updateValue(e)} placeholder="Enter found words" />
                <div id="wordlist">
                    <ul>{list}</ul>
                </div>
            </div>
        );
    }
}


function Square(props) {

    return (
        <button className="square">
            {props.letter}
        </button>
    );
}


function Board(props) {

    const rows = []
    for (let i = 0; i < props.height; i++) {
        const squares = []
        for (let j = 0; j < props.width; j++) {
            index = i * props.width + j;
            let l = props.letters[index];
            squares.push(<Square letter={l} key={index} />)
        }
        rows.push(<div className="board-row" key={i}>{squares}</div>)
    }

    return (<div>{rows}</div>)
}


class Game extends React.Component {
    
    render() {

        const height = this.props.height;
        const width = this.props.width;
        const letters = this.props.letters;
        const words = this.props.words;

        return (
            <div className="game">
                <div className="game-board">
                    <Board
                        height={height}
                        width={width}
                        letters={letters}
                    />
                </div>
                <div className="word-input">
                    <WordInput words={words} onEnter={(w) => this.props.addWord(w)} onDel={() => this.props.removeWord()} />
                </div>
            </div>

        );
    }
}







class ControlPanel extends React.Component {

    constructor(props) {
        super(props);
        this.state = { username: "", command: "", message: "" };
    }

    handleKeyDownCommand(e) {
        if (e.keyCode == 13) { // the enter key code
            if (this.state.command !== "") {
                this.setState({ command: "" });
                this.props.onEnterCommand(this.state.command);
            }
        }
    }

    handleKeyDownMessage(e) {
        if (e.keyCode == 13) { // the enter key code   
            if (this.state.message !== "") {
                this.setState({ message: "" });            
                this.props.onEnterMessage(this.state.message);
            }
        }
    }

    updateUsername(e) {
        this.setState({ username: e.target.value });
        this.props.onEnterUsername(e.target.value);
    }

    updateCommand(e) {
        this.setState({ command: e.target.value });
    }

    updateMessage(e) {
        this.setState({ message: e.target.value });
    }

    render() {
        const status = (this.props.gid === null) ? "Not connected to a game" : "Currently connected to game: " + this.props.gid;
        const messages = this.props.messages.map((m, index) => {
            return (<div className="message" key={index}>
                        [{m.timestamp}] <b>{m.sender}</b>  : {m.content}
                    </div>
                    );
        })
        return (
            <div>
                <div className="control">
                    {status}
                    <input type="text" value={this.state.username} onChange={(e) => this.updateUsername(e)} placeholder="Enter username" style={{ width: "99.5%" }} />
                    <input type="text" value={this.state.command} onKeyDown={(e) => this.handleKeyDownCommand(e)} onChange={(e) => this.updateCommand(e)} placeholder="Enter command here" style={{ width: "99.5%" }} />
                  
                </div>
                <div className="chat">
                    <input type="text" value={this.state.message} onKeyDown={(e) => this.handleKeyDownMessage(e)} onChange={(e) => this.updateMessage(e)} placeholder="Enter chat message here" style={{ width: "99.5%" }} />
                    <div className="messages">
                        {messages}
                    </div>
                </div>
                Command format:<br />
                CREATE GID HEIGHT WIDTH MINLETTERS INCLUDEDOUBLE LANGUAGE<br />
                JOIN GID<br />
                NEWROUND<br />
                SOLVE<br />
                END<br />
                e.g., CREATE game5293 5 5 4 Yes English
            </div>
        );
    }
}

class ModalStore extends React.Component {

    handleClick() {
        this.props.onClick(this.props.content);
    }

    render() {
        return (
            <button type="button" onClick={() => this.handleClick()}>{this.props.type}</button>
        );
    }
}


class Modal extends React.Component {

    render() {
        if (this.props.content === null) {
            return null;
        }

        let content = null;
        if (this.props.content.hasOwnProperty("wordlist")) {
            const wl = this.props.content.wordlist;
            const listcontent = wl.map((word, index) => {
                return (<li key={index}>{word}</li>);
            });
            content = (<ul>{listcontent}</ul>);
        }
        else if (this.props.content.hasOwnProperty("results")) {
            const results = this.props.content.results;

            let playerResults = [];
            for (let player in results) {
                if (results.hasOwnProperty(player)) {

                    let playerlistInvalid = results[player].invalid.map((word, index) => {
                        return (<li key={"in" + index.toString()}><s>{word} ???</s></li>);
                    });

                    let playerlistStruck = results[player].struck.map((word, index) => {
                        return (<li key={"st" + index.toString()}><s>{word}</s></li>);
                    });

                    let playerlistScored = results[player].scored.map((word, index) => {
                        return (<li key={"sc" + index.toString()}><div className="wordscore">{results[player].scores[index]}</div> {word}</li>);
                    });

                    playerResults.push(
                        <div className="playerscoreboard">
                            {player}:<br />
                            Score: {results[player].totalScore}<br />
                            <ul>{playerlistInvalid.concat(playerlistStruck, playerlistScored)}</ul>
                        </div>
                    );
                }
            }

            content = playerResults;
        }


        return (
            <div className="modal-backdrop" onClick={() => this.props.onModalClicked()}>
                <div className="modal-content">
                    {content}
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
            gid: null,
            height: null,
            width: null,
            letters: [],
            words: [],
            messages: [],
            socket: null,

            modalMessage: null,
            lastScoreboard: null,
            lastSolvedList: null
        };
    }

    componentDidMount() {
        this.state.socket = io.connect("http://" + document.domain + ":" + location.port);
        this.state.socket.on("user_join_response", () => this.log("Server", "Welcome to the Boggle server! Please ensure you set your username."));
        this.state.socket.on("game_creation_response", msg => this.handleGameCreationResponse(JSON.parse(msg)));
        this.state.socket.on("game_join_response", msg => this.handleGameJoinResponse(JSON.parse(msg)));      
        this.state.socket.on("new_board", msg => this.updateBoard(JSON.parse(msg)));
        this.state.socket.on("game_result", (result) => {
            this.setState({ lastScoreboard: result });
            this.showModal(result);
        });
        this.state.socket.on("game_solution", (list) => {
            this.setState({ lastSolvedList: list });
            this.showModal(list);
        });
        this.state.socket.on("incoming_message", resp => { 
            this.log(resp.username, resp.message); 
            $('.messages').scrollTop($('.messages')[0].scrollHeight + 300);
        });
        this.state.socket.on("list_request", () => { 
            this.state.socket.emit("list_submit", {
                username: this.state.username,
                gid: this.state.gid,
                list: this.state.words
            });
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

    handleGameCreationResponse(resp) {
        if (resp.response == "OK") {
            this.updateBoard(resp);
            this.log("Server", "Successfully joined game " + resp.gid);
        }
        else if (resp.response == "NOTUNIQUE") {
            this.log("Server", "Game already exists.");
        }
        else if (resp.response == "TOOMANY") {
            this.log("Server", "Game limit reached.  Please wait before attempting to create a game.");
        }
    }

    handleGameJoinResponse(resp) {
        if (resp.response == "OK") {
            this.updateBoard(resp);
            this.log("Server", "Successfully joined game " + resp.gid);
        }
        else if (resp.response == "DOESNOTEXIST") {
            this.log("Server", "Could not find requested game. Please ensure someone creates the game before trying to join.");
        }
        else if (resp.response == "ALREADYJOINED") {
            this.log("Server", "You have already joined this game.");
        }
    }

    updateBoard(resp) {
        this.setState({ 
            gid: resp.gid, 
            height: resp.height, 
            width: resp.width, 
            letters: resp.grid, 
            words: [], 
            modalMessage: null,
            lastScoreboard: null,
            lastSolvedList: null
        });
    }

    addWord(w) {
        this.setState({ words: [w.toUpperCase()].concat(this.state.words)});
    }

    removeWord() {
        this.setState({ words: this.state.words.slice(1)});
    }

    sendCommand(cmd) {
        // TODO: implement a better way of issuing these commands
        let tokens = cmd.split(" ");
        if (tokens[0].toLowerCase() === "create") {
            const gid = tokens[1];
            const height = parseInt(tokens[2], 10);
            const width = parseInt(tokens[3], 10);
            const minLetters = parseInt(tokens[4], 10);
            const includeDoubleLetterCube = (tokens[5].toLowerCase() === "yes");
            const language = tokens[6];

            this.state.socket.emit('game_creation', {
                gid: gid,
                old_gid: this.state.gid,
                height: height,
                width: width,
                minimumLetters: minLetters,
                includeDoubleLetterCube: includeDoubleLetterCube,
                language: language
            });
        }
        else if (tokens[0].toLowerCase() === "join") {
            const gid = tokens[1];

            this.state.socket.emit('game_join', {
                gid: gid,
                old_gid: this.state.gid
            });
        }
        else if (tokens[0].toLowerCase() === "newround") {
            this.state.socket.emit('board_gen', {
                gid: this.state.gid
            });
        }
        else if (tokens[0].toLowerCase() === "solve") {
            this.state.socket.emit('solve_game', {
                gid: this.state.gid
            });
        }
        else if (tokens[0].toLowerCase() === "end") {
            this.state.socket.emit('end_game', {
                gid: this.state.gid
            });
        }
        else {
            this.log("ERROR", "Unrecognized command");
        }
    }

    sendMessage(msg) {
        this.state.socket.emit('new_message', { 
            gid: this.state.gid, 
            username: this.state.username, 
            message: msg
        });
    }

    showModal(content) {
        this.setState({ modalMessage: content });
    }

    render() {
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
                    messages={this.state.messages}
                    onEnterUsername={(usr) => this.setState({ username: usr })}
                    onEnterCommand={(cmd) => this.sendCommand(cmd)}
                    onEnterMessage={(msg) => this.sendMessage(msg)}
                />
                <ModalStore type="Scoreboard" onClick={(c) => this.showModal(c)} content={this.state.lastScoreboard} />
                <ModalStore type="Solved List" onClick={(c) => this.showModal(c)} content={this.state.lastSolvedList} />
                <Modal content={this.state.modalMessage} onModalClicked={() => this.setState({ modalMessage: null })} />
            </div>
        )
    }
}

ReactDOM.render(
    <App />,
    document.getElementById("root")
);

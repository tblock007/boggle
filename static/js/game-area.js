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


class WordInput extends React.Component {

    handleKeyDown(e) {
        if (e.keyCode == 13) { // the enter key code    
            let w = $('#writeword').val().toUpperCase();
            if (w !== '') {
                $('#writeword').val('')            
                this.props.onEnter(w);
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
            <div>
                <input type="text" id="writeword" onKeyDown={(e) => this.handleKeyDown(e)} placeholder="Found Word" />
                <div id="wordlist">
                    <ul>{list}</ul>
                </div>
            </div>
        );
    }
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

    handleKeyDown(e) {
        if (e.keyCode == 13) { // the enter key code    
            let msg = $('#writemessage').val();
            if (msg !== '') {
                $('#writemessage').val('')            
                this.props.onEnter(msg);
            }
        }
    }

    render() {
        const status = (this.props.gid === null) ? "Not connected to a game" : "Currently connected to game " + this.props.gid;
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
                </div>
                <div className="chat">
                    <input type="text" id="writemessage" onKeyDown={(e) => this.handleKeyDown(e)} placeholder="Send message" style={{ width: "99.5%" }} />
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
            username: "null",
            gid: null,
            height: null,
            width: null,
            letters: [],
            words: [],
            messages: [],
            socket: null
        };
    }

    componentDidMount() {
        this.state.socket = io.connect("http://" + document.domain + ":" + location.port);
        this.state.socket.on("game_join_response", msg => this.handleGameJoinResponse(JSON.parse(msg)));      
        this.state.socket.on("new_board", msg => this.updateBoard(JSON.parse(msg)));
        this.state.socket.on("incoming_message", resp => { 
            this.log(resp.username, resp.message); 
            $('.messages').scrollTop($('.messages')[0].scrollHeight + 300);
        });


        // temporary auto join until join functionality is implemented
        this.state.socket.emit("game_join", {
            old_gid: "0",
            gid: "123"
        })
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
        this.setState({ gid: resp.gid, height: resp.height, width: resp.width, letters: resp.grid, words: []});
    }

    addWord(w) {
        this.setState({ words: [w].concat(this.state.words)});
    }

    removeWord() {
        this.setState({ words: this.state.words.slice(1)});
    }

    sendMessage(msg) {
        this.state.socket.emit('new_message', { 
            gid: this.state.gid, 
            username: this.state.username, 
            message: msg
        });
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
                    onEnter={(msg) => this.sendMessage(msg)}
                />
            </div>
        )
    }
}

ReactDOM.render(
    <App />,
    document.getElementById("root")
);

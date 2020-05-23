class WordInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = { word: "" };
    }

    handleKeyDown(e) {
        if (e.keyCode == 13) { // the enter key code
            if (this.state.word === "R" || this.state.word === "r") {
                this.setState({ word: "" });
                this.props.onR();
            }
            else if (this.state.word === "H" || this.state.word === "h") {
                this.setState({ word: "" });
                this.props.onH();
            }  
            else if (this.state.word === "V" || this.state.word === "v") {
                this.setState({ word: "" });
                this.props.onV();
            }
            else {
                if (this.state.word.length >= this.props.minLetters) {
                    this.props.onEnter(this.state.word);
                }
                this.setState({ word: "" });
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
                <input type="text" value={this.state.word} onKeyDown={(e) => this.handleKeyDown(e)} onChange={(e) => this.setState({ word: e.target.value })} placeholder="Enter found words" />
                <div id="wordlist">
                    <ul>{list}</ul>
                </div>
            </div>
        );
    }
}

class Scoreboard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.scoreboard === null) {
            return (
                <div className="game-panel-content-null">
                    Game results will be shown here at the end of the round.
                </div>

            );
        }
        else {
            const results = this.props.scoreboard;
            let playerResults = [];
            for (let player in results) {
                if (results.hasOwnProperty(player)) {
                    let playerlistInvalid = results[player].invalid.map((word, index) => {
                        return (<li key={"in" + index.toString()} className="definable" onClick={() => this.props.requestDefinition(word)}><s>{word} ?</s></li>);
                    });
                    let playerlistStruck = results[player].struck.map((word, index) => {
                        return (<li key={"st" + index.toString()} className="definable" onClick={() => this.props.requestDefinition(word)}><s>{word}</s></li>);
                    });
                    let playerlistScored = results[player].scored.map((word, index) => {
                        return (<li key={"sc" + index.toString()} className="definable" onClick={() => this.props.requestDefinition(word)}><div className="wordscore">{results[player].scores[index]}</div> {word}</li>);
                    });
                    let sum = results[player].scores.reduce((a, b) => a + b, 0)

                    let title = "";
                    if (player === this.props.mostStruck) {
                        title = title + " Bullied";
                    }
                    if (player === this.props.longestWord) {
                        title = title + " Phenomenal";
                    }
                    if (player === this.props.mostInvalid) {
                        title = title + " Goober";
                    }
                    if (title !== "") {
                        title = " the" + title;
                    }

                    playerResults.push(
                        <div className="player-scoreboard" key={player}>
                            {player + title}<br />
                            Score: {sum}
                            <ul>{playerlistScored.concat(playerlistStruck, playerlistInvalid)}</ul>
                        </div>
                    );
                }
            }
            
            return (
                <div className="scoreboard">
                    {playerResults}
                </div>
            );
        }
    }
}

class Solution extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.solution === null) {
            return (
                <div className="game-panel-content-null">
                    Board solution will be shown here at the end of the round.
                </div>

            );
        }
        else {
            const list = this.props.solution.map((word, index) => {
                return (<li key={index} className="definable" onClick={() => this.props.requestDefinition(word)}>{word.toUpperCase()}</li>);
            });
            return (
                <div className="solution">
                    <ul>
                        {list}
                    </ul>
                </div>
            );
        }
    }
}

class GamePanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let wordInputTab = (<button className="selectable-header" onClick={() => { this.props.setGamePanelMode("word-input"); }}>Word Input</button>);
        let scoreboardTab = (<button className="selectable-header" onClick={() => {this.props.setGamePanelMode("scoreboard"); }}>Scoreboard</button>);
        let solutionTab = (<button className="selectable-header" onClick={() => { this.props.setGamePanelMode("solution");  }}>Solution</button>);
        if (this.props.gamePanelMode === "word-input") {
            var content = (<WordInput 
                            minLetters = {this.props.minLetters}
                            words = {this.props.words} 
                            onEnter = {this.props.onEnter} 
                            onDel = {this.props.onDel}
                            onR = {this.props.onR}
                            onH = {this.props.onH}
                            onV = {this.props.onV} 
                        />);
            wordInputTab = (<button className="selected-header">Word Input</button>);
        }
        else if (this.props.gamePanelMode === "scoreboard") {
            var content = (<Scoreboard scoreboard = {this.props.scoreboard} mostInvalid = {this.props.mostInvalid} mostStruck = {this.props.mostStruck} longestWord = {this.props.longestWord} requestDefinition = {this.props.requestDefinition} />);
            scoreboardTab = (<button className="selected-header">Scoreboard</button>);
        }
        else if (this.props.gamePanelMode === "solution") {
            var content = (<Solution solution = {this.props.solution} requestDefinition = {this.props.requestDefinition} />);
            solutionTab = (<button className="selected-header">Solution</button>);
        }
        return (
            <div className="game-panel">
                {wordInputTab}
                {scoreboardTab}
                {solutionTab}
                <div className="game-panel-content">
                    {content}    
                </div>
            </div>
        )
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
    const height = props.letters.length;
    const width = props.letters[0].length;
    let pixelHeight = Math.floor(480 / height) - 2;
    const rows = []
    for (let i = 0; i < height; i++) {
        const squares = []
        for (let j = 0; j < width; j++) {
            index = i * width + j;
            let l = props.letters[i][j];
            squares.push(<Square letter={l} key={index} pixelHeight={pixelHeight} />)
        }
        rows.push(<div className="board-row" key={i}>{squares}</div>)
    }
    return (<div className="game-board">{rows}</div>)
}

class Game extends React.Component {    
    render() {
        return (
            <div className="game">
                <Board className="board" letters={this.props.letters} />
                <GamePanel 
                    minLetters = {this.props.minLetters}
                    words = {this.props.words} 
                    onEnter = {this.props.addWord} 
                    onDel = {this.props.removeWord}
                    onR = {this.props.rotate}
                    onH = {this.props.flipH}
                    onV = {this.props.flipV} 
                    scoreboard = {this.props.scoreboard}
                    solution = {this.props.solution}
                    mostInvalid = {this.props.mostInvalid}
                    mostStruck = {this.props.mostStruck}
                    longestWord = {this.props.longestWord}
                    gamePanelMode = {this.props.gamePanelMode}
                    setGamePanelMode = {this.props.setGamePanelMode} 
                    requestDefinition = {this.props.requestDefinition}                  
                />
            </div>
        );
    }
}

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
            else if (this.state.word !== "") {
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
        return (
            <div className="scoreboard">
                {this.props.scoreboard}
            </div>
        );
    }
}

class Solution extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="solution">
                {this.props.solution}
            </div>
        );
    }
}

class GamePanel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {mode: "word-input" };
    }

    render() {
        let wordInputTab = (<button className="selectable-header" onClick={() => { this.setState({ mode: "word-input" });}}>Word Input</button>);
        let scoreboardTab = (<button className="selectable-header" onClick={() => { this.setState({ mode: "scoreboard" });}}>Scoreboard</button>);
        let solutionTab = (<button className="selectable-header" onClick={() => { this.setState({ mode: "solution" });}}>Solution</button>);
        if (this.state.mode === "word-input") {
            var content = (<WordInput 
                            words = {this.props.words} 
                            onEnter = {this.props.onEnter} 
                            onDel = {this.props.onDel}
                            onR = {this.props.onR}
                            onH = {this.props.onH}
                            onV = {this.props.onV} 
                        />);
            wordInputTab = (<button className="selected-header">Word Input</button>);
        }
        else if (this.state.mode === "scoreboard") {
            var content = (<Scoreboard scoreboard = {this.props.scoreboard} />);
            scoreboardTab = (<button className="selected-header">Scoreboard</button>);
        }
        else if (this.state.mode === "solution") {
            var content = (<Solution solution = {this.props.solution} />);
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
        const letters = this.props.letters;
        const words = this.props.words;

        return (
            <div className="game">
                <Board className="board" letters={letters} />
                <GamePanel 
                    words = {words} 
                    onEnter = {this.props.addWord} 
                    onDel = {this.props.removeWord}
                    onR = {this.props.rotate}
                    onH = {this.props.flipH}
                    onV = {this.props.flipV} 
                    scoreboard = "Scores for the round will be displayed when the round ends. (pass from main.jsx)"
                    solution = "Solution will be available when the round ends. (pass from main.jsx)"                    
                />
            </div>
        );
    }
}

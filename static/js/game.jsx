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
                <Board letters={letters} />
                <WordInput 
                    words = {words} 
                    onEnter = {this.props.addWord} 
                    onDel = {this.props.removeWord}
                    onR = {this.props.rotate}
                    onH = {this.props.flipH}
                    onV = {this.props.flipV} 
                />
            </div>
        );
    }
}

class CreateGameDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gid: "",
            height: 5,
            width: 5,
            language: "english",
            minutes: 4,
            minLetters: 4,
        }
    }

    send_create_request() {
        if (this.state.gid === "" || this.state.gid === "lobby") {
            alert("Invalid game name!");
            return;
        }
        const h = parseInt(this.state.height);
        const w = parseInt(this.state.width);
        const minutes = parseInt(this.state.minutes);
        const minLetters = parseInt(this.state.minLetters);

        if (isNaN(h) || isNaN(w) || isNaN(minutes) || isNaN(minLetters)) {
            alert("Please enter only positive integers for height, width, minutes, and minimum letters.");
            return;
        }

        if (h * w > 76) {
            alert("Only 76 cubes are available. Please choose a smaller board.");
            return;
        }

        const language = this.state.language.toLowerCase();
        if (language !== "english" && language !== "french") {
            alert(this.state.language + " is not a supported language.");
            return;
        }
        this.props.onCreateClicked(this.state.gid, h, w, minLetters, minutes, language);
    }

    render() {        
        return (
            <div className="create-game-dialog">
                <div className="lobby-title">Create Game</div>
                <div className="create-game-section">
                    Game Name:
                    <input 
                        type="text" value={this.state.gid} 
                        onChange={(e) => this.setState({ gid: e.target.value })}
                    />                    
                </div>
                <div className="create-game-section">
                    Board Size:
                    <input 
                        type="text" value={this.state.height} 
                        onChange={(e) => this.setState({ height: e.target.value })} 
                        placeholder="5" 
                    />
                    <div className="centered">x</div>
                    <input 
                        type="text" value={this.state.width} 
                        onChange={(e) => this.setState({ width: e.target.value })} 
                        placeholder="5" 
                    />
                </div>
                <div className="create-game-section">
                    Language:
                    <input 
                        type="text" value={this.state.language} 
                        onChange={(e) => this.setState({ language: e.target.value })} 
                        placeholder="English" 
                    />
                </div>
                <div className="create-game-section">
                    Minutes:
                    <input 
                        type="text" value={this.state.minutes} 
                        onChange={(e) => this.setState({ minutes: e.target.value })} 
                        placeholder="4" 
                    />
                </div>
                <div className="create-game-section">
                    Minimum Letters:
                    <input 
                        type="text" value={this.state.minLetters} 
                        onChange={(e) => this.setState({ minLetters: e.target.value })} 
                        placeholder="4" 
                    />
                </div>
                <button className="other-button" onClick={() => this.send_create_request()}>Create!</button>
            </div>
        );
    }
}

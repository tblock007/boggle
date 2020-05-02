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

    renderPlayerList() {
        let player_list = [];
        for (const [player, score] of Object.entries(this.props.playerScores)) {
            player_list.push(<li key={player}>({score}) {player}</li>);
        }
        return (<ul>{player_list}</ul>);
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

        const player_list = this.renderPlayerList();

        return (
            <div className="control">
                <div className="panel">
                    {info}
                    <button className="other-button" onClick={() => this.props.onStartClicked()}>START ROUND</button>
                    <button className="other-button" onClick={() => this.props.onRotateClicked()}>ROTATE</button>
                    <button className="other-button" onClick={() => this.props.onFlipHorizontalClicked()}>FLIP HORIZONTAL</button>
                    <button className="other-button" onClick={() => this.props.onFlipVerticalClicked()}>FLIP VERTICAL</button>
                    <div className="timer">{this.props.roundTimeRemaining}</div>                                     
                </div>
                <div className="player-list">
                    {player_list}
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

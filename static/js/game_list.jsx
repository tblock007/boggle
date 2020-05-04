class GameListItem extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let state = null;
        if (this.props.state === "ROUND_IN_PROGRESS") {
            state = "Round in progress";
        }
        return (            
            <div className = "game-list-item" onClick = {() => this.props.onGameClicked(this.props.gid)}>
                <div className = "game-name">{this.props.gid}</div>
                <div className = "game-state">{state}</div>
                <div className = "game-properties">[{this.props.language.toUpperCase()}] [{this.props.height} x {this.props.width}] [{this.props.minLetters}+ letters] [{this.props.minutes} min.]</div>
                Players: 
                <div className = "game-players">
                    &nbsp;&nbsp;{Object.keys(this.props.playerScores).join(",")}
                </div>
            </div>
        );
    }
}

class GameList extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {      
        let game_list = [];
        if (this.props.games != null) {
            for (const [gid, game] of Object.entries(this.props.games)) {
                game_list.push(<GameListItem 
                                    key = {gid}
                                    gid = {gid}
                                    state = {game.state}
                                    height = {game.height}
                                    width = {game.width}
                                    minLetters = {game.min_letters}
                                    minutes = {game.minutes}
                                    language = {game.language}
                                    playerScores = {game.player_scores}
                                    onGameClicked = {this.props.onGameClicked}
                                />);
            }
        }

        return (
            <div className="game-list">
                <div className="lobby-title">Game List</div>
                {game_list}
            </div>
        );
    }
}

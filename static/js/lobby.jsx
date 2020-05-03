class Lobby extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            games: null
        };
    }

    componentDidMount() {
        this.state.socket = io.connect("http://" + document.domain + ":" + location.port);
        this.state.socket.emit("lobby_join");
        this.state.socket.on("game_list_update", (resp) => {
            this.setState({ games: resp });
        });
    }

    leaveLobby(gameName) {
        this.state.socket.emit("lobby_leave");
        // Redirect to game after 0.2s to allow lobby_leave message to send.
        setTimeout(() => { window.location = "/game/" + gameName; }, 200);
    }

    render() {        
        return (
            <div className="lobby">
                <GameList 
                    games = {this.state.games}
                    onGameClicked = {(gameName) => this.leaveLobby(gameName)}    
                />
                <CreateGameDialog />
            </div>
        );
    }
}

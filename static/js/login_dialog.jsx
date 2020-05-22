class LoginDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = { username: "" };
    }

    backToLobby() {
        window.location = "/lobby";
    }

    render() {        
        return (
            <div className="login-dialog">
                <input 
                    type="text" value={this.state.username} 
                    onChange={(e) => this.setState({ username: e.target.value })} 
                    placeholder="Enter username" 
                />
                <button className="other-button" onClick={() => this.props.setUsername(this.state.username)}>{"Join " + this.props.gid}</button>
                <button className="other-button" onClick={this.backToLobby}>Back to Lobby</button>
            </div>
        );
    }
}

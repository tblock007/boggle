class LoginDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = { username: "" };
    }

    render() {        
        return (
            <div className="login-dialog">
                <input 
                    type="text" value={this.state.username} 
                    onChange={(e) => this.setState({ username: e.target.value })} 
                    placeholder="Enter username" 
                />
                <button className="other-button" onClick={() => this.props.setUsername(this.state.username)}>JOIN!</button>
            </div>
        );
    }
}

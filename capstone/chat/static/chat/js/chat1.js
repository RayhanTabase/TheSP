
const HOST = "http://127.0.0.1:8000"


class Chat extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            open_chat:false,
            messages:[]
        }  
    }
    
    render(){
        var display_chat = "none"
        var display_chat_button = "block"
        if(this.state.open_chat){
            var display_chat = "block"
            var display_chat_button = "none"
        }
        var chat_messages = this.prev_messages()
        return(
            <div>
                 <div style={{display:`${display_chat}`}}>
                    <button name="close_chat" onClick={this.handleClick} className="close_chatbox">Close</button>
                     <div id="chat_messages" >
                         {chat_messages}
                    </div><br/>

                    <textarea id="input_chat_message"></textarea><br/>
                     <input className="btn btn-primary" id="send_chat" type="submit" value="send"></input>
                </div>

                 <button className="btn btn-primary btn-lg open_chat_button" name="open_chat" onClick={this.handleClick} style={{display:`${display_chat_button}`}}>
                    CHAT
                </button>
            </div>
        )
    }

    handleClick=(event)=>{
        if(event.target.name === "open_chat"){
            this.setState({
                open_chat:true
            })
        }
        else if(event.target.name === "close_chat"){
            this.setState({
                open_chat:false
            })
        }
    }
    componentDidUpdate(prevState) {
        // // If chatting prop was changed and value was true load chatroom
        // if (prevState.open_chat !== this.state.open_chat && this.state.open_chat) { 
        //     // this.get_messages();
        //     this.setup_websockets();
        // }
        this.updateScroll()
    }
    
    componentDidMount=()=>{
        this.setup_websockets();
        this.get_messages();
    }

    get_messages=()=>{
        const room_name = `chat_${business_id}_${username}`
        fetch(`${HOST}/chat/get_messages/${room_name}/`)
        .then(response=>{
            if(response.status === 200){
                return response.json()
            }
        })
        .then(response=>{
            if(response){
                this.setState({
                    messages:response
                })
            }
        })
    }

    updateScroll=()=>{
        var element = document.getElementById("chat_messages");
        element.scrollTop = element.scrollHeight;
    }

    prev_messages=()=>{
        var messages = this.state.messages.map(message=>{
            var alignment = "left"
            if(message.customer_created){
                alignment = "right"
            }
            const give_class = `chat_message-${alignment}` 
            return(
                <p key={message.id} className ={give_class} >
                    <span>
                        {message.message}
                    </span>
                </p>
            )
            
        })
        return messages
    }

    setup_websockets=()=>{
        // Create websocket
        const chatSocket = new WebSocket(
            'ws://' +
            window.location.host +
            '/ws/chat/' +
            business_id +
            '/' +
            username +
            '/'
        );

        // Listen for messages
        chatSocket.onmessage = function(e){
            const data = JSON.parse(e.data);
            // console.log(data)
            if(data.message){
                let chatbox = document.querySelector('#chat_messages')
                var alignment = "left"

                if(data.customer_created){
                    alignment = "right"
                }

                var chat_message = document.createElement("p")
                chat_message.className = `chat_message-${alignment}`
                var span = document.createElement("span")
                span.innerHTML = data.message
                chat_message.appendChild(span);
                chatbox.appendChild(chat_message);

                var element = document.getElementById("chat_messages");
                element.scrollTop = element.scrollHeight;
            }  
        }

        // Handles sending messages to chat
        document.querySelector('#send_chat').addEventListener('click', function(){
            // console.log("send message")
            var message = document.querySelector("#input_chat_message").value;
            if(message.trim()){
                chatSocket.send(JSON.stringify({
                    'message':message,
                    'customer_created':true
                }));
                document.querySelector("#input_chat_message").value = "";
            }
        })
    }
}



ReactDOM.render(<Chat />,document.querySelector('#chatbox')); 
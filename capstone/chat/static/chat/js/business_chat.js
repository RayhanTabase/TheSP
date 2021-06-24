function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 

const HOST = "http://127.0.0.1:8000"

class ChatManagement extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            rooms:[],
            chatting:null
        }  
    }
    
    render(){
        let chat_rooms = this.create_chat_rooms()
        return(
            <div>
                <div className="chat_groups" style={{border:"1px solid black"}}>
                    {chat_rooms}
                </div>    
            </div>              
        )
    }

    componentDidMount=()=>{
        this.get_rooms()
    }

    change_chatting=(room_name)=>{
        var change_to = room_name
        if(!room_name){
            change_to = null
        }
        this.setState({
            chatting:change_to
        })
    }
    
    // Get all rooms created by customers
    get_rooms=()=>{
        fetch(`${HOST}/chat/get_rooms/${business_id}/`)
        .then(response=>{
            return response.json()
        })
        .then(response=>{
            if(response){
                this.setState({
                    rooms:response
                })
            }
        })
    }

    create_chat_rooms=()=>{
        var chat_rooms = this.state.rooms.map(room =>{
            var chatting = false
            if(this.state.chatting == room.room_name){
                chatting = true
            }
            return (
                <CreateRoom
                key ={room.room_name}
                room_name = {room.room_name}
                customer = {room.customer}
                chatting = {chatting}
                change_chatting = {this.change_chatting}
                />
            )
        })
        return chat_rooms
    }
}

class CreateRoom extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            messages:[]     
        }  
    }
    
    render(){
        var chat_messages = this.prev_messages()
        return(
            <div id={this.props.room_name} style={{border:"2px dotted green"}}>
                { this.props.chatting ?
                    <div>
                        <h2>{this.props.customer}</h2>
                        <button name="close_chat" onClick={()=>this.props.change_chatting(null)}>Close</button>
                        <div id="chat_messages" >
                            {chat_messages}
                        </div><br/>

                        <textarea id="input_chat_message"></textarea><br/>
                        <input className="btn btn-primary" id="send_chat" type="submit" value="send"></input>
                    </div>
                    :
                    <h2 onClick={()=>this.props.change_chatting(this.props.room_name)}> {this.props.customer}</h2>
                } 
            </div>            
        )
    }

    componentDidUpdate(prevProps) {
        // If chatting prop was changed and value was true load chatroom
        if (prevProps.chatting !== this.props.chatting && this.props.chatting) { 
            console.log("updating component")
            this.get_messages();
            this.setup_websockets();
        }
    }

    get_messages=()=>{
        fetch(`${HOST}/chat/get_messages/${this.props.room_name}/`)
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

    prev_messages=()=>{
        var messages = this.state.messages.map(message=>{
            var alignment = "right"
            if(message.customer_created){
                alignment = "left"
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

    updateScroll=()=>{ 
        console.log("set scroll to bottom")
        const section = document.querySelector(`#${this.props.room_name}`)
        var element = section.querySelector("#chat_messages");
        element.scrollTop = element.scrollHeight;
    }

    componentWillUnmount() {
        // fix Warning: Can't perform a React state update on an unmounted component
        this.setState = (state,callback)=>{
            return;
        };
    }
  
    setup_websockets=()=>{
        const section = document.querySelector(`#${this.props.room_name}`)
        // Create websocket
        const chatSocket = new WebSocket(
            `ws://${window.location.host}/ws/chat/admin/${employee_id}/${business_id}/${this.props.room_name}/` 
        );

        // Listen for messages
        chatSocket.onmessage = function(e){
            const data = JSON.parse(e.data);
            console.log(data)
            if(data.message){
                let chatbox = section.querySelector('#chat_messages')
                var alignment = "right"

                if(data.customer_created){
                    alignment = "left"
                }

                var chat_message = document.createElement("p")
                chat_message.className = `chat_message-${alignment}`
                var span = document.createElement("span")
                span.innerHTML = data.message
                chat_message.appendChild(span);
                chatbox.appendChild(chat_message);

                var element = section.querySelector("#chat_messages");
                element.scrollTop = element.scrollHeight;
            }   
        }

        // Handles sending messages to chat
        section.querySelector('#send_chat').addEventListener('click', function(){
            // console.log("send message")
            var message = section.querySelector("#input_chat_message").value;

            if(message.trim()){
                chatSocket.send(JSON.stringify({
                    'message':message,
                    'customer_created':false
                }));
                section.querySelector("#input_chat_message").value = "";
            }
        })
    }
}

ReactDOM.render(<ChatManagement />,document.querySelector('#body'));   
// console.log(employee_id,business_id,business_name)

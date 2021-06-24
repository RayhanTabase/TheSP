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
            chatting:null, 
            check_for_chat:true 
        }  
    }
    
    render(){
        var show_chats = this.show_chats()
        return(
            <div>
                <div className="chat_groups container-center-column">
                    {show_chats}
                </div>    
            </div>              
        )
    }

   
    componentDidMount=()=>{
        this.get_rooms()
        if(!this.state.chatting){
            console.log("a")
            this.interval = setInterval(() => this.get_rooms(), 5000);
        }
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    componentDidUpdate() {
        clearInterval(this.interval);
        if(!this.state.chatting){
            console.log("b")
            this.interval = setInterval(() => this.get_rooms(), 5000);
        }
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
                if(this.state.rooms.length === response.length){
                    console.log("dont update")
                }else{
                    this.setState({
                        rooms:response
                    })
                }
            }
        })
    }

    show_chats=()=>{
        if(this.state.chatting ){
            console.log("chat chat chat")
            var chat_room = this.state.rooms.map(room =>{
                if(this.state.chatting == room.room_name){
                    return (
                        <CreateRoom
                        key ={room.room_name}
                        room_name = {room.room_name}
                        customer = {room.customer}
                        change_chatting = {this.change_chatting}
                        />
                    )
                }
            })
            return chat_room
        }else{
            var chat_rooms = this.state.rooms.map(room =>{       
                return (
                    <div key={room.room_name} className="chat_group">
                        <button className="btn btn-block btn-default" onClick={()=>this.change_chatting(room.room_name)}> {room.customer}</button>
                    </div>
                )
            })
            return chat_rooms
        }
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
            <div id={this.props.room_name}>
                <div>
                    <h2 className="text-center">{this.props.customer}</h2>
                    <button name="close_chat" onClick={()=>this.props.change_chatting(null)}>Close</button>
                    <div id="chat_messages" >
                        {chat_messages}
                    </div><br/>

                    <textarea id="input_chat_message"></textarea><br/>
                    <input className="btn btn-primary" id="send_chat" type="submit" value="send"></input>
                </div>
            </div>            
        )
    }

    componentDidMount() { 
        this.get_messages();
        this.setup_websockets();
    }
    componentDidUpdate() {
        this.updateScroll()
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
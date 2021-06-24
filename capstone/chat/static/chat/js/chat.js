document.addEventListener('DOMContentLoaded', function() {
    // console.log(username,business_name,business_id)
    document.querySelector("#submit").addEventListener('click', function(e){
        console.log("send message")
        const messageInputDom = document.querySelector("#input");
        const message = messageInputDom.value;
        
        chatSocket.send(JSON.stringify({
            'message':message,
            'customer_created':true
        }));

        messageInputDom.value = "";
    })

    const chatSocket = new WebSocket(
        'ws://' +
        window.location.host +
        '/ws/chat/' +
        business_id +
        '/' +
        username +
        '/'
    );

    chatSocket.onmessage = function(e){
        const data = JSON.parse(e.data);
        if(data.message){
            if(data.customer_created){
                document.querySelector('#chat_text').value += `${(username)} : ${(data.message)}\n\n`
            }else{
                document.querySelector('#chat_text').value += `///${business_name} : ${(data.message)}\n\n`
            }
        }   
        else{
            console.log(data)
        }
    }
});
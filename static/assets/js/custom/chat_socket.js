const infodiv = document.getElementById("infodiv");
const chat_input = document.getElementById("chat_input");
const send_form = document.getElementById("send_msg_form");
const ul_list = document.getElementById("ul_list");
const popSound = document.getElementById("popSound");


infodiv.scrollTop = infodiv.scrollHeight; 

const domain = 'http://'+window.location.host
const urls ='ws://'+ window.location.host +"/ws"+ window.location.pathname;

let gamestate = "ON";
const ws = new ReconnectingWebSocket(urls);

const my_username = send_form.dataset.username

// ws.onopen = function (e) {
//     console.log('connection open')
// }

ws.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    if(data.command == "private_chat"){
        ul_list.innerHTML += `
        <li class="media ${data.sender.username === my_username ? 'sent' :'received'} d-flex">
        <div class="avatar flex-shrink-0">
            <img src="${domain}${data.sender.avatar}" alt="User Image" class="avatar-img  rounded-circle">
        </div>

        <div class="media-body flex-grow-1">
            <div class="msg-box">
                <div>
                    <p>${data.text}</p>
                    <ul class="chat-msg-info">
                        <li>
                            <div class="chat-time">
                                <span>${data.created_at}</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </li>
    `;
    infodiv.scrollTop = infodiv.scrollHeight;
    popSound.play()

    }
  

}

send_form.onsubmit = function(e){
    e.preventDefault()
    console.log(chat_input.value)
    if(!chat_input.value.trim()){
        toastr.error('Message cannot be blank !')
    }
    else{
        ws.send(
            JSON.stringify({
                command:"private_chat",
                message:chat_input.value
            })
        );
        send_form.reset()
    }
}
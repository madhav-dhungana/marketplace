// const urls ="ws://127.0.0.1:8000/ws/notification/";
const ws_urls = 'ws://'+ window.location.host +'/ws/notification/'
const urls = 'http://'+window.location.host
const ws = new ReconnectingWebSocket(ws_urls);


ws.onopen = function (e) {
    console.log('connection open')
}
ws.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    $("#noti_num").addClass("bg-reds")
    $("#noti_num").text(data.count)
    // $("#noti_span").prepend(`<span id="noti_num" class="noti_num">${data.count}</span>`)
    
    $("#nav_noti_content").prepend(`
        <ul class="notification-list">
        <li class="notification-message">
            <a href="${data.notification_url ?`${urls}${data.notification_url}`:''}">
                <div class="media d-flex">
                    ${data.action_by_url ?
                     `<span class="avatar avatar-sm flex-shrink-0">
                        <img class="avatar-img rounded-circle" alt="" src="${`${urls}${data.action_by_url}`}">
                    </span>`
                    :''}
                    <div class="media-body flex-grow-1">
                        <p class="noti-details"><span class="noti-title">${data.message}</span></p>
                        <p class="noti-time"><span class="notification-time">${data.time}</span></p>
                    </div>
                </div>
            </a>
        </li>
    </ul>
    `)
    toastr.success(data.message)
}
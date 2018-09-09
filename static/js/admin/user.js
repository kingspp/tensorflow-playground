/**
 * Created by prathyushsp on 16/10/16.
 */

var user_socket = '';
var user_list = [];

function get_state(state){
    if (state == "offline")
        return "text-muted";
    else if(state == "busy")
        return "text-danger";
    else if (state == "available")
        return "text-success";
}

function load_user(username){

    for(var i=0; i< user_list.length; i++){
        if (user_list[i].username == username) {
            $('#username').text(user_list[i].username);
            $('#script_content').html(user_list[i].script.replace(/(?:\r\n|\r|\n)/g, '<br />'));
            $('#user_status_big').text(user_list[i].state);
            $('#file_count').text('12');
            if (user_list[i].state == 'busy')
                $('#user_active_threads_big').text(1);
            else
                $('#user_active_threads_big').text(0);
            break;
        }
    }
}

$(document).ready(function () {
    user_socket = io.connect();
    user_socket.on('connect', function () {
        user_socket.emit('user_status', {init: 'User Connected'});
    });
    user_socket.emit('user');
    user_socket.on('user_response', function (res) {
        $('#busy_users').text(res.user_status.busy);
        $('#active_users').text(res.user_status.active);
        $('#offline_users').text(res.user_status.offline);
        $('#total_users').text(res.user_status.total);
        $('.team-members').html('');
        user_list = res.users;
        for (var i=0; i< res.users.length; i++){
            $('.team-members').append(
                '<li>'
                    +'<div class="row">'
                        +'<div class="col-xs-6">'+res.users[i].username+'<br/>'
                            +'<span class="'+get_state(res.users[i].state)+'"><small>'+res.users[i].state+'</small></span>'
                        +'</div>'
                        +'<div class="col-xs-3 text-right">'
                            +'<btn class="btn btn-sm btn-success btn-icon" onclick = "load_user(\''+res.users[i].username+'\')"><i class="fa fa-user"></i></btn>'
                        +'</div>'
                    +'</div>'
                +'</li>'
            );
        }
        setTimeout(function () {
            user_socket.emit('user');
        }, 2000);
    });

});
/**
 * Created by prathyush on 5/10/16.
 */

var tfplay_version = "BETA v0.6.5";
var editor = ace.edit("editor");
var socket = '';
var body = $('body');
var data_files_table = $("#data_files_table");
var python_files_table = $("#python_files_table");
var model_files_table = $("#model_files_table");
var data_t = data_files_table.DataTable({
    "scrollY": 200,
    "scrollX": true
});
var python_t = python_files_table.DataTable({
    "scrollY": 200,
    "scrollX": true
});
var model_t = model_files_table.DataTable({
    "scrollY": 200,
    "scrollX": true
});


var tooltip = new PNotify({
    title: "Save File",
    text: $('#save_frm').html(),
    hide: false,
    buttons: {
        closer: true,
        sticker: false
    },
    history: {
        history: false
    },
    width: PNotify.prototype.options.width,
    height: "75px",
    animate_speed: "fast",
    opacity: .9,
    icon: "fa fa-commenting",
    stack: false,
    auto_display: false
});


function notice_update() {
    alert('submit');
    tooltip.update({
        title: 'File Save',
        text: 'File saved successfully',
        icon: true,
        width: PNotify.prototype.options.width,
        hide: true,
        buttons: {
            closer: false,
            sticker: false
        },
        type: 'success',
        delay: 1000

    });
    return false;
}


function refresh_cards() {
    editor.setValue('print("Hello World. A simple DL IDE:) ")');
    $('#final_result').html('');
    $('#p_status').text(' -- ')
}

function get_files() {
    data_t.clear();
    python_t.clear();
    model_t.clear();
    HTTPUtil.GET("/get_files", function (res, err) {
        if (res === null) {
            console.log("Exception while getting the data from the server");
        } else {
            if (res.status == 500) {
                jsonData2 = "Server Error!!" + err
            } else {
                for (var i = 0; i < res.data_files.length; i++)
                    data_t.row.add(['<a href="/download/' + res.data_files[i] + '" download="' + res.data_files[i] + '" style="cursor: pointer">' + res.data_files[i] + '</a><span onclick="delete_file(\'' + res.data_files[i] + '\'); return false" style="padding-left: 8px; cursor: pointer"><i class="fa fa-trash" aria-hidden="true"></i></span>']).draw(false);
                for (i = 0; i < res.python_files.length; i++)
                    python_t.row.add(['<span onclick="load_file(\'' + res.python_files[i] + '\'); return false" style="cursor: pointer">' + res.python_files[i] + '</span><span onclick="delete_file(\'' + res.python_files[i] + '\'); return false" style="padding-left: 8px; cursor: pointer"><i class="fa fa-trash" aria-hidden="true"></i></span>']).draw(false);
                for (i = 0; i < res.model_files.length; i++)
                    model_t.row.add(['<span>' + res.model_files[i] + '</span><span onclick="delete_file(\'' + res.model_files[i] + '\'); return false" style="padding-left: 8px; cursor: pointer"><i class="fa fa-trash" aria-hidden="true"></i></span>']).draw(false);
            }
        }
    });
}


function run_thread() {
    socket.emit('event', {code: editor.getValue()});
    $('#final_result').html('');
}

function stop_thread() {
    HTTPUtil.GET('/stop', function (res, err) {
    });
}


function get_current_user() {
    HTTPUtil.GET('/current_user', function (user) {
        $('#user_name').text(user.username);
    });
}

function load_file(file_name) {
    HTTPUtil.GET('/load_file/' + file_name, function (file_data) {
        if (file_name.includes('.py'))
            editor.setValue(file_data.responseText);
    });
    var offset = 20;
    $('html, body').animate({
        scrollTop: $("#debugger").offset().top + offset
    }, 1000);
}

function delete_file(file_name) {
    HTTPUtil.GET('/delete_file/' + file_name, function () {
        new PNotify({
            title: 'Success',
            text: 'File ' + file_name + ' deleted successfully',
            type: 'success',
            delay: 1000
        });
    });
    get_files();
}

$(document).ready(function () {
    $('#result_div').perfectScrollbar();
    $('.var_tab').perfectScrollbar();
    $('#card_stack').perfectScrollbar();

    $('#save_file').on('click', function () {
        (new PNotify({
            title: 'Save File',
            text: 'Please enter the file name',
            icon: 'glyphicon glyphicon-question-sign',
            hide: false,
            confirm: {
                prompt: true
            }
        })).get().on('pnotify.confirm', function (e, notice, val) {
            if (val.length > 0) {
                if (!val.includes('.py'))
                    val = val + '.py';
                HTTPUtil.POST('/save_file', {"filename": val, "content": editor.getValue()}, function (res, err) {
                    if (res === null) {
                        console.log("Exception while getting the data from the server");
                    } else {
                        if (res.status == 500) {
                            jsonData = "Server Error!!" + err
                        } else {
                            get_files();
                            notice.cancelRemove().update({
                                title: 'Success',
                                text: 'File ' + $('<div/>').text(val).html() + ' saved successfully',
                                icon: true,
                                type: 'success',
                                hide: true,
                                buttons: {
                                    closer: true,
                                    sticker: true
                                },
                                delay: 1000
                            });

                        }
                    }
                });

            }
            else
                new PNotify({
                    title: 'Error',
                    text: 'File Name Error',
                    type: 'error',
                    delay: 1000

                });
        }).on('pnotify.cancel', function (e, notice) {
            notice.cancelRemove().update({
                title: 'Error',
                text: 'File Save Cancelled',
                icon: true,
                hide: true,
                type: 'error',
                delay: 1000
            });
        });
    });
    socket = io.connect();
    editor.setTheme("ace/theme/solarized_dark");
    editor.getSession().setMode("ace/mode/python");
    new WOW().init();

    socket.on('connect', function () {
        socket.emit('my_event', {init: 'abcd'});
    });

    socket.on('response', function (msg) {
        msg = JSON.parse(msg);
        if (msg.status == 'running') {
            $('#p_status').html(' Running');
            $('#play_button_area').html('<button type="button" title="Stop Script" id="stop_btn" onclick="stop_thread()" class="btn mybutton_red"'
                + 'style="margin-top:40px">'
                + '<i class="fa fa-stop" aria-hidden="true"></i>'
                + '</button>');
        }
        else if (msg.status == 'terminated') {
            $('#p_status').html(' Terminated');
            $('#play_button_area').html('<button type="button" title="Execute Script" id="run_btn" onclick="run_thread()" class="btn mybutton_green"'
                + 'style="margin-top:40px;">'
                + '<i class="fa fa-play" aria-hidden="true"></i>'
                + '</button>');
            get_files();
        }
        else if (msg.status == 'error')
            $('#final_result').append('<span style="color: maroon">' + msg.data.replace(/(?:\r\n|\r|\n)/g, '<br />') + '</span>');
        else if (msg.status == 'success')
            $('#final_result').append('<span style="color: darkgreen">' + msg.data.replace(/(?:\r\n|\r|\n)/g, '<br />') + '</span>');

    });


    $("#tfplay_version").html(tfplay_version);
    get_current_user();
    get_files();
    $('#reload_btn').on('click', refresh_cards);


    $('#file_upload_form').on('submit', function (e) {
        e.preventDefault();
        var fileName = $('.file-footer-caption').text();
        this.submit();
        setTimeout(function () {
            $(".fileinput-remove-button").trigger("click");
            $('.file-caption-name').html(fileName);
            get_files();
            new PNotify({
                title: 'Success',
                text: 'File ' + fileName + ' successfully uploaded',
                type: 'success',
                delay: 1000

            });
            load_file(fileName.split(" ")[0]);
        }, 1000);

    });

    $('#launch_board').on('click', function () {
        var win = '';
        if (window.location.protocol == "https:")
            win = window.open('https://tensorboard.admin.net', '_blank');
        else
             win = window.open('http://' + document.domain + ':6006');
        if (win)
            win.focus();
        else
            alert('Please allow popups for this website');
    });
});
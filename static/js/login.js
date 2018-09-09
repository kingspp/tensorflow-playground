$('.toggle').on('click', function () {
    $('.container').stop().addClass('active');
});

$('.close').on('click', function () {
    $('.container').stop().removeClass('active');
});


function calert(type, title, msg) {
        new PNotify({
            title: title,
            text: msg,
            type:type,
            delay:1000
        });
}


$(document).ready(function () {
    $('#register_form').on('submit', function (e) {
        e.preventDefault();
        if ($("#confirm_password").val() == $('#password1').val()) {
            this.submit();
        }
        else {
            new PNotify({
                title: 'Error',
                text: 'Passwords do not match',
                type: 'error',
                delay: 1000

            });
        }
    });
});
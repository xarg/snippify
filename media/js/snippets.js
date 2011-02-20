$(document).ready(function(){
    $('.source').width($('.snippet-code').width()-40);

    $('body').resize(function(){
        $('.source').width($('.snippet-code').width()-40);
    });

    $("#change-style").change(function(){
        var name = $(this).attr('name');
        var value = $(this).attr('value');
        $.get(UPDATE_FIELD_URL, {'field': name, 'value': value}, function(data){
            if (data == 'OK'){
                window.location = window.location;
            }
        });
    });
});

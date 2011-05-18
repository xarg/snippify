$(document).ready(function(){
    $('input.preview').click(function(e){
        e.preventDefault();
        var data = {
            'body': $("#id_body").val(),
            'lexer': $("#id_lexer").val(),
        }
        $.post(PREVIEW_URL, data, function(response){
            $('#preview_container').show();
            $('#preview_body').html(response);
        });
    });
});

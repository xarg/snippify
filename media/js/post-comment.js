var previewed = false;
var commentBusy = false;
$(document).ready(function() {
	$('.preview-comment').click(function(e){
		e.preventDefault();
		$('.comment-preview').fadeIn();
		$('.comment-preview .content').text($('#id_comment').val());
	})
    $('.comment-form form').submit(function(e) {
    	e.preventDefault();
        ajaxComment();
    });
});

function ajaxComment() {
    $('div.comment-error').text('');
	$('.comment-preview').hide();
    if (commentBusy) {
        $('div.comment-form form').before('\
            <div class="comment-error">\
                Your comment is currently in the process of posting.\
            </div>\
        ');
        $('div.comment-error').fadeOut(2000);
        return false;
    }
    comment = $('div.comment-form form').serialize();
    // Add a wait animation
    $('.submit').after('\
        <img src="' + MEDIA_URL + '/images/ajax-wait.gif" alt="Please wait..."\
            class="ajax-loader" />\
    ');
    url = $('div.comment-form form').attr('action');
    // Use AJAX to post the comment.
    $.ajax({
        type: 'POST',
        url: url,
        data: comment,
        success: function(data) {
            removeWaitAnimation()
            if (data.error) {
				commentFailure(data.error);
            } else {
                commentSuccess(data.content);
            }
        },
        error: function(data) {
            removeWaitAnimation()
            commentFailure('Something when wrong. Refresh this page and try again');
        },
        dataType: 'json'
    });
    return false;
}
function commentSuccess(content) {
	if ($('#snippet-comments .comment-list').children().length == 0) {
		$('div#comments').prepend('<h2 class="comment-hd">1 comment so far:</h2>')
	}
	$('#id_comment').val('');
	$('#snippet-comments .comment-list').append(content);
	$('div.comment-item:last').show('slow');
}
function commentFailure(error) {
    $('.comment-error').text(error);
}
function removeWaitAnimation() {
    // Remove the wait animation and message
    $('.ajax-loader').remove();
    $('div.comment-waiting').stop().remove();
}
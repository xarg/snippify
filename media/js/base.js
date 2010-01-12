$(document).ready(function(){
	searchDefault = $("#big-search-input").val();
	if (searchDefault == '') { $("#big-search-input").addClass('default'); }
	$("#big-search-input").focus(function(event){
		if ($(this).val() == searchDefault)  {
			$(this).removeClass('default');
		}
	});
	$("#big-search-input").blur(function(event){
		if ($(this).val() == '') {
			$(this).addClass('default');
		}
	});
	$("#show-restkey").click(function(event){
		$("#show-restkey").slideUp("fast",function() {
			$("#the-restkey").slideDown("fast");
		});
	});
	$("#flash_message").click(function(event){
		$('#flash_message').slideUp("fast");
	});
	$('#seo-text-more').hide();
	$("#read-more-seo").click(function(event){
		$('#seo-text-more').slideDown("");
		$('#read-more-seo').slideUp("fast");
	});
	$('#one-two-three').click(function(){
		if($(this).hasClass('logged')){
			window.location = '/create/'
		}else{
			window.location = '/account/signin/'
		}
	})
	setTimeout('$("#flash_message").slideUp("fast")', 5000);
});
function qsearch() {
	searchDefault = $("#big-search-input").val();
	$("#big-search-input").focus();
	$(this).removeClass('default');
}